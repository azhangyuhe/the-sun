from elasticsearch import Elasticsearch


def es_connect():
    es = Elasticsearch(
        ['114.116.11.72:60000'],
        sniff_on_connection_fail=True,
        http_auth=('elastic', 'ab5f15g6113*A0C5#'),
        sniffer_timeout=60
    )
    return es


def createES(ip_index, domain_index):
    # ip和domain数据库索引设计模板
    ip_request_body = {
        "settings": {
            "number_of_shards": 5,
            "number_of_replicas": 1
        },
        "mappings": {
            "properties": {
                "scan_time": {
                    "type": "text"
                },
                "domain": {
                    "type": "text"
                },
                "ipv4": {
                    "type": "text"
                },
                "ipv6": {
                    "type": "text"
                },
                "mac": {
                    "type": "text"
                },
                "ip_location": {
                    "type": "text"
                },
                "os": {
                    "type": "text"
                },
                "port": {
                    "type": "nested",
                    "properties": {
                        "port": {
                            "type": "text"
                        },
                        "server": {
                            "type": "text"
                        },
                        "version": {
                            "type": "text"
                        },
                        "banner": {
                            "type": "text"
                        },
                        "leak": {
                            "type": "nested",
                            "properties": {
                                "name": {
                                    "type": "text"
                                },
                                "more_info": {
                                    "properties": {
                                        "payload": {
                                            "type": "text"
                                        },
                                        "content": {
                                            "type": "text"
                                        }
                                    }
                                }
                            }
                        },
                        "http": {
                            "properties": {
                                "title": {
                                    "type": "text"
                                },
                                "status_code": {
                                    "type": "text"
                                },
                                "web_finger": {
                                    "type": "text"
                                },
                                "arachni": {
                                    "type": "text"
                                }
                            }}
                    }
                }}
        }
    }
    domain_request_body = {
        "settings": {
            "number_of_shards": 5,
            "number_of_replicas": 1
        },
        "mappings": {
            "properties": {
                "website_page": {
                    "type": "nested",
                    "properties": {
                        "status_code": {
                            "type": "integer"
                        },
                        "response_headers": {
                            "properties": {
                                "Date": {
                                    "type": "text"
                                },
                                "Server": {
                                    "type": "text"
                                },
                                "X-Frame-Options": {
                                    "type": "text"
                                },
                                "Last-Modified": {
                                    "type": "text"
                                },
                                "Accept-Ranges": {
                                    "type": "text"
                                },
                                "Cache-Control": {
                                    "type": "text"
                                },
                                "Expires": {
                                    "type": "text"
                                },
                                "Vary": {
                                    "type": "text"
                                },
                                "Content-Encoding": {
                                    "type": "text"
                                },
                                "ETag": {
                                    "type": "text"
                                },
                                "Content-Length": {
                                    "type": "text"
                                },
                                "Keep-Alive": {
                                    "type": "text"
                                },
                                "Connection": {
                                    "type": "text"
                                },
                                "Content-Type": {
                                    "type": "text"
                                },
                                "Content-Language": {
                                    "type": "text"
                                }
                            }},
                        "title": {
                            "type": "text"
                        },
                        "url": {
                            "type": "text"
                        },
                        "method": {
                            "type": "text"
                        },
                        "banner": {
                            "type": "text"
                        }
                    }
                },
                "all_banner": {
                    "type": "text"
                },
                "scheme": {
                    "type": "text"
                },
                "domain": {
                    "type": "text"
                },
                "robots": {
                    "type": "text"
                },
                "real_ip": {
                    "type": "text"
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
                        "creation_date": {
                            "type": "text"
                        },
                        "expiration_date": {
                            "type": "text"
                        }
                    }
                },
                "cert": {
                    "properties": {
                        "public_key": {
                            "type": "text"
                        },
                        "cert_version": {
                            "type": "text"
                        },
                        "cert_serial_number": {
                            "type": "text"
                        },
                        "signature_algorithm": {
                            "type": "text"
                        },
                        "is_expire": {
                            "type": "text"
                        },
                        "public_key_len": {
                            "type": "text"
                        },
                        "lssure": {
                            "type": "text"
                        },
                        "ST": {
                            "type": "text"
                        },
                        "L": {
                            "type": "text"
                        },
                        "O": {
                            "type": "text"
                        },
                        "CN": {
                            "type": "text"
                        },
                        "before": {
                            "type": "text"
                        },
                        "after": {
                            "type": "text"
                        }
                    }
                },
                "icp": {
                    "properties": {
                        "Owner": {
                            "type": "text"
                        },
                        "CompanyName": {
                            "type": "text"
                        },
                        "CompanyType": {
                            "type": "text"
                        },
                        "SiteLicense": {
                            "type": "text"
                        },
                        "SiteName": {
                            "type": "text"
                        },
                        "MainPage": {
                            "type": "text"
                        },
                        "VerifyTime": {
                            "type": "text"
                        }
                    }
                },
                "dns": {
                    "properties": {
                        "A": {
                            "type": "text"
                        },
                        "NS": {
                            "type": "text"
                        },
                        "MX": {
                            "type": "text"
                        },
                        "CNAME": {
                            "type": "text"
                        },
                    }
                },
                "frame": {
                    "type": "text"
                },
                "scan_time": {
                    "type": "text"
                },
                "leak": {
                    "properties": {
                        "name": {
                            "type": "text"
                        },
                        "more_info": {
                            "properties": {
                                "payload": {
                                    "type": "text"
                                },
                                "content": {
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
    # judgeIndex(domain_index, domain_request_body)


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
    es = es_connect()
    ip_index = "scan_ip"  # es数据库名 ip部分
    domain_index = "scan_domain"  # es数据库名 domain部分
    createES(ip_index, domain_index)  # 创建两个数据库索引
