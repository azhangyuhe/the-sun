import dns.resolver
from core.my_class import Plugin
from tld import get_fld


class Scan(Plugin):
    def __init__(self):
        super().__init__()
        self.name = 'dns'
        self.type = 'web'
        self.time = '2022-02-02'
        self.author = 'beginner'

    def scan(self, scanner):

        try:
            A = dns.resolver.query(scanner.domain, 'A')
            for i in A.response.answer:
                for j in i.items:
                    if j.rdtype == 1:
                        scanner.DNS['A'] += f'{j.address};'
                    else:
                        pass
        except Exception as error:
            pass

        try:
            main_domain = get_fld(f'http://{scanner.domain}')
            ns = dns.resolver.query(main_domain, 'NS')
            for i in ns.response.answer:
                for j in i.items:
                    scanner.DNS['NS'] += f'{j.to_text()};'
        except Exception as error:
            pass

        try:
            main_domain = get_fld(f'http://{scanner.domain}')
            MX = dns.resolver.query(main_domain, 'MX')
            for i in MX:
                scanner.DNS['MX'] += f'{i.preference}_{i.exchange};'
        except Exception as error:
            pass

        try:
            cname = dns.resolver.query(scanner.domain, 'CNAME')
            for i in cname.response.answer:
                for j in i.items:
                    scanner.DNS['CNAME'] += f'{j.to_text()};'
        except Exception as error:
            pass
