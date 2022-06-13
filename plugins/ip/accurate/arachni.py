# 作者：博客园_杠上花
# 邮箱: a2578629964@163.com
# 时间：2022年1月20日
# 编码：utf-8
# 版本：python3.8
import json
import time
import requests
from core.Global import LOGGER
from core.my_class import Plugin, IpScanner
from scan_setting import PAGE_LIST
from scan_setting import ARACHNI_IP
from scan_setting import ARACHNI_PORT


class Arachni:
    def __init__(self, ip, port, auth):
        self.ip = ip
        self.port = port
        self.auth = auth

    def test_connect(self):
        response = requests.get(url=f'http://{self.ip}:{self.port}', auth=self.auth)
        if response.status_code == 404:
            if 'Try this' in response.content.decode():
                return True
            else:
                return False
        else:
            return False

    def add_scan(self, target_url):
        options = json.dumps({'url': f'{target_url}', "checks": ['*'],
                              'scope': {'page_limit': PAGE_LIST},
                              'audit': {'elements': ['link', 'form', 'cookie']},
                              'http': {
                                  'user_agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:96.0) Gecko/20100101 Firefox/96.0'}
                              })
        response = requests.post(url=f'http://{self.ip}:{self.port}/scans', data=options, auth=self.auth)
        if response.status_code == 200:
            json_data = json.loads(response.content.decode())
            return json_data.get('id')
        else:
            return False

    def get_all_id(self):
        response = requests.get(url=f'http://{self.ip}:{self.port}/scans', auth=self.auth)
        if response.status_code == 200:
            id_dic = json.loads(response.content.decode())
            return [i for i in id_dic]

    def get_status(self, scan_id):
        response = requests.get(url=f'http://{self.ip}:{self.port}/scans/{scan_id}/summary', auth=self.auth)
        if response.status_code == 200:
            result = json.loads(response.content.decode())
            return result.get('status')
        else:
            return False

    def get_issues(self, scan_id):
        response = requests.get(url=f'http://{self.ip}:{self.port}/scans/{scan_id}/report.json', auth=self.auth)
        scan_result = json.loads(response.content.decode())
        if tmp := scan_result.get('issues', ''):
            issue = [i.get('name', '') for i in tmp]
            return issue
        else:
            return False

    def delete_task(self, scan_id):
        response = requests.delete(url=f'http://{self.ip}:{self.port}/scans/{scan_id}', auth=self.auth)
        if response.status_code == 200:
            return True
        else:
            return False


class Scan(Plugin):
    def __init__(self):
        super().__init__()
        self.name = 'unauthorized_access'
        self.type = 'ip'
        self.time = '2022-02-02'
        self.author = 'beginner'

    def scan(self, scanner: IpScanner):
        for port in scanner.port:
            if scanner.port[port]['server'] in ['http', 'https']:
                arachni = Arachni(ip='127.0.0.1', port=7331, auth=('arachni', 'cuitscan'))
                if scan_id := arachni.add_scan(target_url=f'http://{scanner.ipv4}:{port}'):
                    print(scan_id)
                    if arachni.get_status(scan_id):
                        while status := arachni.get_status(scan_id):
                            if status == 'done':
                                scanner.port[port]['http']['arachni'] = arachni.get_issues(scan_id)
                                arachni.delete_task(scan_id)
                                break
                            time.sleep(3)
                    else:
                        LOGGER.warning('status error')
                else:
                    LOGGER.warning('scan id error')


def arachni_test():
    try:
        time.sleep(5)
        response = requests.get(url=f'http://{ARACHNI_IP}:{ARACHNI_PORT}')
        if response.status_code == 404 and ('Sinatra' in response.content.decode()):
            return True
        return False
    except requests.exceptions.ConnectionError:
        return False
    except Exception as e:
        LOGGER.warning(e)
        return False
