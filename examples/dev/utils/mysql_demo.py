import pymysql

"""
pip install pymysql
"""

# 创建数据库链接
conn = pymysql.connect(
    host="ip地址", # 链接数据库的ip
    user="db_username",   # 用户名
    password="db_password",   # 用户密码
    db="db_name",     # 数据库名称
    port=3306,    # 数据库端口号，默认是3306
    charset='utf8',   # 字符集编码
    autocommit=True    # 自动提交
    )
    
# 创建游标
# cursor = conn.cursor()  # 创建普通的游标，返回结果为元组类型
cursor = conn.cursor(pymysql.cursors.DictCursor)    # 指定返回格式为字典

# 数据库操作
cursor.execute("select * from students limit 5;") # 查询数据库中数据
# cursor.execute("insert into students (name,phone,age,sex) values ('lilili','15000000001',18,'女');")  # 往数据库中插入数据
# cursor.execute('update students set name = "小白" where id = 1;')   # 更新数据库中数据 
# cur.execute('delete from students where id=50 ;')  # 删除数据库中数据

print(cursor.description)  # 查看数据库中表的字段信息

# conn.commit() #提交（insert，delect，update都需要提交。如果在创建数据库连接时设置autocommit=True，则不需要使用该语句提交数据库增删改的操作）

# print(cursor.fetchall())  # 获取sql执行的结果，获取表中所有数据，返回数据是二维数组
# print(cursor.fetchone())  # 只获取一条数据,返回数据是一维数组
print(cursor.fetchmany(5))  # 输入几获取几条数据，返回数据是二维数据组

for line in cursor:  # 取表中每行数据
    print(line)

cursor.close()  # 关闭游标
conn.close()    # 关闭数据库链接

# conn.cursor()普通游标返回数据
# ((1, '小黑', '11111111111', 18, '男'), (2, '小白', '11111111112', 18, '男'))
# conn.cursor(pymysql.cursors.DictCursor)指定返回字典的游标返回数据
# [{'id': 1, 'name': '小黑', 'phone': '11111111111', 'age': 18, 'sex': '男'}, {'id': 2, 'name': '小白', 'phone': '11111111112', 'age': 18, 'sex': '男'}]
