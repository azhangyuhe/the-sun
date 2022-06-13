from core.my_class import Plugin, Scanner


class Scan(Plugin):
    def __init__(self):
        super().__init__()
        self.name = 'unauthorized_access'
        self.type = 'ip'
        self.time = '2022-02-02'
        self.author = 'beginner'
    def scan(self, scanner: Scanner):
        pass