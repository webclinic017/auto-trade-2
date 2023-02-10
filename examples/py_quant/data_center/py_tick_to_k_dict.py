import clickhouse_driver
import pandas as pd

# 连接 clickhouse 数据库
conn = clickhouse_driver.connect(host='your_host', user='your_user', password='your_password', database='your_database')

# 查询字典数据
query = 'SELECT * FROM dict_table'
df = pd.read_sql(query, con=conn)

# 对查询结果进行处理合成 k 线
df_grouped = df.groupby('code')['price'].agg(['open', 'high', 'low', 'close'])
df_k = df_grouped.resample('1min').agg({'open': 'first', 'high': 'max', 'low': 'min', 'close': 'last'})

# 关闭数据库连接
conn.close()

# 打印结果
print(df_k)
