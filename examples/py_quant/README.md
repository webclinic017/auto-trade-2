# Alpha Quant

## data

timescaledb 
devops/k8s/postgresql/postgres/docker-compose.yaml

### Third api

#### akshare

#### easyruatation

#### tushare

tushare.pro
www.alphavantage.co

tushare.pro api token: 

```python
import tushare as ts

g_ts_token = ""

ts.set_token(g_ts_token)

# pro = ts.pro_api()
pro = ts.pro_api(g_ts_token)

df = pro.index_daily(ts_code='399300.SZ', start_date='202000507', end_date='20200608')
print(df)

df = ts.get_today_all()
# print(df)

df = ts.get_index()
print(df)
```

#### BaoStock

```
pip install baostock -i https://pypi.tuna.tsinghua.edu.cn/simple/ --trusted-host pypi.tuna.tsinghua.edu.cn

```

#### efinance

```
pip install efinance
```

#### pyalgotrade-cn

#### rqalpha easyhistory

```bash
pip3 install rqalpha

## 下载股票历史数据
rqalpha update_bundle


```

## trade

### easytrader

https://easytrader.readthedocs.io/zh/master/usage/