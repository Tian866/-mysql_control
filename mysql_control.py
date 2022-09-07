import time
import pymysql
import yaml


def banner():
    print("""
         __  __        ____      _ ____  _
        |  \/  |_   _ / ___|__ _(_) __ )(_)
        | |\/| | | | | |   / _` | |  _ \| |
        | |  | | |_| | |__| (_| | | |_) | |
        |_|  |_|\__, |\____\__,_|_|____/|_|
                |___/
    """)


def read_yaml():
    with open(file='db.yaml', mode='r', encoding='utf-8') as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
    return data['Mysql']  # 返回带有用户名和密码的字典


def conn_db_get_filepath():
    mysql = read_yaml()
    db = pymysql.connect(host=mysql['host'],
                         user=mysql['user'],
                         password=mysql['password'],
                         database=mysql['database'])
    cursor = db.cursor()
    sql = 'SHOW VARIABLES LIKE "general_log%"'
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        general_log = results[0][1]
        general_log_file = results[1][1]
        # 判断日志功能是否打开
        if general_log == "OFF":
            sql = "SET GLOBAL general_log = 'ON'"
            cursor.execute(sql)

    except:
        print("[-] Error: unable to fetch data")
        db.rollback()

    db.close()
    return general_log_file


def follow(f):
    f.seek(0, 2)
    while True:
        line = f.readline()
        if not line:
            time.sleep(0.1)
            continue
        yield line.strip()


def main():
    banner()
    file_path = conn_db_get_filepath()
    f = open(file_path, "r")
    loglines = follow(f)
    for line in loglines:
        print(line)


if __name__ == '__main__':
    main()
