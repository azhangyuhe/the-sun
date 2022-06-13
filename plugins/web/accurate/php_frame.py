import re
from re import search, I
from core.my_class import Plugin
from concurrent.futures import ThreadPoolExecutor


class Scan(Plugin):
    def __init__(self):
        super().__init__()
        self.name = 'python_frame'
        self.type = 'web'
        self.time = '2022-02-02'
        self.author = 'beginner'

    def check(self, headers, html):
        flag = False
        try:
            for key, value in headers.items():
                flag |= search("CAKEPHP=", value) is not None
                if flag:
                    return "cakephp_php"
                flag |= search("ci_session=", value) is not None
                if flag:
                    return "codeigniter_php"
                flag |= search("fuelcid=", value) is not None
                if flag:
                    return "fuelphp_php"
                flag |= search("laravel_session=", value) is not None
                if flag:
                    return "laravel_php"
            flag |= search(r"<meta name=\"generator\" content=\"Seagull Framework\" />", html, flags=re.M) is not None
            flag |= search(
                r"Powered by <a href=\"http://seagullproject.org[/]*\" title=\"Seagull framework homepage\">Seagull PHP Framework</a>",
                html, flags=re.M) is not None
            flag |= search(r"var SGL_JS_SESSID[\s]*=", html, flags=re.M) is not None
            if flag:
                return "seagull_php"
            flag |= search(r"<meta name=\"generator\" content=\"Zend.com CMS", html, flags=re.M) is not None
            flag |= search(r"<meta name=\"vendor\" content=\"Zend Technologies", html, flags=re.M) is not None
            flag |= search(r"\"Powered by Zend Framework\"", html, flags=re.M) is not None
            flag |= search(r" alt=\"Powered by Zend Framework!\" />", html, flags=re.M) is not None
            if flag:
                return "zend_php"
            flag |= search(r'Powered by <a href="http://fuelphp\.com">FuelPHP</a>', html, flags=re.M) is not None
            if flag:
                return "fuelphp_php"
            return flag
        except Exception as error:
            print(error)
            return flag

    def get_result(self, page):
        try:
            code, headers, title, html = page['response']
            if code == 404:
                return False
            if frame := self.check(headers=headers, html=html):
                return frame
            return False
        except Exception:
            return False

    def scan(self, scanner):
        try:
            for page in scanner.website_page:
                if scanner.frame:
                    break
                result = self.get_result(page)
                if result:
                    scanner.frame = result
        except Exception:
            print('php_frame')
