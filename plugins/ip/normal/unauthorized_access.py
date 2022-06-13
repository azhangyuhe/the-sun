# 作者：博客园_杠上花
# 邮箱: a2578629964@163.com
# 时间：2022年1月20日
# 编码：utf-8
# 版本：python3.8
import os
import socket
import requests
from pymongo import MongoClient
from kazoo.client import KazooClient

from core.my_class import Plugin, IpScanner


def elasticsearch_access(target_ip: str, port: int):
    """
    Elasticsearch的增删改查操作全部由http接口完成。
    由于Elasticsearch授权模块需要付费，所以免费开源的Elasticsearch可能存在未授权访问漏洞。
    攻击者可以拥有Elasticsearch的所有权限。可以对数据进行任意操作。

    :param target_ip:
    :param port:
    :return:
    """
    try:
        response = requests.get(url=f"http://{target_ip}:{port}/_nodes")
        if "_nodes" in response.content.decode():
            return True
        return False
    except requests.exceptions.ConnectionError:
        return False
    except Exception as error:
        return False


def docker_access(target_ip: str, port: int):
    """
    Docker 未授权访问漏洞
    Docker Remote API 是一个取代远程命令行界面（rcli）的REST API。
    通过 docker client 或者 http 直接请求就可以访问这个 API,可以做任何docker能够做的东西,
    增删容器,利用数据卷读写主机内容

    :param target_ip:
    :param port:
    :return:
    """

    try:
        response = requests.get(url=f"http://{target_ip}:{port}/version")
        if "Components" in response.content.decode():
            return True
        return False
    except requests.exceptions.ConnectionError:
        return False
    except Exception as error:
        return False


def mongodb_access(target_ip: str, port: int):
    """
    MongoDB服务安装后，默认未开启权限验证。如果服务监听在0.0.0.0，则可远程无需授权访问数据库

    mongod
    :param target_ip:
    :param port:
    :return:
    """

    # 建立Mongodb数据库连接
    try:
        client = MongoClient(host=target_ip, port=port)
        if client.list_database_names():
            return True
        return False
    except Exception as error:
        return False


def memcached_access(target_ip: str, port: int):
    """
    由于 Memcached 的安全设计缺陷没有权限控制模块，
    所以对公网开放的Memcache服务很容易被攻击者扫描发现，
    攻击者无需认证通过命令交互可直接读取 Memcached中的敏感信息。
    memcache

    :param target_ip:
    :param port:
    :return:
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((target_ip, port))
        s.send("stats\r\n".encode())
        result = s.recv(1024)
        if "version" in result.decode():
            return True
        return False
    except Exception as error:
        return False


def zookeeper_access(target_ip: str, port: int):
    """
    Zookeeper安装部署之后默认情况下不需要任何身份验证，造成攻击者可以远程利用Zookeeper，
    通过服务器收集敏感信息或者在Zookeeper集群内进行破坏（比如：kill命令）。
    攻击者能够执行所有只允许由管理员运行的命令。

     2181
    :param target_ip:
    :param port:
    :return:
    """
    try:
        zk = KazooClient(hosts=f"{target_ip}:{port}")  # 如果是本地那就写127.0.0.1
        zk.start(timeout=4)  # 与zookeeper连接
        return True
    except Exception as error:
        return False


def redis_access(target_ip: str, port: int):
    """
    漏洞危害:
     （1）攻击者无需认证访问到内部数据，可能导致敏感信息泄露，黑客也可以恶意执行flushall来清空所有数据；
     （2）攻击者可通过EVAL执行lua代码，或通过数据备份功能往磁盘写入后门文件(webshell)；
     （3）最严重的情况，如果Redis以root身份运行，黑客可以给root账户写入SSH公钥文件，直接通过SSH登录受害服务器

    :param target_ip:
    :param port:
    :return:
    """
    poc = "\x2a\x31\x0d\x0a\x24\x34\x0d\x0a\x69\x6e\x66\x6f\x0d\x0a"
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((target_ip, port))  # 连接
        sock.send(poc.encode())  # 发送info命令
        response = sock.recv(1024).decode()  # 接收响应数据
        if "redis_version" in response:
            return True
        else:
            return False
    except Exception as error:
        return False


def rsync_access(target_ip: str, port: int):
    """
    rsync
    :param target_ip:
    :param port:
    :return:
    """
    try:

        result = os.popen(f"rsync rsync://{target_ip}:{port}/src").read()
        if "etc" in result:
            return True
        return False
    except requests.exceptions.ConnectionError:
        return False
    except Exception as error:
        return False


def couchdb_access(target_ip: str, port: int):
    """
    默认会在5984端口开放Restful的API接口，如果使用SSL的话就会监听在6984端口，
    用于数据库的管理功能。其HTTP Server默认开启时没有进行验证，而且绑定在0.0.0.0，
    所有用户均可通过API访问导致未授权访问。
    couchdb

    :param target_ip:
    :param port:
    :return:
    """
    try:
        response = requests.get(url=f"http://{target_ip}:{port}/_config")
        if "couch_mrview_http" in response.content.decode():
            return True
        return False
    except requests.exceptions.ConnectionError:
        return False
    except Exception as error:
        return False


def hadoop_access(target_ip: str, port: int):
    try:
        response = requests.get(url=f"http://{target_ip}:{port}/cluster")
        if "Cluster Nodes Metrics" in response.content.decode():
            return True
        return False
    except requests.exceptions.ConnectionError:
        return False
    except Exception as error:
        return False


def jupyterNotebook_access(target_ip: str, port: int):
    """
    如果管理员未为Jupyter Notebook配置密码，将导致未授权访问漏洞，
    游客可在其中创建一个console并执行任意Python代码和命令。

    8888
    :param target_ip:
    :param port:
    :return:
    """
    try:
        response = requests.get(url=f"http://{target_ip}:{port}")
        if "Select items to perform actions on them." in response.content.decode():
            return True
        return False
    except requests.exceptions.ConnectionError:
        return False
    except Exception as error:
        return False


class Scan(Plugin):
    def __init__(self):
        super().__init__()
        self.name = 'unauthorized_access'
        self.type = 'ip'
        self.time = '2022-02-02'
        self.author = 'beginner'

    def scan(self, scanner: IpScanner):
        try:
            for port in scanner.port:
                if scanner.port[port]["server"] == "redis":
                    if redis_access(scanner.ipv4, port):
                        scanner.port[port]["leak"].append(
                            {"name": 'Unauthorized access vulnerability', 'more_info': {'payload': '', 'content': ''}})
                elif scanner.port[port]["server"] == "mongodb":
                    if mongodb_access(scanner.ipv4, port):
                        scanner.port[port]["leak"].append(
                            {"name": 'Unauthorized access vulnerability', 'more_info': {'payload': '', 'content': ''}})
                elif scanner.port[port]["server"] == "memcached":
                    if memcached_access(scanner.ipv4, port):
                        scanner.port[port]["leak"].append(
                            {"name": 'Unauthorized access vulnerability', 'more_info': {'payload': '', 'content': ''}})
                elif scanner.port[port]["server"] == "rsync":
                    if rsync_access(scanner.ipv4, port):
                        scanner.port[port]["leak"].append(
                            {"name": 'Unauthorized access vulnerability', 'more_info': {'payload': '', 'content': ''}})
                elif scanner.port[port]["server"] == "couchdb":
                    if couchdb_access(scanner.ipv4, port):
                        scanner.port[port]["leak"].append(
                            {"name": 'Unauthorized access vulnerability', 'more_info': {'payload': '', 'content': ''}})
                elif port == 9200:
                    if elasticsearch_access(scanner.ipv4, port):
                        scanner.port[port]["leak"].append(
                            {"name": 'Unauthorized access vulnerability', 'more_info': {'payload': '', 'content': ''}})
                elif port == 2375:
                    if docker_access(scanner.ipv4, port):
                        scanner.port[port]["leak"].append(
                            {"name": 'Unauthorized access vulnerability', 'more_info': {'payload': '', 'content': ''}})
                elif port == 2181:
                    if zookeeper_access(scanner.ipv4, port):
                        scanner.port[port]["leak"].append(
                            {"name": 'Unauthorized access vulnerability', 'more_info': {'payload': '', 'content': ''}})
                elif port == 8088:
                    if hadoop_access(scanner.ipv4, port):
                        scanner.port[port]["leak"].append(
                            {"name": 'Unauthorized access vulnerability', 'more_info': {'payload': '', 'content': ''}})
                elif port == 8888:
                    if jupyterNotebook_access(scanner.ipv4, port):
                        scanner.port[port]["leak"].append(
                            {"name": 'Unauthorized access vulnerability', 'more_info': {'payload': '', 'content': ''}})
                else:
                    pass
        except Exception as error:
            print(error)
