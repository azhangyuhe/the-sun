from elasticsearch import Elasticsearch


# from config.es_option import esConnect


def createES(ip_index, domain_index):
    # ip和domain数据库索引设计模板
    ip_request_body = {
        "settings": {
            "number_of_shards": 5,
            "number_of_replicas": 1
        },
        "mappings": {
            "properties": {
                "ip": {
                    "properties": {
                        "ip_location": {
                            "type": "text"
                        },
                        "ip_info": {
                            "properties": {
                                "ipv4": {
                                    "type": "ip"
                                },
                                "os": {
                                    "type": "text"
                                },
                                "ip_type": {
                                    "type": "text"
                                },
                                "mac": {
                                    "type": "text"
                                }
                            }
                        }
                    }
                },
                "port": {
                    "type": "nested",
                    "properties": {
                        "port": {
                            "type": "integer"
                        },
                        "server": {
                            "type": "text"
                        },
                        "version": {
                            "type": "text"
                        },
                        "leak": {
                            "type": "nested",
                            "properties": {
                                "name": {
                                    "type": "text"
                                },
                                "more_info": {
                                    "type": "text"
                                }
                            }},
                        "web": {
                            "properties": {
                                "title": {
                                    "type": "text"
                                },
                                "html": {
                                    "type": "text"
                                },
                                "headers": {
                                    "type": "text"
                                },
                                "banner": {
                                    "type": "text"
                                },
                                "issues": {
                                    "type": "text"
                                }
                            }
                        }
                    }
                }
            }
        }
    }
    domain_request_body = {
        "settings": {
            "number_of_shards": 5,
            "number_of_replicas": 1
        },
        "mappings": {
            "properties": {
                "ip": {
                    "type": "ip"
                },
                "whois": {
                    "properties": {
                        "domain_name": {
                            "type": "text"
                        },
                        "registrar": {
                            "type": "text"
                        },
                        "whois_server": {
                            "type": "text"
                        },
                        "referral_url": {
                            "type": "text"
                        },
                        "updated_date": {
                            "type": "text"
                        },
                        "creation_date": {
                            "type": "text"
                        },
                        "expiration_date": {
                            "type": "text"
                        },
                        "name_servers": {
                            "type": "text"
                        },
                        "emails": {
                            "type": "text"
                        },
                        "dnssec": {
                            "type": "text"
                        },
                        "name": {
                            "type": "text"
                        },
                        "org": {
                            "type": "text"
                        },
                        "address": {
                            "type": "text"
                        },
                        "city": {
                            "type": "text"
                        },
                        "state": {
                            "type": "text"
                        },
                        "zipcode": {
                            "type": "text"
                        },
                        "country": {
                            "type": "text"
                        }
                    }
                },
                "icp": {
                    "properties": {
                        "主办单位名称": {
                            "type": "text"
                        },
                        "主办单位性质": {
                            "type": "text"
                        },
                        "网站名称": {
                            "type": "text"
                        }
                    }
                },
                "banner": {
                    "type": "text"
                },
                "other": {
                    "properties": {
                        "robots.txt": {
                            "properties": {
                                "status_code": {
                                    "type": "integer"
                                },
                                "more_info": {
                                    "type": "text"
                                }
                            }
                        }
                    }
                }
            }
        }
    }

    judgeIndex(ip_index, ip_request_body)
    judgeIndex(domain_index, domain_request_body)


def judgeIndex(index_name, request_body):
    # 先判断索引是否存在，若存在，先删除索引 注意插入时将此部分注释 否则会重建数据库
    if es.indices.exists(index_name):
        es.indices.delete(index=index_name)
    else:
        print('索引不存在，可以创建')
    result = es.indices.create(index=index_name, ignore=400, body=request_body)
    print("创建index成功")
    print(result)  # {'acknowledged': True, 'shards_acknowledged': True, 'index': 'scanner'}


if __name__ == '__main__':
    es = Elasticsearch(
        ['127.0.0.1:9200'],
        sniff_on_connection_fail=True,
        sniffer_timeout=60
    )
    ip_index = "scan_ip"  # es数据库名 ip部分
    domain_index = "scan_domain"  # es数据库名 domain部分
    createES(ip_index, domain_index)  # 创建两个数据库索引
