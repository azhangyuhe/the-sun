import json

import requests
from tqdm import tqdm
from elasticsearch import helpers
from elasticsearch import Elasticsearch
from scan_setting import ES_IP, ES_PORT
from core.Global import LOGGER


def elasticsearch_test():
    try:
        response = requests.get(url=f'http://{ES_IP}:{ES_PORT}')
        if response.status_code == 200:
            return True
    except requests.exceptions.ConnectionError:
        return False
    except Exception as e:
        LOGGER.warning(e)
        return False

def esConnect():
    # 连接ES，创建索引
    es = Elasticsearch(
        [f'{ES_IP}:{ES_PORT}'],
        sniff_on_connection_fail=True,
        sniffer_timeout=60
    )
    return es


def getDate(path):
    # 将数据从文件读出
    words = []
    with open(path, "r", encoding="utf-8") as fp:
        for t in fp.readlines():
            tmp = []
            t = json.loads(t)
            for key, value in t['port'].items():
                value['port'] = key
                tmp.append(value)
            t['port'] = tmp
            words.append(json.dumps(t, ensure_ascii=False))
    return words


def insert_es(path, my_index, one_bulk):
    es = esConnect()
    words = getDate(path)
    # 插入数据 one_bulk表示一个bulk里装多少个
    body = []
    body_count = 0  # 记录body里面有多少个.
    # 最后一个bulk可能没满one_bulk,但也要插入

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
            helpers.bulk(es, body)  # 用bulk批量存储
            pbar.update(one_bulk)
            body_count = 0
            body = []
            body.append(every_body)
            body_count += 1

    if len(body) > 0:
        # 如果body里面还有，则再插入一次（最后非整块的）
        helpers.bulk(es, body)

    pbar.close()
    print("插入数据完成!")


def ip_search(es, domain_name, my_index):
    """

    :param es:
    :param domain_name:
    :param my_index:
    :return:
    """
    # 根据keywords1来查找，倒排索引
    my_search1 = \
        {
            "query": {
                "match": {
                    "whois.domain_name": domain_name
                }
            }
        }

    # helpers查询
    es_result = helpers.scan(
        client=es,
        query=my_search1,
        scroll='10m',
        index=my_index,
        timeout='10m'
    )
    es_result = [item for item in es_result]  # 原始是生成器<generator object scan at 0x0000022E384697D8>
    # print(es_result) # 可以直接打印查看
    search_res = []
    for item in es_result:
        tmp = item['_source']
        # search_res.append((tmp['ip'], tmp['ip_location'], tmp['os'],tmp['ip_type']))
        # 可指定显示查询后结果信息
        print("查询出数据内容如下：" + str(tmp))
    print("共查询到%d条数据" % len(es_result))


def domain_search(es, ip, port, banner, server, issues, web_server, my_index):
    # 根据keywords1来查找，倒排索引
    my_search1 = \
        {
            "query": {
                "bool": {
                    "must": [
                        {
                            "nested": {
                                "path": "port_list",
                                "query": {
                                    "bool": {
                                        "should": [
                                            {
                                                "match": {
                                                    "ip": ip
                                                }
                                            },
                                            {
                                                "match": {
                                                    "port_list.port": port
                                                }
                                            },
                                            {
                                                "match": {
                                                    "port_list.server": server
                                                }
                                            },
                                            {
                                                "match": {
                                                    "port_list.web.banner": banner
                                                }
                                            },
                                            {
                                                "match": {
                                                    "port_list.web.issues": issues
                                                }
                                            },
                                            {
                                                "match": {
                                                    "port_list.web.headers.Server": web_server
                                                }
                                            }
                                        ]
                                    }
                                }
                            }
                        }
                    ]
                }
            }
        }

    # helpers查询
    es_result = helpers.scan(
        client=es,
        query=my_search1,
        scroll='10m',
        index=my_index,
        timeout='10m'
    )
    es_result = [item for item in es_result]  # 原始是生成器<generator object scan at 0x0000022E384697D8>
    # print(es_result) # 可以直接打印查看
    # search_res = []
    for item in es_result:
        tmp = item['_source']
        # search_res.append((tmp['ip'], tmp['ip_location'], tmp['os'],tmp['ip_type']))
        # 可指定显示查询后结果信息
        print("查询出数据内容如下：" + str(tmp))
    print("共查询到%d条数据" % len(es_result))
