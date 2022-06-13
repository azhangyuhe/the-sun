import time
import redis

from scan_setting import REDIS_HOST, REDIS_STREAM, REDIS_GROUP, REDIS_PASSWORD


def create_connect(db=0):
    host, port = REDIS_HOST.split(":")
    pool = redis.ConnectionPool(host=host, port=port, password=REDIS_PASSWORD, db=db, max_connections=50,
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


add_target = create_connect()
# while True:
#     t=add_target.brpop('transmit_')
#     print(t)
# add_target.xadd(name='test_stream', id='*', fields={'k': 'v'})
# add_target.xgroup_create(name='test_stream', groupname='test_group')
# ,221.192.241.99,222.222.178.99
# for j in range(239, 241):
#     for i in range(92, 150):
#         # print(j)
#         add_target.xadd('scan_stream', id='*', fields={'key': f'ip_221.192.{j}.{i}_t_f'})
#     time.sleep(800)
# with open('open_ip.txt','r') as fp:
#     for ip in fp.readlines():
#         add_target.xadd('scan_stream', id='*', fields={'key': f'ip_{ip.strip()}_t_f'})

# add_target.xadd('scan_stream', id='*', fields={'key': f'ip_77.121.100.211_t_f'})
# add_target.xadd('scan_stream', id='*', fields={'key': f'ip_212.110.154.149_t_f'})
# add_target.xadd('scan_stream', id='*', fields={'key': f'ip_212.111.205.71_t_f'})
# add_target.xadd('scan_stream', id='*', fields={'key': f'ip_212.110.139.65_t_f'})
# add_target.xadd('scan_stream', id='*', fields={'key': f'domain_www.processon.com_t_f'})


# time.sleep(2000)
for i in range(1, 50):
    for j in range(1, 254):
        add_target.xadd('scan_stream', id='*', fields={'key': f'ip_182.141.{i}.{j}_t_f'})
    time.sleep(300)

# add_target.xadd('scan_stream', id='*', fields={'key': f'ip_114.116.11.72_t_f'})
