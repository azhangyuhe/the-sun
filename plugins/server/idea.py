from lxml import etree
from config.auxiliary.encrypt import get_html
from core.my_class import Plugin


class Scan(Plugin):
    def __init__(self):
        super().__init__()
        self.name = 'idea目录解析'
        self.type = 'server'
        self.time = '2022-02-02'
        self.author = 'beginner'

    def scan(self, scanner):
        try:
            headers = scanner.headers
            url = "{}://{}/".format(scanner.scheme, scanner.domain)
            payload = url + ".idea/workspace.xml"
            response = self.my_get(payload, headers)
            html = get_html(response)
            path_lst = []
            if '<component name="' in html:
                root = etree.XML(html)
                for e in root.iter():
                    if e.text and e.text.strip().find('$PROJECT_DIR$') >= 0:
                        path = e.text.strip()
                        path = path[path.find('$PROJECT_DIR$') + 13:]
                        if path not in path_lst:
                            path_lst.append(path)
                    for key in e.attrib:
                        if e.attrib[key].find('$PROJECT_DIR$') >= 0:
                            path = e.attrib[key]
                            path = path[path.find('$PROJECT_DIR$') + 13:]
                            if path and path not in path_lst:
                                path_lst.append(path)
                if path_lst:
                    scanner.leak.append(
                        {'name': 'idea敏感文件发现',
                         'more_info': {'payload': payload, 'content': f"敏感目录列表:{repr(path_lst)}"}})
        except Exception as error:
            print(error)
