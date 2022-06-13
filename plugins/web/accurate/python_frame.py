from re import search, I
from concurrent.futures import ThreadPoolExecutor
from core.my_class import Plugin


class Scan(Plugin):
    def __init__(self):
        super().__init__()
        self.name = 'python_frame'
        self.type = 'web'
        self.time = '2022-02-02'
        self.author = 'beginner'

    def check(self, headers, html):
        try:
            flag = False
            for key, value in headers.items():
                flag |= search("flask", value) is not None
                if flag:
                    return "flask_python"
                flag |= search("wsgiserver/", value) is not None
                flag |= search("python/", value) is not None
                flag |= search("csrftoken=", value) is not None
                if flag:
                    return "django_python"
                flag |= search("web2py", value) is not None
                if flag:
                    return "web2py_python"
            flag |= search(r"<div id=\"serendipityLeftSideBar\">", html) is not None
            if flag:
                return "web2py_python"
            return flag
        except Exception:
            return False

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
            print('python_frame')
