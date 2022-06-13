# 作者：博客园_杠上花
# 邮箱: a2578629964@163.com
# 时间：2022年1月20日
# 编码：utf-8
# 版本：python3.8
import requests
import urllib3
from lxml import etree
from config.auxiliary import common

urllib3.disable_warnings()


def scan(url, port, ip_data):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'}
    try:
        response = requests.get(url=url, headers=headers, timeout=10)
        if response.status_code > 399:
            return False
        response_headers = response.headers
        response_html = common.get_html(response)
        try:
            xpath_html = etree.HTML(response_html)
        except Exception as error:
            html = bytes(bytearray(response_html, encoding='utf-8'))
            xpath_html = etree.HTML(html)
        title = xpath_html.xpath('/html/head/title/text()')[0]
        ip_data['port'][port]['web'] = {'title': str(title), 'html': str(response_html), 'headers': dict(response_headers)}
        return True
    except requests.exceptions.ConnectionError:
        return False
    except IndexError:
        ip_data['port'][port]['web'] = {'title': '', 'html': str(response_html), 'headers': dict(response_headers)}
        return True
    except Exception as e:
        return False
