import redis

from py.mysql_history import get_content, query_history
from py.util import read_yaml


def connect_redis():
    return redis.Redis(read_yaml('database.redis.host'), port=read_yaml('database.redis.port'))


conn = connect_redis()


def exists_key(key):
    print(conn)
    return conn.exists(key)


def set_kv(k, v):
    conn.set(k, v)


def get_v(k):
    return conn.get(k)


def update_v(k, v):
    conn.set(k, v)


def flush_cache(sessionId):
    message_key = sessionId + "_message"
    content_key = sessionId + "_content"
    content_num_key = sessionId + "_content_num"
    conn.delete(message_key)
    conn.delete(content_key)
    conn.delete(content_num_key)


def load_history_cache():
    return get_v("history")


if __name__ == '__main__':
    history_cache = get_v("history")
    print(history_cache)
    print(eval(history_cache))
