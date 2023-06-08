import pymysql as mysql

from py.util import read_yaml


def connect_mysql():
    conn = mysql.connect(host=read_yaml('database.mysql.host'),
                         user=read_yaml('database.mysql.username'),
                         password=read_yaml('database.mysql.password'),
                         db=read_yaml('database.mysql.db'),
                         port=read_yaml('database.mysql.port'),
                         charset='utf8')
    return conn, conn.cursor()


def execute_sql(cursor, sql):
    cursor.execute(sql)
    return cursor.fetchall()


def insert_content_table(sessionId, role_num, question):
    conn, cursor = connect_mysql()
    sql = "INSERT INTO content(`session_id`, `role`, `sentence`) VALUE(\'" \
          + sessionId + "\', " + role_num + ", \'" + question + "\');"
    execute_sql(cursor, sql)
    conn.commit()


def insert_message_table(name, sessionId):
    conn, cursor = connect_mysql()
    sql = "INSERT INTO message(`name`, `session_id`) VALUE(\'" + name + "\', \'" + sessionId + "\');"
    execute_sql(cursor, sql)
    conn.commit()
