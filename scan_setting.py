# 作者：博客园_杠上花
# 邮箱: a2578629964@163.com
# 时间：2022年1月20日
# 编码：utf-8
# 版本：python3.8
import os
from multiprocessing import cpu_count

# 用于网络检测的url和对应检测返回内容的字符串
CHECK_INTERNET_ADDRESS = "http://ipinfo.io/json"
CHECK_INTERNET_VALUE = '"ip":'

# 用于扫描的进程数,每个进程对应的线程数
PROCESS_NUM = 10  # cpu_count()

PORT_RANGE = '1-15000'

# Redis数据库相关配置
REDIS_HOST = os.environ.get("REDIS_HOST", default="114.116.11.72:60001")
REDIS_PASSWORD = os.environ.get("REDIS_PASSWORD", default="0b*c566#9e3e2*")

# Elasticsearch相关配置
ES_IP = '114.116.11.72'
ES_PORT = 60000
ES_INDEX = 'scan_ip'
ES_INDEX_DOMAIN = 'scan_domain'
ES_PATH = 'data/demo'
ES_PATH_DOMAIN = 'data/demo_domain'

# 该扫描节点的名称(自定义)
REDIS_STREAM = 'scan_stream'

REDIS_ONLINE = 'online'
REDIS_LIST = 'transmit'
REDIS_GROUP = 'scan_group'
REDIS_DICT = 'monitor'
REDIS_STATISTICS = 'statistics'

# 爬取页面数量(arachni会自动爬取该网站的页面 扫描一个页面大概需要30s)
ARACHNI_IP = '127.0.0.1'
ARACHNI_PORT = '7331'
PAGE_LIST = 1

MYSQL_IP = '114.116.11.72'
MYSQL_PORT = 60002
MYSQL_USER = 'root'
MYSQL_PASSWD = 'd#db*c878dd*b227*e'

WEB_SERVER = '172.17.0.1'
ICP_API='2a6531c7bb1d43038b722db2b3339b9f'