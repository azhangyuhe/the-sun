# 作者：博客园_杠上花
# 邮箱: a2578629964@163.com
# 时间：2022年1月20日
# 编码：utf-8
# 版本：python3.8
"""
tcp/ip协议中，专门保留了三个IP地址区域作为私有地址，其地址范围如下：
10.0.0.0/8：10.0.0.0～10.255.255.255
172.16.0.0/12：172.16.0.0～172.31.255.255
192.168.0.0/16：192.168.0.0～192.168.255.255
"""
from core.Global import LOGGER


def is_lan(ip_l):
    """

    :param ip_l:
    :return:
    """
    if ip_l[0] == 10:
        return True
    elif ip_l[0] == 172 and (16 <= ip_l[1] <= 31):
        return True
    elif ip_l[0] == 192 and ip_l[1] == 168 and (1 <= ip_l[2] <= 255):
        return True
    return False


def scan(scanner):
    ip = scanner.ipv4
    ip_l = [int(i) for i in ip.split('.')]
    if is_lan(ip_l):
        scanner.ip_type = "LAN"
    elif ip == '0.0.0.0' or ip == '127.0.0.1':
        scanner.ip_type = "LAN"
    else:
        scanner.ip_type = "INTERNET"

    LOGGER.info(f"[*] {scanner.ipv4} type is {scanner.ip_type}")
