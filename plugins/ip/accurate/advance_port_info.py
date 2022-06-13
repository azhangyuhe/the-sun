# 作者：博客园_杠上花
# 邮箱: a2578629964@163.com
# 时间：2022年1月20日
# 编码：utf-8
# 版本：python3.8
import ftplib
import os
import re
import pymysql
import nmap

from core.Global import BURP_SERVER_DICT
from core.my_class import Plugin, IpScanner
from data.weak_password import user_pass
from concurrent.futures import ThreadPoolExecutor, as_completed


class Template:
    def __init__(self, hostname, port):
        self.hostname = hostname
        self.port = port

    def anonymous_login(self):
        pass

    def weak_passwd(self):
        pass

    def empty_passwd(self):
        pass

    def unauthorized_access(self):
        pass


class FTP(Template):
    def anonymous_login(self):
        try:
            with ftplib.FTP(self.hostname) as ftp:  # 创建Ftp对象 默认21端口号
                ftp.connect(port=self.port)
                ftp.login()  # Ftp匿名登录
                ftp.quit()
                return self.port, 'anonymous_login'
        # 报错说明匿名登录失败
        except Exception as e:
            return False

    def ftp_backdoor(self):
        nm = nmap.PortScanner()
        # 配置nmap参数
        result = nm.scan(hosts=self.hostname,
                         arguments=f'-p {self.port} --script=ftp-vsftpd-backdoor')
        if result['scan'][self.hostname]['tcp'][self.port].get('script', ''):
            return self.port, 'ftp-vsftpd-backdoor'


class MYSQL(Template):
    def empty_passwd(self):
        for username in user_pass:
            try:
                pymysql.connect(host=self.hostname, port=self.port, user=username, passwd="", connect_timeout=2)
                return self.port, f'empty_passwd({username})'
            except Exception as e:
                pass


def weak_passwd(port, shell):
    print('weak', port)
    result = os.popen(shell).read()
    login = re.compile(r'login:(.*?)password:(.*?)\n')
    match_group = login.search(result)
    if match_group:
        return port, f'weak_passwd;{match_group.group(1).strip()},{match_group.group(2).strip()}'


class Scan(Plugin):
    def __init__(self):
        super().__init__()
        self.name = 'advance_port_info'
        self.type = 'ip'
        self.time = '2022-02-02'
        self.author = 'beginner'

    def scan(self, scanner: IpScanner):
        executor = ThreadPoolExecutor(max_workers=3)
        all_task = []
        for port in scanner.port:
            try:
                service = scanner.port[port]['server']
                if service == 'ftp':
                    ftp = FTP(scanner.ipv4, port)
                    shell = f'hydra {scanner.ipv4} ftp  -f -s {port} -I 10 -l root  -P {BURP_SERVER_DICT} '
                    all_task.append(executor.submit(ftp.ftp_backdoor))
                    all_task.append(executor.submit(weak_passwd, port, shell))
                    all_task.append(executor.submit(ftp.anonymous_login))
                elif service == 'mysql':
                    mysql = MYSQL(scanner.ipv4, port)
                    shell = f'hydra -f -s {port} -I -t 4 -l root  -P {BURP_SERVER_DICT} mysql://{scanner.ipv4}'
                    all_task.append(executor.submit(weak_passwd, port, shell))
                    all_task.append(executor.submit(mysql.empty_passwd))
                elif service == 'ssh':
                    shell = f'hydra -q -f -s {port} -I -t 4 -l root  -P {BURP_SERVER_DICT} ssh://{scanner.ipv4}'
                    all_task.append(executor.submit(weak_passwd, port, shell))
                elif service == 'telnet':
                    shell = f'hydra -f -s {port} -I -t 10 -l root  -P {BURP_SERVER_DICT} telnet://{scanner.ipv4}'
                    all_task.append(executor.submit(weak_passwd, port, shell))
                elif service == 'postgresql':
                    shell = f'hydra -f -s {port} -I -q -t 5 -l root  -P {BURP_SERVER_DICT} postgres://{scanner.ipv4}'
                    all_task.append(executor.submit(weak_passwd, port, shell))

            except Exception as error:
                print('continue', port)
                print(error)
                continue

        for future in as_completed(all_task):
            if future.result():
                port, result = future.result()
                if ';' in result:
                    scanner.port[port]['leak'].append(
                        {"name": result.split(';')[0], 'more_info': {'payload': '', 'content': result.split(';')[1]}})
                else:
                    scanner.port[port]['leak'].append({"name": result, 'more_info': {'payload': '', 'content': ''}})
