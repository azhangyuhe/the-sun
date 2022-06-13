# 作者：博客园_杠上花
# 邮箱: a2578629964@163.com
# 时间：2022年1月20日
# 编码：utf-8
# 版本：python3.8
import abc
import json
import time

import nmap
import requests
from config.auxiliary import random_ua
from config.db_option.redis_option import create_connect
from scan_setting import REDIS_LIST, REDIS_ONLINE


class Scanner:
    def __init__(self, domain, speed_mode, return_mode, redis_con):
        self.redis_con = redis_con
        self.scheme = ''
        self.domain = domain
        self.robots = ''
        self.real_ip = []
        self.whois = {}
        self.icp = {}
        self.cert = {}
        self.DNS = {'A': '', 'NS': '', 'MX': '', 'CNAME': ''}
        self.frame = ''
        self.speed_mode = speed_mode
        self.return_mode = return_mode
        self.ua = random_ua.get_ua()
        self.headers = {'User-Agent': self.ua}
        self.result = {}
        self.website_page = []
        self.page_data = []
        self.leak = []

    def update_con(self):
        self.redis_con = create_connect()

    def format_data(self):
        tmp = {'website_page': []}
        all_banner = []
        if self.leak:
            for leak_ in self.leak:
                tmp = [{'payload': leak_['more_info']['payload']}, {"content": leak_['more_info']['content']}]
                leak_['more_info'] = tmp
        for page in self.website_page:
            p_tmp = {'response_headers': []}
            if not page.get('response'):
                p_tmp['status_code'] = 404
                p_tmp['title'] = ''
            else:
                p_tmp['status_code'] = page['response'][0]
                for k, v in page['response'][1].items():
                    p_tmp['response_headers'].append({k: v})

                p_tmp['title'] = str(page['response'][2])  # <class 'lxml.etree._ElementUnicodeResult'>
            p_tmp['url'] = page['url']
            p_tmp['method'] = page['method']
            if page.get('banner'):
                p_tmp['banner'] = list(page['banner'])
                for t in p_tmp['banner']:
                    if t in all_banner:
                        continue
                    all_banner.append(t)
            else:
                p_tmp['banner'] = []
            tmp['website_page'].append(p_tmp)

        tmp.update({'all_banner': all_banner})
        tmp.update({'scheme': str(self.scheme)})
        tmp.update({'domain': self.domain})
        tmp.update({'cert': self.cert})
        tmp.update({'dns': self.DNS})
        tmp.update({'robots': self.robots})
        tmp.update({'real_ip': self.real_ip})
        tmp.update({'whois': self.whois})
        tmp.update({'icp': self.icp})
        tmp.update({'frame': self.frame})
        tmp.update({'leak': self.leak})
        tmp.update({'scan_time': time.time()})
        s_tmp = json.dumps(tmp, ensure_ascii=False)
        self.update_con()
        self.transmit('f' + s_tmp)
        if self.return_mode:
            self.redis_con.lpush(REDIS_ONLINE, s_tmp)

    def transmit(self, data):
        self.redis_con.lpush(REDIS_LIST, data)


class IpScanner:
    def __init__(self, ip, speed_mode, return_mode, redis_con):
        self.redis_con = redis_con
        self.ipv4 = ip
        self.ipv6 = ''
        self.domain = ''
        self.return_mode = return_mode  # True--> zaixian
        self.speed_mode = speed_mode  # True--> jingque
        self.ip_type = ''
        self.mac = ''
        self.ip_location = list()
        self.os = []
        self.port = {}
        self.plugins = {}
        self.nmap = nmap.PortScanner()

    def update_con(self):
        self.redis_con = create_connect()
        self.nmap = nmap.PortScanner()

    def format_data(self):
        tmp = {}
        port_tmp = []
        for i, k in self.port.items():
            if k.get('leak'):
                for leak_ in k['leak']:
                    leak_['more_info'] = [{'payload': leak_['more_info']['payload']},
                                          {"content": leak_['more_info']['content']}]
        for i, k in self.port.items():
            k.update({"port": i})
            port_tmp.append(k)
        tmp.update({'ipv4': self.ipv4})
        tmp.update({'ipv6': self.ipv6})
        tmp.update({'mac': self.mac})
        tmp.update({'ip_location': self.ip_location})
        tmp.update({'os': self.os})
        tmp.update({'port': port_tmp})
        tmp.update({'scan_time': time.time()})
        tmp.update({'domain': self.domain})
        s_tmp = json.dumps(tmp, ensure_ascii=False)
        self.update_con()
        if self.ip_type == 'LAN':
            now = time.localtime()
            now_time = time.strftime("lan_%Y_%m_%d", now)
            self.redis_con.hset(now_time, key=self.ipv4, value=s_tmp)
        else:
            self.transmit('t' + s_tmp)
            if self.return_mode:
                self.redis_con.lpush(REDIS_ONLINE, s_tmp)

    def transmit(self, data):
        self.redis_con.lpush(REDIS_LIST, data)


class Plugin:
    def __init__(self):
        self.name = None
        self.type = None
        self.time = None
        self.author = 'beginner'

    @abc.abstractmethod
    def scan(self, scanner):
        pass

    def load_poc(self, *args):
        """
        生成poc
        :param args:
        :return:
        """
        pass

    def get_result(self, *args):
        """
        用于多线程 提高速度
        :param args:
        :return:
        """
        pass

    def check(self, *args):
        """
        用于验证
        :param args:
        :return:
        """
        pass

    def my_get(self, url, headers=None):
        response = False
        proxy_pool = {'http': [], 'https': []}
        proxy = None
        try:
            if headers is None:
                headers = {'User-Agent': random_ua.get_ua()}
            response = requests.get(url=url, headers=headers, verify=False, proxies=None)
            return response
        except Exception as error:
            return response

    def my_post(self, url, headers=None, data=None):
        response = False
        proxy_pool = {'http': [], 'https': []}
        proxy = None
        if headers is None:
            headers = {'User-Agent': random_ua.get_ua()}

        try:
            if data:
                response = requests.post(url=url, headers=headers, data=data, verify=False, proxies=None)
            else:
                response = requests.post(url=url, headers=headers, verify=False, proxies=None)
            return response
        except Exception as error:
            return response


class PortOpenError(Exception):
    def __init__(self, value):
        self.value = value

    # 返回异常类对象的说明信息
    def __str__(self):
        return self.value


class ReachableError(Exception):
    def __init__(self, value):
        self.value = value

    # 返回异常类对象的说明信息
    def __str__(self):
        return self.value


class DomainError(Exception):
    def __init__(self, value):
        self.value = value

    # 返回异常类对象的说明信息
    def __str__(self):
        return self.value
