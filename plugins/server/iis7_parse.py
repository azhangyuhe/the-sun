from config.auxiliary.encrypt import get_html
from core.my_class import Plugin


class Scan(Plugin):
    def __init__(self):
        super().__init__()
        self.name = 'iis7.0解析漏洞'
        self.type = 'server'
        self.time = '2022-02-02'
        self.author = 'beginner'

    def scan(self, scanner):
        try:
            headers = scanner.headers
            url = f"{scanner.scheme}://{scanner.domain}/"
            payload = url + "robots.txt/.php"
            response = self.my_get(url=payload, headers=headers)
            ContentType = response.headers.get("Content-Type", '')
            if 'html' in ContentType and "allow" in get_html(response):
                scanner.leak.append(
                    {'name': 'iis7.0解析漏洞', 'more_info': {'payload': payload, 'content': ContentType}})
        except Exception as error:
            print(error)
