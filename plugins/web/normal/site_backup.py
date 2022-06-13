import requests
from core.my_class import Plugin
from concurrent.futures import ThreadPoolExecutor


class Scan(Plugin):
    def __init__(self):
        super().__init__()
        self.name = 'site_backup'
        self.type = 'web'
        self.time = '2022-02-02'
        self.author = 'beginner'

    def check(self, content):
        features = [b'PK\x03\x04\x14', b'\x04\x03\x4b\x50', b'\x50\x4b\x03\x04', b'\x52\x61\x72\x21',
                    b'\x2d\x2d\x20\x4d', b'\x2d\x2d\x20\x70\x68', b'\x2f\x2a\x0a\x20\x4e',
                    b'\x2d\x2d\x20\x41\x64', b'\x2d\x2d\x20\x2d\x2d', b'\x2f\x2a\x0a\x4e\x61']
        for i in features:
            if content.startswith(i):
                return True
        return False

    def load_poc(self, url):
        poc = [
            '.git', 'web.tar', 'website.tar', 'backup.tar', 'back.tar', 'www.tar', 'wwwroot.tar', 'temp.tar',
            'web.tar.gz',
            'website.tar.gz', 'backup.tar.gz', 'back.tar.gz', 'www.tar.gz', 'wwwroot.tar.gz', 'temp.tar.gz', 'web.zip',
            'website.zip', 'backup.zip', 'back.zip', 'www.zip', 'wwwroot.zip', 'temp.zip', 'web.rar', 'website.rar',
            'backup.rar', 'back.rar', 'www.rar', 'wwwroot.rar', 'temp.rar'
        ]
        return [f'{url}/{i}' for i in poc]

    def get_result(self, url):
        try:
            headers = {
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'}
            response = requests.get(url=url, headers=headers, allow_redirects=False)
            if 200 <= response.status_code < 300:
                head_flag = response.raw.read(10)
            else:
                return False
            if self.check(head_flag) or "application/" in response.headers.get("Content-Type", ''):
                return url
        except Exception as error:
            return False
        return False

    def scan(self, scanner):
        url = f'{scanner.scheme}://{scanner.domain}'
        pocs = self.load_poc(url)
        try:
            with ThreadPoolExecutor(max_workers=10) as pool:
                results = pool.map(self.get_result, pocs)
                for result in results:
                    if result:
                        scanner.leak.append(
                            {'name': '网站备份', 'more_info': {'payload': result, 'content': ''}})


        except Exception as error:
            print('site_backup')



