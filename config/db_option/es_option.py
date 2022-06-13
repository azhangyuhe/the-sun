# 作者：博客园_杠上花
# 邮箱: a2578629964@163.com
# 时间：2022年1月20日
# 编码：utf-8
# 版本：python3.8
import json
import requests
from tqdm import tqdm
from elasticsearch import Elasticsearch, helpers
from scan_setting import ES_IP, ES_PORT
from core.Global import LOGGER


def es_connect():
    es = Elasticsearch(
        ['114.116.11.72'],
        http_auth=('', ''),
        port=,
        timeout=,
        max_retries=3,
        retry_on_timeout=True)
    return es


class EsOption:
    def __init__(self, ip, port, ip_index, domain_index):
        self.ip = ip
        self.port = port
        self.ip_index = ip_index
        self.domain_index = domain_index
        self.es = es_connect()

    def insert_es(self, path, my_index, one_bulk):
        self.es = es_connect()
        def get_date():
            with open(path, "r", encoding="utf-8") as fp:
                return [t for t in fp.readlines()]

        words = get_date()
        body = []
        body_count = 0
        print("共需要插入%d条" % len(words))
        pbar = tqdm(total=len(words))
        for i in range(0, len(words)):
            every_body = \
                {
                    "_index": my_index,
                    "_source": words[i]
                }

            if body_count < one_bulk:
                body.append(every_body)
                body_count += 1
            else:
                helpers.bulk(self.es, body)  # 用bulk批量存储
                pbar.update(one_bulk)
                body_count = 0
                body = []
                body.append(every_body)
                body_count += 1

        if len(body) > 0:
            # 如果body里面还有，则再插入一次（最后非整块的）
            helpers.bulk(self.es, body)

        pbar.close()
        print("插入数据完成!")

    def ip_search(self):
        pass

    def domain_search(self, domain_name):
        pass


def elasticsearch_test():
    try:
        es_connect()
        return True
    except requests.exceptions.ConnectionError:
        return False
    except Exception as e:
        LOGGER.warning(e)
        return False



