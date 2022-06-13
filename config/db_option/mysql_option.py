import pymysql
from scan_setting import MYSQL_IP, MYSQL_PORT, MYSQL_PASSWD, MYSQL_USER


def create_mysql():
    # 建库和建表
    con = pymysql.connect(host=MYSQL_IP, user=MYSQL_USER, port=MYSQL_PORT,
                          passwd=MYSQL_PASSWD, charset='utf8')
    cur = con.cursor()
    # 开始建库
    cur.execute("create database scan_db1 character set utf8;")
    # 使用库
    cur.execute("use scan_db1;")
    # 建表
    cur.execute(
        "create table scan_record(id integer primary key auto_increment,start_time datetime,end_time datetime,total_tasks integer,success_task integer,fail_task integer)character set utf8;")


def insert_data(data: tuple, table: str):
    option_db = {'scan_record': 'insert into scan_record values(null,"{}","{}",{},{},{})'}
    db = pymysql.connect(host=MYSQL_IP, user=MYSQL_USER, port=MYSQL_PORT,
                         passwd=MYSQL_PASSWD, charset='utf8',write_timeout=60000)
    db.select_db('scan_db1')
    cursor = db.cursor()

    try:
        cursor.execute(option_db[table].format(*data))
        db.commit()
        print('ok')
    except Exception as error:
        print(error)
        db.rollback()
    db.close()


def mysql_test():
    try:
        con = pymysql.connect(host=MYSQL_IP, user=MYSQL_USER, port=MYSQL_PORT,
                              passwd=MYSQL_PASSWD, charset='utf8')
        con.ping()
        return True
    except Exception:
        return False
