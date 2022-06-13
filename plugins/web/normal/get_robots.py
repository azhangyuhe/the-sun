# 作者：博客园_杠上花
# 邮箱: a2578629964@163.com
# 时间：2022年1月20日
# 编码：utf-8
# 版本：python3.8
import requests
from config.auxiliary import encrypt
from core.my_class import Plugin, Scanner


class Scan(Plugin):
    def __init__(self):
        super().__init__()
        self.name = 'get_robots'
        self.type = 'web'
        self.time = '2022-02-02'
        self.author = 'beginner'

    def check(self, html):
        if 'User-agent' in html or 'Allow' in html or 'Disallow' in html:
            return True
        return False

    def scan(self, scanner: Scanner):
        try:
            response = requests.get(url=f'{scanner.scheme}://{scanner.domain}/robots.txt', headers=scanner.headers,
                                    verify=False)
            if response.status_code == 200:
                html = encrypt.get_html(response)
                if html:
                    if self.check(html):
                        scanner.robots = html
            else:
                pass
        except Exception as error:
            pass
