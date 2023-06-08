import redis

from py.util import read_yaml


def connect_redis():
    return redis.Redis(read_yaml('database.redis.host'), port=read_yaml('database.redis.port'))


if __name__ == '__main__':
    conn = connect_redis()
    print(conn.ttl('uuid'))
