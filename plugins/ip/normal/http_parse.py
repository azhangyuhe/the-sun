import threading

import requests
from modular import website_fingerprint
from config.auxiliary.encrypt import get_html, get_title
from core.my_class import Plugin, IpScanner


class Scan(Plugin):
    def __init__(self):
        super().__init__()
        self.name = 'http_parse'
        self.type = 'ip'
        self.time = '2022-02-02'
        self.author = 'beginner'

    def get_result(self, scanner: IpScanner, port):
        try:
            response = requests.get(f'http://{scanner.ipv4}:{port}', verify=False, allow_redirects=False)
            html = get_html(response)
            title = get_title(html)
            scanner.port[port]['http']['title'] = title
            scanner.port[port]['http']['status_code'] = response.status_code
            scanner.port[port]['http']['web_finger'] = website_fingerprint.scan(url=f'http://{scanner.ipv4}:{port}',
                                                                                html=html, title=title,
                                                                                headers=response.headers)
        except Exception:
            print('http_parse_get')

    def scan(self, scanner: IpScanner):
        try:
            tmp = []
            for port in scanner.port:
                if scanner.port[port]['server'] == 'http':
                    t = threading.Thread(target=self.get_result, args=(scanner, port,))
                    t.start()
                    tmp.append(t)
            for j in tmp:
                j.join()

        except Exception:
            print('http_parse')
