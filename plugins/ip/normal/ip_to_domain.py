import socket
from core.my_class import Plugin, IpScanner


class Scan(Plugin):
    def __init__(self):
        super().__init__()
        self.name = 'ipToDomain'
        self.type = 'web'
        self.time = '2022-02-02'
        self.author = 'beginner'

    def scan(self, scanner: IpScanner):
        try:
            name, alias, _ = socket.gethostbyaddr(scanner.ipv4)
            scanner.domain = name
        except socket.error:
            scanner.domain = ''
