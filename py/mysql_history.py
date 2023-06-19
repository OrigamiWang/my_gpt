import pymysql as mysql

from py.util import read_yaml, get_num_by_role


def connect_mysql():
    conn = mysql.connect(host=read_yaml('database.mysql.host'),
                         user=read_yaml('database.mysql.username'),
                         password=read_yaml('database.mysql.password'),
                         db=read_yaml('database.mysql.db'),
                         port=read_yaml('database.mysql.port'),
                         charset='utf8')
    return conn, conn.cursor()


def execute_sql(sql):
    conn, cursor = connect_mysql()
    cursor.execute(sql)
    return cursor.fetchall()


def insert_content_table(content_arr):
    conn, cursor = connect_mysql()
    sql = "INSERT INTO content(`session_id`, `role`, `sentence`) VALUES"
    sql_arr = []
    for content in content_arr:
        value = "(\'" + content['sessionId'] + "\'," + str(get_num_by_role(content['role'])) + ",\'" + content[
            'content'] + "\'),"
        sql_arr.append(value)
    sql += "".join(sql_arr)
    cursor.execute(sql[0:len(sql) - 1])
    conn.commit()


def insert_message_table(message):
    conn, cursor = connect_mysql()
    name = message['name']
    sessionId = message['sessionId']
    sql = "INSERT INTO message(`name`, `session_id`) VALUE(\'" + name + "\', \'" + sessionId + "\');"
    cursor.execute(sql)
    conn.commit()


def get_content(sessionId):
    sql = "SELECT * FROM content c WHERE c.`session_id` = \'" + sessionId + "\'"
    return execute_sql(sql)


def update_time(session_id):
    conn, cursor = connect_mysql()
    sql = "UPDATE message m SET m.`time` = NOW() WHERE m.`session_id` = \'" + str(session_id) + "\'"
    print(sql)
    cursor.execute(sql)
    conn.commit()


def update_msg_name_by_id(msg_id, msg_name):
    conn, cursor = connect_mysql()
    sql = "UPDATE message m SET m.`name` = \'" + msg_name + "\' WHERE m.id = " + msg_id
    cursor.execute(sql)
    conn.commit()


def del_content_by_msg_id(msg_id):
    conn, cursor = connect_mysql()
    sql = "DELETE FROM content c WHERE c.`session_id` = (SELECT m.`session_id` FROM message m WHERE m.`id` = " \
          + msg_id + ")"
    cursor.execute(sql)
    conn.commit()


def del_message_by_msg_id(msg_id):
    conn, cursor = connect_mysql()
    sql = "DELETE FROM message m WHERE m.`id` = " + msg_id
    cursor.execute(sql)
    conn.commit()


# 删除message以及对应的content
def del_fun(msg_id):
    # 删除content
    del_content_by_msg_id(msg_id)
    # 删除message
    del_message_by_msg_id(msg_id)


def query_history():
    sql = "SELECT * FROM message m ORDER BY m.`time` DESC LIMIT 0, 7;"
    return execute_sql(sql)


def query_content_list(id):
    sql = "SELECT * FROM content c WHERE c.`session_id` = (SELECT m.`session_id` FROM message m WHERE m.`id` = " + \
          str(id) + ")"
    return execute_sql(sql)


def get_sessionId_by_msgId(id):
    sql = "SELECT m.`session_id` FROM message m WHERE m.`id` = " + str(id)
    return execute_sql(sql)


if __name__ == '__main__':
    history_list = (query_history())
    print(str(history_list))
