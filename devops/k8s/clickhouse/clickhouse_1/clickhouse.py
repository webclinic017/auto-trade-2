"""
推荐运行环境

python 3.8.3
clickhouse_driver==0.2.3
clickhouse_sqlalchemy==0.2.0
sqlalchemy==1.4.32
"""

"""
1.Client
"""
def test_client(
    host="localhost",
    # port=9000,
    port=8123,
    database=None,
    user="default",
    passwrod=""):

    from clickhouse_driver import Client
    
    client = Client(host=host, port=port, database=database,user=user ,password=passwrod)
    sql = 'SHOW TABLES'
    res = client.execute(sql)
    print(res)

"""
2.Client
"""
def test_connect(
    host="localhost",
    # port=9000,
    port=8123,
    database=None,
    user="default",
    passwrod=""):

    from clickhouse_driver import connect

    #账号:密码@主机名:端口号/数据库
    conn = connect(f'clickhouse://{user}:{passwrod}@{host}:{port}/{database}')
    cursor = conn.cursor()
    cursor.execute('SHOW TABLES')

"""
clickhouse_sqlalchemy 连接方式
使用较复杂，推荐使用上述两种，注意使用端口为http端口8123。
"""
def test_3():
    from clickhouse_sqlalchemy import make_session
    from sqlalchemy import create_engine
    import pandas as pd

    conf = {
        "user": "default",
        "password": "",
        "host": "127.0.0.1",
        "port": "8123",
        "database": ""
    }
    
    url = 'clickhouse://{user}:{password}@{host}:{port}/{database}'.format(**conf)
    engine = create_engine(url, pool_size=100, pool_recycle=3600, pool_timeout=20)
    
    sql = 'SHOW TABLES'

    session = make_session(engine)
    cursor = session.execute(sql)
    try:
        fields = cursor._metadata.keys
        df = pd.DataFrame([dict(zip(fields, item)) for item in cursor.fetchall()])
        print(df)
    finally:
        cursor.close()
        session.close()

async def async_ch():
    import asyncio
    from aiochclient import ChClient
    from aiohttp import ClientSession

    async with ClientSession() as s:
        client = ChClient(s, 
            url="http://localhost:8123/",
            user="default",
            password="",
            database="",
        )
        alive = await client.is_alive()
        print(f'client is alive: {alive}')
        sql='INSERT INTO phalgorithom.pipeHeatAnalyse(id, calcTable) values (4,3)'
        await client.execute(sql)

def test_async_ch():
    import asyncio
    asyncio.run(async_ch())

test_3()