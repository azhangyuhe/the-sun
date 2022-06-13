# 作者：博客园_杠上花
# 邮箱: a2578629964@163.com
# 时间：2022年1月20日
# 编码：utf-8
# 版本：python3.8
import re
import sqlite3

import urllib3
from modular.Wappalyzer import WebPage, Wappalyzer

urllib3.disable_warnings()


# 数据库查询操作 返回name与key
def check(db_id):
    with sqlite3.connect('data/cms_finger.db') as conn:
        cursor = conn.cursor()
        result = cursor.execute('SELECT name, keys FROM `tide` WHERE id=\'{}\''.format(db_id))
        for row in result:
            return row[0], row[1]


# 返回cms_finger.db的行数
def count():
    with sqlite3.connect('data/cms_finger.db') as conn:
        cursor = conn.cursor()
        result = cursor.execute('SELECT COUNT(id) FROM `tide`')
        for row in result:
            return row[0]


class RequestsScanner:
    def __init__(self, headers, body, title):
        self.headers = str(headers)
        self.body = body
        self.title = title
        self.finger = []

    def check_rule(self, key, header, body, title):
        """指纹识别"""
        try:
            if 'title="' in key:
                # 将标识中的title=的内容去除与title进行比较 符合条件返回True
                if re.findall(r'title="(.*)"', key)[0].lower() in title.lower():
                    return True
            elif 'body="' in key:
                if re.findall(r'body="(.*)"', key)[0] in body: return True
            else:
                if re.findall(r'header="(.*)"', key)[0] in header: return True
        except Exception as e:
            pass

    def handle(self, _id, header, body, title):
        # 取出数据库的key进行匹配
        name, key = check(_id)
        # 因为cms_finger.db收集的信息存在多种不同组合才会有下面的分支
        # 满足一个条件即可的情况 ('Lucene', 'header="Lucene" || title="Lucene"')
        if '||' in key and '&&' not in key and '(' not in key:
            for rule in key.split('||'):
                if self.check_rule(rule, header, body, title):
                    self.finger.append(name)
                    break
        # 只有一个条件的情况
        elif '||' not in key and '&&' not in key and '(' not in key:
            if self.check_rule(key, header, body, title):
                self.finger.append(name)
        # 需要同时满足条件的情况
        elif '&&' in key and '||' not in key and '(' not in key:
            num = 0
            for rule in key.split('&&'):
                if self.check_rule(rule, header, body, title):
                    num += 1
            if num == len(key.split('&&')):
                self.finger.append(name)
        else:
            # 与条件下存在并条件: 1||2||(3&&4)
            if '&&' in re.findall(r'\((.*)\)', key)[0]:
                for rule in key.split('||'):
                    if '&&' in rule:
                        num = 0
                        for _rule in rule.split('&&'):
                            if self.check_rule(_rule, header, body, title):
                                num += 1
                        if num == len(rule.split('&&')):
                            self.finger.append(name)
                            break
                    else:
                        if self.check_rule(rule, header, body, title):
                            self.finger.append(name)
                            break
            else:
                # 并条件下存在与条件： 1&&2&&(3||4)
                num = 0
                for rule in key.split('&&'):
                    if '||' in rule:
                        for _rule in rule.split('||'):
                            if self.check_rule(_rule, title, body, header):
                                num += 1
                                break
                    else:
                        if self.check_rule(rule, title, body, header):
                            num += 1
                if num == len(key.split('&&')):
                    self.finger.append(name)

    def run(self):
        '''
        search the match banner from banner.db
        '''
        try:
            header, body, title = self.headers, self.body, self.title
            for db_id in range(1, int(count())):
                try:
                    self.handle(db_id, header, body, title)
                except Exception as e:
                    pass
        except Exception as e:
            print(e)
        finally:
            return self.finger


def scan(url, html, title, headers):
    cms = RequestsScanner(headers, html, title)
    banner = cms.run()
    wappalyzer = Wappalyzer.latest(technologies_file='data/technologies.json')
    webpage = WebPage.new_from_url(url, html, headers)
    banner.extend(wappalyzer.analyze(webpage))

    return list(set([i.lower() for i in banner]))
