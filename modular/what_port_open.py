# 作者：博客园_杠上花
# 邮箱: a2578629964@163.com
# 时间：2022年1月20日
# 编码：utf-8
# 版本：python3.8
import os
from core.Global import LOGGER


def scan(scanner):
    ip = scanner.ipv4
    LOGGER.info(f'[*] {ip} what_port_open')
    try:
        f = os.popen(f'./thirdpart/port_scan {scanner.ipv4}')
        data = f.readlines()
        data = list(set([i.strip().split(':')[1] for i in data]))
        f.close()
        if data:
            for i in data:
                scanner.port[int(i)] = {"server": "", "version": "", "banner": "",
                                   "leak": [],
                                   "http": {'title': '', 'status_code': '', 'web_finger': [], 'arachni': []}}
            return False
        else:
            return True
    except Exception as error:
        print('port scan error:', error)
        return True
