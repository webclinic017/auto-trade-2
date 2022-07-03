#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 3 10:18:23 2022

@author: alphazz
"""




from   pandas import DataFrame, Series
import pandas as pd

import gc   # garbage collector

import time

import math

import re

import random



import os

import numpy as np

import shelve


import time


import psycopg2     # 该库用于在 python 中调用 postgreSQL

from sqlalchemy import create_engine      # 用于连 sql 数据库的一个包

from  multiprocessing import Process, Pool      # 用于控制并行执行的包

from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


configs = {
    "host": "192.168.0.2",
    "port": 5151,
    "user": "postgres",
    "password": "even_the_smallest",
}



def creat_conn_with_pg(
    dbname = 'stock_data',
    host = configs["host"],
    port = configs["port"], 
    user = configs["user"],
    password = configs["password"],
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
        
        
        
def gen_multi_s_tuple(length):
    """
    目标：    生成一个由 %s 构成的元组，以供 SQL 语句所用；
    参数：    length，int, 元组中元素的个数
    返回值：形如（%s，%s）的元组
    """
    
    multi_s = ','.join(['%s',]*length)
    multi_s = '(' + multi_s + ')'
    
    return multi_s        
        