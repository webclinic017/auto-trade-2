# Alpha Quant

## Res

### Third api

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
  