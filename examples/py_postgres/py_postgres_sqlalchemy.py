import sqlalchemy

# 1 Install
"""
https://docs.sqlalchemy.org/en/14/core/pooling.html

https://docs.sqlalchemy.org/en/13/

我们需要安装 sqlalchemy library 以及psycopg2.
pip install sqlalchemy
pip install psycopg2

"""

import sqlalchemy
import datetime
def connect(user, password, db, host='localhost', port=5432):
    '''Returns a connection and a metadata object'''
    # We connect with the help of the PostgreSQL URL
    # postgresql://federer:grandestslam@localhost:5432/tennis
    url = 'postgresql://{}:{}@{}:{}/{}'
    url = url.format(user, password, host, port, db)

    # The return value of create_engine() is our connection object
    con = sqlalchemy.create_engine(url, client_encoding='utf8')

    # We then bind the connection to MetaData()
    meta = sqlalchemy.MetaData(bind=con)

    return con, meta


con, meta = connect('postgres', 'postgres', 'postgres')
from sqlalchemy import Table, Column, Integer, String, ForeignKey,TIMESTAMP

slams = Table('slams', meta,
    Column('name', String, primary_key=True),
    Column('country', String)
)

results = Table('results', meta,
    Column('slam', String, ForeignKey('slams.name')),
    Column('year', Integer),
    Column('result', String)
)
# Create the above tables
meta.create_all(con)
for table in meta.tables:
    print(table)
tests = Table('test', meta,
    Column('value', Integer),
    Column('time', TIMESTAMP),
    Column('name', String)
)
# clause = slams.insert().values(name='Wimbledon', country='United Kingdom')

# con.execute(clause)

# clause = slams.insert().values(name='Roland Garros', country='France')
#
# result = con.execute(clause)
#
# print(result.inserted_primary_key)

victories = [
    {'slam': 'Wimbledon', 'year': 2003, 'result': 'W'},
    {'slam': 'Wimbledon', 'year': 2004, 'result': 'W'},
    {'slam': 'Wimbledon', 'year': 2005, 'result': 'W'}
]

for row in con.execute(tests.select()):
    print(row.name)


con.execute(meta.tables['results'].insert(), victories)

# for row in con.execute(results.select()):
#     print(row.year)

rows=list(con.execute(results.select()))
print(rows[0].year)


clause = results.select().where(results.c.year == 2005)
c=con.execute('select max(value) as vv from slams')
names = [row[0] for row in c]
print(list(names))
# cc=results.update().where(results.c.year == 2005).values(year=2008)
# con.execute(cc)
# va=[
#     {'value':11,'time':datetime.datetime.now(),'name':'test'},
#     {'value':11,'time':datetime.datetime.now(),'name':'test1'}
# ]
# ss=tests.insert(values=va)
# con.execute(ss)

# 8 max/min 等
c=con.execute('select max(value) as vv from slams')
names = [row[0] for row in c]
print(list(names))

# 和类之间的映射
# tablepy
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class Address(Base):
    __tablename__ = 'address'
    # Here we define columns for the table address.
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, primary_key=True)
    street_name = Column(String(250))
    street_number = Column(String(250))
    post_code = Column(String(250), nullable=False)
    person_id = Column(Integer, ForeignKey('person.id'))#外键，指明地址与用户的关联关系
class Person(Base):
    __tablename__ = 'person'
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    addressid=relationship(Address,backref='person',uselist=False)#backref使得address也能获得person对象，uselist是一对一


# Create an engine that stores data in the local directory's
# sqlalchemy_example.db file.
engine = create_engine('postgresql://postgres:postgres@localhost:{}/postgres'.format(5432))

# Create all tables in the engine. This is equivalent to "Create Table"
# statements in raw SQL.
Base.metadata.create_all(engine)

# operatedb.py
from sqlalchemy.orm import sessionmaker
# from tablepy import Address, Person ,engine

class operateDb:
    def __init__(self):
        self.DBSession = sessionmaker(bind=engine)
        self.session=self.DBSession()
    def add(self,object):
        self.session.add(object)
        self.session.commit()
    def addmany(self,objectlist):
        self.session.add_all(objectlist)
        self.session.commit()
    def filterone(self,object,filter):
        return self.session.query(object).filter(filter).first()

    def update(self,object,filter,updic):
        self.session.query(object).filter(filter).update(updic)
        self.session.commit()

# demo.py
# from tablepy import Address, Person
# from operatedb import operateDb
from sqlalchemy import text
from sqlalchemy import and_
from sqlalchemy import or_

#添加多个
# per1=Person(name="chen")
# per2=Person(name="xu")
# operateDb().addmany([per1,per2])

# address1=Address(street_name="quanshui",street_number="1",post_code="123",person_id=1)
# address2=Address(street_name="quanshui",street_number="1",post_code="123",person_id=2)
# operateDb().addmany([address1,address2])

#查询地址

address=operateDb().filterone(Address,Address.id==1)
print(address.person.name)

#多条件查询
filter=and_(Address.id==1,Address.street_name=='quanshui')
address=operateDb().filterone(Address,filter=(filter))
print(address.person.name)

#多条件查询与更新

filter=and_(Address.id==1,Address.street_name=='quanshui')
address=operateDb().update(Address,filter=(filter),updic={"street_name":"dalian"})