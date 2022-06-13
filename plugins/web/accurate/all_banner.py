from core.my_class import Plugin, Scanner
from modular import website_fingerprint


class Scan(Plugin):
    def __init__(self):
        super().__init__()
        self.name = 'get_robots'
        self.type = 'web'
        self.time = '2022-02-02'
        self.author = 'beginner'

    def get_result(self, page):
        try:
            code, headers, title, html = page['response']
            if code == 404:
                return []
            banner = website_fingerprint.scan(page['url'], html, title, headers)
            return banner
        except Exception:
            return []

    def scan(self, scanner: Scanner):
        try:
            num = 0
            for page in scanner.website_page:
                banner = self.get_result(page)
                if banner:
                    scanner.website_page[num]['banner'] = banner
                num += 1
        except Exception as error:
            print('allbanner')
