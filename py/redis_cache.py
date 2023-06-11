import redis

from py.mysql_history import get_content
from py.util import read_yaml


def connect_redis():
    return redis.Redis(read_yaml('database.redis.host'), port=read_yaml('database.redis.port'))


conn = connect_redis()


def exists_key(sessionId):
    print(conn)
    return conn.exists(sessionId)


def set_kv(k, v):
    conn.set(k, v)


def get_v(k):
    return conn.get(k)


def update_v(k, v):
    conn.set(k, v)


def flush_cache(sessionId):
    message_key = sessionId + "_message"
    content_key = sessionId + "_content"
    conn.delete(message_key)
    conn.delete(content_key)


if __name__ == '__main__':
    print(conn.set('a', 'a'))
    print(conn.exists('a'))
