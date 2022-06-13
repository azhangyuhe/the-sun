# 作者：博客园_杠上花
# 邮箱: a2578629964@163.com
# 时间：2022年1月20日
# 编码：utf-8
# 版本：python3.8
import re


def strand_ip(value):
    ip = r"^\d{1,3}(\.\d{1,3}){3}$"
    if value and re.match(ip, value):
        return True
    else:
        return False

def strand_url(value):
    url=r"^(http|https)://.*$"
    if value and re.match(url, value):
        return True
    else:
        return False

if __name__ == '__main__':
    print(strand_url(''))