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


conn, cursor = connect_mysql()


def execute_sql(cursor, sql):
    cursor.execute(sql)
    return cursor.fetchall()


def insert_content_table(content_arr):
    sql = "INSERT INTO content(`session_id`, `role`, `sentence`) VALUES"
    sql_arr = []
    for content in content_arr:
        value = "(\'" + content['sessionId'] + "\'," + str(get_num_by_role(content['role'])) + ",\'" + content[
            'content'] + "\'),"
        sql_arr.append(value)
    sql += "".join(sql_arr)
    execute_sql(cursor, sql[0:len(sql) - 1])
    conn.commit()


def insert_message_table(message):
    name = message['name']
    sessionId = message['sessionId']
    sql = "INSERT INTO message(`name`, `session_id`) VALUE(\'" + name + "\', \'" + sessionId + "\');"
    execute_sql(cursor, sql)
    conn.commit()


def get_content(sessionId):
    sql = "SELECT * FROM content c WHERE c.`session_id` = \'" + sessionId + "\'"
    return execute_sql(cursor, sql)


def update_time(session_id):
    sql = "UPDATE message m SET m.`time` = NOW() WHERE m.`session_id` = \'" + str(session_id) + "\'"
    print(sql)
    execute_sql(cursor, sql)
    conn.commit()


# 更新message和content
def update_db():
    return None


def query_history():
    sql = "SELECT * FROM message m ORDER BY m.`time` DESC LIMIT 0, 7;"
    return execute_sql(cursor, sql)


def query_content_list(id):
    sql = "SELECT * FROM content c WHERE c.`session_id` = (SELECT m.`session_id` FROM message m WHERE m.`id` = " + \
          str(id) + ")"
    return execute_sql(cursor, sql)


def get_sessionId_by_msgId(id):
    sql = "SELECT m.`session_id` FROM message m WHERE m.`id` = " + str(id)
    return execute_sql(cursor, sql)


if __name__ == '__main__':
    history_list = (query_history())
    print(str(history_list))
