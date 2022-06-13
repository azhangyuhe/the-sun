import os
import ssl
import sys
import time
import redis
import signal
import requests
import multiprocessing
from sys import path
from urllib3 import disable_warnings
# ===============================================
from core.scan_controller import start
from plugins.ip.accurate.arachni import arachni_test
from core.Global import BANNER, LOGGER, ORIGINAL_SIGINT
from config.db_option.es_option import elasticsearch_test
from config.db_option.redis_option import test_connect as redis_test
from config.db_option.mysql_option import mysql_test
from scan_setting import CHECK_INTERNET_VALUE, CHECK_INTERNET_ADDRESS


def my_exit(signum, fram):
    # 恢复为默认处理方式--->交给KeyboardInterrupt处理
    signal.signal(signal.SIGINT, ORIGINAL_SIGINT)

    try:
        print("[!] If you want to quit, Press Ctrl+C again!")
        time.sleep(3)
    except KeyboardInterrupt:
        time.sleep(0.3)
        print("[!] GoodBye！")
        sys.exit()

    signal.signal(signal.SIGINT, my_exit)


def check_connect():
    """
    验证其他组件是否能成功连接

    :return redis.exceptions.ConnectionError: Redis connection succeeded
    :raises Exception: Arachni cannot connect
    """
    check_content = requests.get(CHECK_INTERNET_ADDRESS).content.decode()
    if CHECK_INTERNET_VALUE in check_content:
        LOGGER.info('[*] Successfully connected to the Internet')
    else:
        raise requests.exceptions.ConnectionError

    if redis_test():
        LOGGER.info('[*] Redis connection succeeded')
    else:
        raise redis.exceptions.ConnectionError

    if arachni_test():
        LOGGER.info('[*] Arachni connection succeeded')
    else:
        LOGGER.warning('[!] Arachni cannot connect')
        raise Exception

    if elasticsearch_test():
        LOGGER.info('[*] Elasticsearch connection succeeded')
    else:
        LOGGER.warning('[!] Elasticsearch cannot connect')
        raise Exception

    if mysql_test():
        LOGGER.info('[*] Mysql connection succeeded')
    else:
        LOGGER.warning('[!] Mysql cannot connect')
        raise Exception


def clean_net_error():
    """
    清除网络请求和路径引用可能带来的错误

    :return: None
    """
    # 官方强制验证https的安全证书，然添加忽略验证的参数，但是依然会给出警告1
    disable_warnings()
    # Python2/3 解决访问Https时不受信任SSL证书问题
    ssl._create_default_https_context = ssl._create_unverified_context
    path.append(os.path.dirname(os.path.abspath(__file__)))
    path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def main():
    try:
        # 优雅退出
        signal.signal(signal.SIGINT, my_exit)
        # 输出banner
        sys.stdout.write(BANNER)
        # 消除网络请求可能出现的错误
        clean_net_error()
        # 检测互连网、redis、Elasticsearch能否成功连接
        check_connect()
        start()

    except requests.exceptions.ConnectionError:
        LOGGER.warning('[!] Unable to connect to the Internet, please check the network')

    except redis.exceptions.ConnectionError:
        LOGGER.warning('[!] Redis cannot connect')

    except Exception as error:
        LOGGER.warning(error)


if __name__ == '__main__':
    # 设置多进程模式
    multiprocessing.set_start_method('spawn')
    main()
