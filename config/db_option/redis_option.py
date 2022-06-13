# 作者：博客园_杠上花
# 邮箱: a2578629964@163.com
# 时间：2022年1月20日
# 编码：utf-8
# 版本：python3.8
import time
import redis
from scan_setting import REDIS_HOST, REDIS_GROUP, REDIS_STREAM, REDIS_DICT, REDIS_STATISTICS, REDIS_PASSWORD


def test_connect():
    try:
        host, port = REDIS_HOST.split(":")
        r = redis.Redis(host=host, port=port, password=REDIS_PASSWORD)
        if r.ping():
            # 对redis stream的配置
            if r.exists(REDIS_STREAM):
                r.delete(REDIS_STREAM)
            r.xadd(name=REDIS_STREAM, id='*', fields={'k': 'v'})
            r.xgroup_create(name=REDIS_STREAM, groupname=REDIS_GROUP)
            # 分别记录扫描成功的ip域名总数
            r.hset(REDIS_DICT, key='ip', value=0)
            r.hset(REDIS_DICT, key='domain', value=0)
            # 记录扫描状态，开始时间、结束时间扫描总数，扫描成功数、扫描失败数
            r.hset(REDIS_STATISTICS, key='start_time', value=time.time())
            r.hset(REDIS_STATISTICS, key='end_time', value=0)
            r.hset(REDIS_STATISTICS, key='scan_sum', value=0)
            r.hset(REDIS_STATISTICS, key='scan_success', value=0)
            r.hset(REDIS_STATISTICS, key='scan_fail', value=0)

            return True
        else:
            return False
    except Exception:
        raise redis.exceptions.ConnectionError


def create_connect(db=0):
    host, port = REDIS_HOST.split(":")
    pool = redis.ConnectionPool(host=host, port=port, db=db, password=REDIS_PASSWORD, max_connections=50,
                                decode_responses=True)
    r = redis.Redis(connection_pool=pool, single_connection_client=False)
    while True:
        try:
            if r.ping():
                break
        except:
            print('连接失败,正在尝试重新连接')
        time.sleep(5)

    return r
