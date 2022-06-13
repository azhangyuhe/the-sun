# 作者：博客园_杠上花
# 邮箱: a2578629964@163.com
# 时间：2022年1月20日
# 编码：utf-8
# 版本：python3.8
import whois

from core.my_class import Plugin


class Scan(Plugin):
    def __init__(self):
        super().__init__()
        self.name = 'whois'
        self.type = 'web'
        self.time = '2022-02-02'
        self.author = 'beginner'

    def scan(self, scanner):
        try:
            whois_result = whois.whois(scanner.domain)
            scanner.whois['domain_name'] = whois_result.get('domain_name')
            scanner.whois['registrar'] = whois_result.get('registrar')
            scanner.whois['whois_server'] = whois_result.get('whois_server')
            scanner.whois['referral_url'] = whois_result.get('referral_url')
            scanner.whois['name_servers'] = whois_result.get('name_servers')
            scanner.whois['emails'] = whois_result.get('emails')
            scanner.whois['dnssec'] = whois_result.get('dnssec')
            scanner.whois['name'] = whois_result.get('name')
            scanner.whois['org'] = whois_result.get('org')
            scanner.whois['address'] = whois_result.get('address')
            scanner.whois['city'] = whois_result.get('city')
            scanner.whois['state'] = whois_result.get('state')
            scanner.whois['zipcode'] = whois_result.get('zipcode')
            scanner.whois['country'] = whois_result.get('country')
            scanner.whois['creation_date'] = str(whois_result.get('creation_date'))
            scanner.whois['expiration_date'] = str(whois_result.get('expiration_date'))
        except Exception as error:
            pass
