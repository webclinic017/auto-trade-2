#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

# apk add py-pgdb or

import platform
import datetime
import time
import sys
import os
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from sqlalchemy import create_engine
from sqlalchemy.types import NVARCHAR
from sqlalchemy import inspect
import pandas as pd
import traceback
import akshare as ak
import config 

# 使用环境变量获得数据库。兼容开发模式可docker模式。
pg_host = config.db_pg["host"]
pg_port = config.db_pg["port"]
pg_user = config.db_pg["user"]
pg_pwd = config.db_pg["password"]
pg_db = config.db_pg["db"]

print("pg_host :", pg_host, ",pg_user :", pg_user, ",pg_db :", pg_db)
url_pg = config.get_url_pg()
# print("url_pg :", url_pg)

__version__ = "2.0.0"
# 每次发布时候更新。

def engine(url_db = url_pg):
    engine = create_engine(
        url_db,
        encoding='utf8', convert_unicode=True)
    return engine

def engine_to_db(dbname):
    url  = config.get_url_pg(dbname = dbname)
    engine = create_engine(
        url,
        encoding='utf8', convert_unicode=True)
    return engine

def creat_conn_no_db(
    host = config.db_pg["host"],
    port = config.db_pg["port"], 
    user = config.db_pg["user"],
    password = config.db_pg["password"],
 ):
    try:
        conn = psycopg2.connect(f"host = localhost port = {port} password= {password} user={user}")  
        # curs  = conn.cursor()
            
        # engine = create_engine(f'postgresql://{user}:{password}@localhost:{port}/') 
    except:
        try:
            conn = psycopg2.connect(f"host = {host} port = {port} password= {password} user={user}")  
            # curs  = conn.cursor()
        except:       
            print('数据库连接创建失败')
    return conn

def create_db(dbname,
              conn, 
              curs):
    """
    目标：在PostgreSQL服务器中，创建指定的数据库
    
    参数：dbname，str，创建的数据库的名称；
             conn，           PostgreSQL服务器连接，由包 psycopg2 生成；
             curs，            PostgreSQL服务器连接的游标，与conn相对应；
    
    返回值：None
    """

    # 设置数据库连接状态，创建数据库时，需要用到
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

    # 先删除该数据库，以确保代码可重复执行（这是确保代码可重复执行的常用策略）
    try:
        curs.execute("DROP DATABASE {} ;".format(dbname))
        conn.commit()
    except: 
        conn.rollback()
    
    # 创建数据库
    try:
        curs.execute("CREATE DATABASE {};".format(dbname))
        conn.commit()
        print("{} 数据库创建成功".format(dbname))
    except Exception as e:
        print(e)
        conn.rollback()
        
    return None

def creat_conn_with_pg(
    dbname = config.db_pg["db"],
    host = config.db_pg["host"],
    port = config.db_pg["port"], 
    user = config.db_pg["user"],
    password = config.db_pg["password"],
 ):
    try:
        conn = psycopg2.connect(f"host = localhost port = {port} password= {password} dbname={dbname}  user={user}")  
        curs  = conn.cursor()
            
        engine = create_engine(f'postgresql://{user}:{password}@localhost:{port}/{dbname}') 
        
    except:
        try:
            conn = psycopg2.connect(f"host = {host} port = {port} password= {password} dbname={dbname}  user={user}")  
            curs  = conn.cursor()

            engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{dbname}')
        except:       
            print('数据库连接创建失败')
            
    return conn, curs, engine

def gen_multi_s_tuple(length):
    """
    目标：    生成一个由 %s 构成的元组，以供 SQL 语句所用；
    参数：    length，int, 元组中元素的个数
    返回值：形如（%s，%s）的元组
    """
    
    multi_s = ','.join(['%s',]*length)
    multi_s = '(' + multi_s + ')'
    
    return multi_s  

# 通过数据库链接 engine。
def curs(
    dbname = config.db_pg["db"],
    host = config.db_pg["host"],
    port = config.db_pg["port"], 
    user = config.db_pg["user"],
    password = config.db_pg["password"],
):
    try:
        conn = psycopg2.connect(f"host = {host} port = {port} password= {password} dbname={dbname}  user={user}")  
        curs  = conn.cursor()

        # engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{dbname}')
    except Exception as e:    
        print('数据库连接创建失败',e)
    conn.autocommit(on=True)
    return curs


# 定义通用方法函数，插入数据库表，并创建数据库主键，保证重跑数据的时候索引唯一。
def insert_db(data, table_name, write_index, primary_keys):
    # 插入默认的数据库。
    insert_other_db(pg_db, data, table_name, write_index, primary_keys)


# 增加一个插入到其他数据库的方法。
def insert_other_db(dbname, data, table_name, write_index, primary_keys):
    # 定义engine
    engine_pg = engine_to_db(dbname)
    # 使用 http://docs.sqlalchemy.org/en/latest/core/reflection.html
    # 使用检查检查数据库表是否有主键。
    insp = inspect(engine_pg)
    col_name_list = data.columns.tolist()
    # 如果有索引，把索引增加到varchar上面。
    if write_index:
        # 插入到第一个位置：
        col_name_list.insert(0, data.index.name)
    print(col_name_list)
    data.to_sql(name=table_name, con=engine_pg, schema=dbname, if_exists='append',
                dtype={col_name: NVARCHAR(length=255) for col_name in col_name_list}, index=write_index)

    # print(insp.get_pk_constraint(table_name))
    # print()
    # print(type(insp))
    # 判断是否存在主键
    if insp.get_pk_constraint(table_name)['constrained_columns'] == []:
        with engine_pg.connect() as con:
            # 执行数据库插入数据。
            try:
                con.execute('ALTER TABLE `%s` ADD PRIMARY KEY (%s);' % (table_name, primary_keys))
            except  Exception as e:
                print("################## ADD PRIMARY KEY ERROR :", e)




# 插入数据。
def insert(sql, params=()):
    with curs() as db_curs:
        print("insert sql:" + sql)
        try:
            db_curs.execute(sql, params)
        except  Exception as e:
            print("error :", e)


# 查询数据
def select(sql, params=()):
    with curs() as db_curs:
        print("select sql:" + sql)
        try:
            db_curs.execute(sql, params)
        except  Exception as e:
            print("error :", e)
        result = db_curs.fetchall()
        return result


# 计算数量
def select_count(sql, params=()):
    with curs() as db_curs:
        print("select sql:" + sql)
        try:
            db_curs.execute(sql, params)
        except  Exception as e:
            print("error :", e)
        result = db_curs.fetchall()
        # 只有一个数组中的第一个数据
        if len(result) == 1:
            return int(result[0][0])
        else:
            return 0


# 通用函数。获得日期参数。
def run_with_args(run_fun):
    tmp_datetime_show = datetime.datetime.now()  # 修改成默认是当日执行 + datetime.timedelta()
    tmp_hour_int = int(tmp_datetime_show.strftime("%H"))
    if tmp_hour_int < 12 :
        # 判断如果是每天 中午 12 点之前运行，跑昨天的数据。
        tmp_datetime_show = (tmp_datetime_show + datetime.timedelta(days=-1))
    tmp_datetime_str = tmp_datetime_show.strftime("%Y-%m-%d %H:%M:%S.%f")
    print("\n######################### hour_int %d " % tmp_hour_int)
    str_db = "pg_host :" + pg_host + ", pg_user :" + pg_user + ", pg_db :" + pg_db
    print("\n######################### " + str_db + "  ######################### ")
    print("\n######################### begin run %s %s  #########################" % (run_fun, tmp_datetime_str))
    start = time.time()
    # 要支持数据重跑机制，将日期传入。循环次数
    if len(sys.argv) == 3:
        # python xxx.py 2017-07-01 10
        tmp_year, tmp_month, tmp_day = sys.argv[1].split("-")
        loop = int(sys.argv[2])
        tmp_datetime = datetime.datetime(int(tmp_year), int(tmp_month), int(tmp_day))
        for i in range(0, loop):
            # 循环插入多次数据，重复跑历史数据使用。
            # time.sleep(5)
            tmp_datetime_new = tmp_datetime + datetime.timedelta(days=i)
            try:
                run_fun(tmp_datetime_new)
            except Exception as e:
                print("error :", e)
                traceback.print_exc()
    elif len(sys.argv) == 2:
        # python xxx.py 2017-07-01
        tmp_year, tmp_month, tmp_day = sys.argv[1].split("-")
        tmp_datetime = datetime.datetime(int(tmp_year), int(tmp_month), int(tmp_day))
        try:
            run_fun(tmp_datetime)
        except Exception as e:
            print("error :", e)
            traceback.print_exc()
    else:
        # tmp_datetime = datetime.datetime.now() + datetime.timedelta(days=-1)
        try:
            run_fun(tmp_datetime_show)  # 使用当前时间
        except Exception as e:
            print("error :", e)
            traceback.print_exc()
    print("######################### finish %s , use time: %s #########################" % (
        tmp_datetime_str, time.time() - start))


# 设置基础目录，每次加载使用。
bash_stock_tmp = "./data/cache/hist_data_cache/%s/%s/"
def mkdir_for_bash_stock_tmp():
    if not os.path.exists(bash_stock_tmp):
        os.makedirs(bash_stock_tmp)  # 创建多个文件夹结构。
        print("######################### init tmp dir #########################")
# mkdir_for_bash_stock_tmp()

# 增加读取股票缓存方法。加快处理速度。
def get_hist_data_cache(code, date_start, date_end):
    cache_dir = bash_stock_tmp % (date_end[0:7], date_end)
    # 如果没有文件夹创建一个。月文件夹和日文件夹。方便删除。
    # print("cache_dir:", cache_dir)
    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir)
    cache_file = cache_dir + "%s^%s.gzip.pickle" % (date_end, code)
    # 如果缓存存在就直接返回缓存数据。压缩方式。
    if os.path.isfile(cache_file):
        print("######### read from cache #########", cache_file)
        return pd.read_pickle(cache_file, compression="gzip")
    else:
        print("######### get data, write cache #########", code, date_start, date_end)
        stock = ak.stock_zh_a_hist(symbol= code, start_date=date_start, end_date=date_end, adjust="")
        stock.columns = ['date', 'open', 'close', 'high', 'low', 'volume', 'amount', 'amplitude', 'quote_change',
                         'ups_downs', 'turnover']
        if stock is None:
            return None
        stock = stock.sort_index(0)  # 将数据按照日期排序下。
        print(stock)
        stock.to_pickle(cache_file, compression="gzip")
        return stock
