import os

db_pg = {
    "host": "192.168.31.110",
    "port": 5433, # alpha-pg 
    "user": "postgres",
    "password": "postgres",
    "db": "k_house",
}

db_mysql = {
    "host": "192.168.1.100",
    "port": 3306, # alpha-pg 
    "user": "postgres",
    "password": "postgres",
    "db": "k_house",
}

# 使用环境变量获得数据库。兼容开发模式可docker模式。
mysql_host = os.environ.get('MYSQL_HOST') if (os.environ.get('MYSQL_HOST') != None) else "mysqldb"
mysql_user = os.environ.get('MYSQL_USER') if (os.environ.get('MYSQL_USER') != None) else "root"
mysql_pwd = os.environ.get('MYSQL_PWD') if (os.environ.get('MYSQL_PWD') != None) else "mysqldb"
mysql_db = os.environ.get('MYSQL_DB') if (os.environ.get('MYSQL_DB') != None) else "stock_data"

db_mysql["host"] = mysql_host;
db_mysql["port"] = 3306;
db_mysql["user"] = mysql_user;
db_mysql["password"] = mysql_pwd;
db_mysql["db"] = mysql_db;

def get_url_pg(
    dbname = db_pg["db"],
    host = db_pg["host"],
    port = db_pg["port"], 
    user = db_pg["user"],
    password = db_pg["password"],
):
   return f'postgresql://{user}:{password}@{host}:{port}/{dbname}'


def get_url_mysql(
    dbname = db_mysql["db"],
    host = db_mysql["host"],
    port = db_mysql["port"], 
    user = db_mysql["user"],
    password = db_mysql["password"],
):
   return f"mysql+mysqldb://{user}:{password}@{host}:{port}/{dbname}?charset=utf8mb4"