# 作者：博客园_杠上花
# 邮箱: a2578629964@163.com
# 时间：2022年1月20日
# 编码：utf-8
# 版本：python3.8
def sP(nm, ip):
    ping_scan_raw_result = nm.scan(hosts=ip, arguments='-sP')
    status = ping_scan_raw_result.get('nmap').get('scanstats').get('uphosts')
    if status == '1':
        return True


def sS(nm, ip):
    ping_scan_raw_result = nm.scan(hosts=ip, arguments='-sS -p 1111')
    status = ping_scan_raw_result.get('nmap').get('scanstats').get('uphosts')
    if status == '1':
        return True


def scan(scanner):
    """
    输入一个ip 如果ip存活返回False否则返回True

    :param ip:
    :return:
    """
    ip = scanner.ipv4
    nm = scanner.nmap
    if sP(nm, ip):
        return False
    if sS(nm, ip):
        return False
    return True
