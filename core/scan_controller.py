import signal
import sys
import threading
import multiprocessing
# =======================================================
import time

from config.db_option.redis_option import create_connect
from core.init import init
from core.my_class import ReachableError, PortOpenError, DomainError, IpScanner, Scanner
from scan_setting import PROCESS_NUM, REDIS_DICT, REDIS_STATISTICS
from scan_setting import REDIS_LIST
from core.Global import LOGGER, ORIGINAL_SIGINT
from scan_setting import ES_PATH, ES_PATH_DOMAIN, REDIS_GROUP, REDIS_STREAM
from config.db_option.es_option import option
from config.db_option.mysql_option import insert_data
from modular import *


def ip_scan(scanner: IpScanner, PLUGINS):
    thread_list = []
    # 判断ip是否可达 如果不可达直接扫描下一个任务
    result = judge_reachable.scan(scanner)
    if result:
        raise ReachableError(f'[!] {scanner.ipv4} Invalid value of IP')

    # 判断该ip是内网还是外网两种扫描模式会有不同
    decide_ip_type.scan(scanner)

    # 如果ip类型是外网会扫描地理位置
    if scanner.ip_type == 'INTERNET':
        Geography.scan(scanner)

    # 扫描端口开放情况
    empty = what_port_open.scan(scanner)
    if empty:
        raise PortOpenError(f'[!] {scanner.ipv4}_Empty open of port')
    # 端口版本、操作系统版本
    port_server_version.scan(scanner)
    if PLUGINS.get('normal'):
        for name, plug in PLUGINS['normal']:
            t = threading.Thread(target=plug.scan, args=(scanner,))
            thread_list.append(t)
            t.start()


    if PLUGINS.get('os'):
        for name, plug in PLUGINS['os']:
            t = threading.Thread(target=plug.scan, args=(scanner,))
            thread_list.append(t)
            t.start()

    if PLUGINS.get('accurate'):
        if scanner.speed_mode and scanner.ip_type == 'LAN':
            for name, plug in PLUGINS['accurate']:
                t = threading.Thread(target=plug.scan, args=(scanner,))
                thread_list.append(t)
                t.start()
    for t in thread_list:
        t.join()

    scanner.format_data()


def domain_scan(scanner: Scanner, D_PLUGINS):
    thread_list = []
    # 已知域名尝试性获取ip(中小网站可能为真实ip、大型网站一般有cdn)
    domain_get_ip.scan(scanner)
    if get_scheme.scan(scanner):
        LOGGER.info(f'[*] {scanner.domain} scan normal!')
        if D_PLUGINS.get('normal'):

            for name, plug in D_PLUGINS.get('normal'):
                t = threading.Thread(target=plug.scan, args=(scanner,))
                thread_list.append(t)
                t.start()

        # 上面的插件与爬取页面无关(server_poc、whois、robots等等)
        LOGGER.info(f'[*] {scanner.domain} scan crawl!')
        crawl.scan(scanner)  # 爬取该域名下尽可能多的页面
        # 下面的插件与爬取页面有关(每个页面的banner、每个页面的备份文件、page可能存在的漏洞)
        LOGGER.info(f'[*] {scanner.domain} scan server!')
        if D_PLUGINS.get('server'):
            for name, plug in D_PLUGINS['server']:
                t = threading.Thread(target=plug.scan, args=(scanner,))
                thread_list.append(t)
                t.start()
        LOGGER.info(f'[*] {scanner.domain} scan accurate!')
        if D_PLUGINS.get('accurate'):
            for name, plug in D_PLUGINS['accurate']:
                plug.scan(scanner)

        for t in thread_list:
            t.join()
        scanner.format_data()
        # print(scanner.__dict__)
        LOGGER.info(f'[+] {scanner.domain} scan over!')
    else:
        raise DomainError('domain error')


def consumer():
    """
    在redis消费者组中接受任务 任务分为domain和ip两类进行扫描

    :return:
    """
    PLUGINS, D_PLUGINS = init()
    LOGGER.warning('[*] plugin load over')
    while True:
        try:
            redis_connect = create_connect()
            print(multiprocessing.current_process().name)
            task_content = redis_connect.xreadgroup(groupname=REDIS_GROUP, consumername=str(id(redis_connect)),
                                                    streams={REDIS_STREAM: ">"}, block=0, count=1)
            tmp = task_content[0][1][0][1].get('key')
            scan_type, target, scan_speed, scan_mode = tmp.strip('"').split('_')
            redis_connect.hincrby(REDIS_STATISTICS, 'scan_sum')
            if 'ip' == scan_type:
                LOGGER.info(f'[*] start scan{target}')
                speed = False if scan_speed == 'f' else True
                mode = False if scan_mode == 'f' else True
                scanner = IpScanner(target, speed, mode, redis_connect)
                ip_scan(scanner, PLUGINS)

            elif 'domain' == scan_type:
                LOGGER.info(f'[*] start scan{target}')
                speed = False if scan_speed == 'f' else True
                mode = False if scan_mode == 'f' else True
                scanner = Scanner(target, speed, mode, redis_connect)
                domain_scan(scanner, D_PLUGINS)
            else:
                LOGGER.warning('[!] Wrong scan type,only scan ip or domain')
        except DomainError as error:
            LOGGER.warning('DomainError')
        except ReachableError as error:
            LOGGER.warning(error)
        except PortOpenError as error:
            LOGGER.warning(error)
        except KeyError as e:
            print(e)
            LOGGER.warning('KeyError')
        except KeyboardInterrupt:
            raise KeyboardInterrupt
        except Exception as e:
            LOGGER.warning(f'[!!] {e}')


def transmit():
    """
    因为是多进程扫描使用redis接收每个进程扫描结果并存入数据库

    :return:
    """
    redis_connect = create_connect()
    while True:
        result = redis_connect.brpop(REDIS_LIST)[1]
        try:
            redis_connect.hincrby(REDIS_STATISTICS, 'scan_success')
            if result[0] == 't':
                redis_connect.hincrby(REDIS_DICT, 'ip')
                tmp = int(redis_connect.hget(REDIS_DICT, 'ip'))
                if tmp % 5 == 0:
                    try:
                        option.insert_es(ES_PATH, 'scan_ip', 5000)
                        with open(ES_PATH, 'w') as fp:
                            fp.write(result[1:])
                            fp.write('\n')
                    except:
                        with open(ES_PATH, 'a') as fp:
                            fp.write(result[1:])
                            fp.write('\n')
                else:
                    with open(ES_PATH, 'a') as fp:
                        fp.write(result[1:])
                        fp.write('\n')

            else:
                print('domain')
                redis_connect.hincrby(REDIS_DICT, 'domain')
                tmp = int(redis_connect.hget(REDIS_DICT, 'domain'))
                if tmp % 5 == 0:
                    try:
                        option.insert_es(ES_PATH_DOMAIN, 'scan_domain', 5000)
                        with open(ES_PATH_DOMAIN, 'w') as fp:
                            fp.write(result[1:])
                            fp.write('\n')
                    except:
                        with open(ES_PATH_DOMAIN, 'a') as fp:
                            fp.write(result[1:])
                            fp.write('\n')
                else:
                    with open(ES_PATH_DOMAIN, 'a') as fp:
                        fp.write(result[1:])
                        fp.write('\n')
        except Exception as error:
            print('transmit')
            print(error)


def start():
    """
    开启多进程扫描并且开启redis转接

    :return:
    """

    def call():
        # requests.get()
        pass

    try:
        signal.signal(signal.SIGINT, ORIGINAL_SIGINT)
        # threading.Thread(target=call, daemon=True).start()
        pool = multiprocessing.Pool(processes=PROCESS_NUM)
        for i in range(PROCESS_NUM):
            proc_name = f'proc_{i + 1}'
            pool.apply_async(func=consumer)

        LOGGER.info('[*] Forward processing')
        transmit()

    except KeyboardInterrupt:
        # 键盘中断 清除进程池中的进程
        r = create_connect()
        r.hset(REDIS_STATISTICS, key='end_time', value=time.time())
        start_time = r.hget(name=REDIS_STATISTICS, key='start_time')
        end_time = r.hget(name=REDIS_STATISTICS, key='end_time')
        total_tasks = int(r.hget(name=REDIS_STATISTICS, key='scan_sum'))
        success_task = int(r.hget(REDIS_DICT, 'ip')) + int(r.hget(REDIS_DICT, 'domain'))
        fail_task = total_tasks - success_task
        print(11111111111111)
        insert_data((start_time, end_time, total_tasks, success_task, fail_task), 'scan_record')
        pool.terminate()
        sys.exit()
