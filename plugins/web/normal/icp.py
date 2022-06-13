# 作者：博客园_杠上花
# 邮箱: a2578629964@163.com
# 时间：2022年1月20日
# 编码：utf-8
# 版本：python3.8
import json
from scan_setting import ICP_API
from lxml import etree
import requests

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
            response = requests.get(
                url=f'https://apidatav2.chinaz.com/single/icp?key={ICP_API}&domain={scanner.domain}')
            tmp = json.loads(response.content.decode())
            if tmp['StateCode'] == 1 and tmp['Reason'] == '成功':
                scanner.icp['Owner'] = tmp['Result'].get('Owner', '')
                scanner.icp['CompanyName'] = tmp['Result'].get('CompanyName', '')
                scanner.icp['CompanyType'] = tmp['Result'].get('CompanyType', '')
                scanner.icp['SiteLicense'] = tmp['Result'].get('SiteLicense', '')
                scanner.icp['SiteName'] = tmp['Result'].get('SiteName', '')
                scanner.icp['MainPage'] = tmp['Result'].get('MainPage', '')
                scanner.icp['VerifyTime'] = tmp['Result'].get('VerifyTime', '')

        except Exception as error:
            print(error)
