from re import search, I
from concurrent.futures import ThreadPoolExecutor
from config.auxiliary.encrypt import get_html
from core.my_class import Plugin


class Scan(Plugin):
    def __init__(self):
        super().__init__()
        self.name = 'java_frame'
        self.type = 'web'
        self.time = '2022-02-02'
        self.author = 'beginner'

    def check(self, headers, html):
        try:
            flag = False
            for key, value in headers.items():
                flag |= search("org.springframework.web.servlet.i18n.CookieLocaleResolver.LOCALE=", value) is not None
                if flag:
                    return "spring_java"

            flag |= search(r"<\w[^>]*(=\"/_jcr_content/){1}[^>]*>", html) is not None
            if flag:
                return "jackrabbit_java"

            return flag
        except Exception as error:
            return error

    def get_result(self, page):
        try:
            code, headers, title, html = page['response']
            if code == 404:
                return False
            if frame := self.check(headers=headers, html=html):
                return frame
            return False
        except Exception as error:
            return False

    def scan(self, scanner):
        try:
            for page in scanner.website_page:
                if scanner.frame:
                    break
                result = self.get_result(page)
                if result:
                    scanner.frame = result
        except Exception as error:
            print('java_frame')
