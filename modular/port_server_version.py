# 作者：博客园_杠上花
# 邮箱: a2578629964@163.com
# 时间：2022年1月20日
# 编码：utf-8
# 版本：python3.8
from core.Global import LOGGER


def scan(scanner):
    LOGGER.info(f'[*] {scanner.ipv4} port_server_version')
    ip = scanner.ipv4
    port = ','.join([str(i) for i in scanner.port])
    nm = scanner.nmap
    scan_raw_result = nm.scan(hosts=ip, arguments=f'-sV --script=banner -p {port} -O')
    base = scan_raw_result['scan'][ip]
    os = []
    try:
        for port, info in base['tcp'].items():
            scanner.port[port]["server"] = info.get('name', 'unknown')
            scanner.port[port]["version"] = info.get('product', '') + " " + info.get('version', '')
            if script := info.get('script'):
                scanner.port[port]['banner'] = script.get('banner', '')
        for i in base.get('osmatch'):
            os.append(i.get('name'))
        scanner.os = os
    except Exception as error:
        print('port server version error')
