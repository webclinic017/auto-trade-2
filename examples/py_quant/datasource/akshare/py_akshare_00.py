import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory  as fg
import akshare as ak
from dash import html
from dash import dcc
from dash import Input#输入
from dash import Output#输出
import time
from dash import dash_table
import dash
import pandas as pd
import requests
import json
import datetime
import time
import os
import execjs
#获取最进1周的交易日期，自动踢出非交易日
df=ak.stock_zh_a_daily(symbol='sh000001')
date=df['date'].tolist()[-10:]
date_list=[]
for i in date:
    date_list.append(str(i)[:10])
loc=time.localtime()
week=loc.tm_wday
if week<=5:
    date_list.append(datetime.datetime.now())
#建立股票列表
code=ak.stock_individual_fund_flow_rank()
def adjust_stock(x):
    if x[0]=='6' or x[:2]=='68' or x[:2]=='30':
        x='SH'+x
    elif x[0]=='0':
        x='SZ'+x
    else:
        x=x
    return  x
code['股票代码1']=code['代码'].apply(adjust_stock)
stock_dict=dict(zip(code['股票代码1'].tolist(),code['名称'].tolist()))
def stock_indvid_ananly(date='20220930'):
    '''
    行业分析统计分析
    '''
    df=ak.stock_zt_pool_em(date=date)
    hy_list = df['所属行业'].tolist()
    # 去掉重复的数据
    hy_list_tuple = list(set(hy_list))
    hy_data_count = []
    for i in hy_list_tuple:
        hy_data_count.append(hy_list.count(i))
    hy_df = pd.DataFrame({'行业': hy_list_tuple, '板块个数': hy_data_count})
    # 对数据进行排序
    hy = hy_df.sort_values(by='板块个数', ascending=False,ignore_index=True)
    return hy
def get_comple_title_em(code='SZ000837'):
    '''
    从东方财富获取公司的核心题材数据
    code股票代码
    '''
    url='http://emweb.securities.eastmoney.com/CoreConception/PageAjax?'
    headers={
        'Age':'23',
        'Expires':'Sat, 30 Jul 2022 15:01:32 GMT',
        'Last-Modified':'Sat, 30 Jul 2022 14:59:32 GMT',
        'Server':'Tengine',
        'Strict-Transport-Security':'max-age=3153600',
        'Host':'emweb.securities.eastmoney.com',
        'Referer':'http://emweb.securities.eastmoney.com/CoreConception/Index?type=web&code={}'.format(code),
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
        'X-Requested-With':'XMLHttpRequest'
    }
    params={
        'code':code
    }
    res=requests.get(url=url,params=params,headers=headers)
    json_text=json.loads(res.text)
    #核心题材
    df=pd.DataFrame(json_text['ssbk'])
    #详细题材
    #df1=pd.DataFrame(json_text['hxtc'])
    df.rename(columns={'BOARD_NAME':'核心题材'},inplace=True)
    df1=df[['核心题材']]
    return df1
def get_stock_gn_ananly(date='20221014'):
    df=ak.stock_zt_pool_em(date=date)
    gn = pd.DataFrame()
    # 将全部的数据合并
    for stock in df['代码'].tolist():
        if stock[0:1] == '0':
            stock = 'SZ' + stock
        else:
            stock = 'SH' + stock
        # 获取涨停股票全部的概念数据
        url = 'http://emweb.securities.eastmoney.com/CoreConception/PageAjax?'
        headers = {
            'Age': '23',
            'Expires': 'Sat, 30 Jul 2022 15:01:32 GMT',
            'Last-Modified': 'Sat, 30 Jul 2022 14:59:32 GMT',
            'Server': 'Tengine',
            'Strict-Transport-Security': 'max-age=3153600',
            'Host': 'emweb.securities.eastmoney.com',
            'Referer': 'http://emweb.securities.eastmoney.com/CoreConception/Index?type=web&code={}'.format(stock),
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest'
        }
        params = {
            'code': stock
        }
        res = requests.get(url=url, params=params, headers=headers)
        json_text = json.loads(res.text)
        # 核心题材
        df = pd.DataFrame(json_text['ssbk'])
        # 详细题材
        # df1=pd.DataFrame(json_text['hxtc'])
        df.rename(columns={'BOARD_NAME': '核心题材'}, inplace=True)
        df1 = df[['核心题材']]
        gn_df = df1
        gn = pd.concat([gn, gn_df], ignore_index=True)
    # 对核心题材进行统计,去掉重复的概念
    bk = list(set(gn['核心题材'].tolist()))
    bk_count = []
    for m in bk:
        bk_count.append(gn['核心题材'].tolist().count(m))
    bk_df = pd.DataFrame({'题材': bk, '出现的次数': bk_count})
    # 对数据进行排序，前10
    bk_df_sort = bk_df.sort_values(by='出现的次数', ascending=False, ignore_index=True)[:10]
    return bk_df_sort
#统计涨停的股票个数
def get_stock_count_zt_and_dt_amount(start_date='20220926',end_date='20220930'):
    df=ak.stock_zh_a_daily(symbol='sh000001')
    date_list_amount=df['date'].tolist()[-20:]
    date_list_1 = []
    zt_count = []
    dt_count = []
    for i in date_list_amount:
        date_list_1.append(str(i)[:10])
    for date_time in date_list_1:
        try:
            zt=ak.stock_zt_pool_em(date=''.join(str(date_time)[:11].split('-')))
            dt=ak.stock_zt_pool_dtgc_em(date=''.join(str(date_time)[:11].split('-')))
            zt_count.append(len(zt['代码'].tolist()))
            dt_count.append(len(dt['代码'].tolist()))
        except:
            dt_count.append(0)
    data=pd.DataFrame({'时间':date_list_amount,'涨停家数':zt_count,'跌停家数':dt_count})
    return data
#股票涨停高标统计
#统计涨停的股票个数
def get_stock_zt_gb_count(start_date='20220920',end_date='20220930'):
    '''
    统计涨停的股票龙头高标
    '''
    start_end_list=pd.date_range(start=start_date,end=end_date)
    df=ak.stock_zh_a_daily(symbol='sh000001')
    date_list_amount=df['date'].tolist()[-len(start_end_list):]
    loc=time.localtime()
    week=loc.tm_wday
    if week<=5:
        date_list_amount.append(datetime.datetime.now())
    name=[]
    total_count=[]
    for date_time in date_list_amount:
        df=ak.stock_zt_pool_em(date=''.join(str(date_time)[:11].split('-')))
        #天数
        #涨停次数
        count=[]
        for m in df['涨停统计']:
            count.append(m.split('/')[1])
        df['涨停次数']=count
        #建立索引
        index_dict=dict(zip(df['涨停次数'].tolist(),df['名称'].tolist()))
        name.append(index_dict[str(max(count))])
        total_count.append(max(count))
    data=pd.DataFrame({'时间':date_list_amount,'高标股票名称':name,'涨停次数':total_count})
    return data
#盘口异动
pk_change=['火箭发射', '快速反弹', '大笔买入', '封涨停板', '打开跌停板', '有大买盘', '竞价上涨', '高开5日线',
           '向上缺口', '60日新高', '60日大幅上涨', '加速下跌', '高台跳水', '大笔卖出', '封跌停板', '打开涨停板',
           '有大卖盘', '竞价下跌', '低开5日线', '向下缺口', '60日新低', '60日大幅下跌']
xg=["创月新高", "半年新高", "一年新高", "历史新高","创月新低", "半年新低", "一年新低", "历史新低",'连续上涨',
    '连续下跌','持续放量','持续缩量',"5日均线", "10日均线", "20日均线", "30日均线", "60日均线", "90日均线", "250日均线", "500日均线",
    '量价齐升','量价齐跌','险资举牌']
rd=['雪球关注排行榜','雪球讨论排行榜','雪球分享交易排行榜','同花顺热度榜','东方财富热度榜','淘股吧热度榜','历史趋势及粉丝特征',
    '个股人气榜-实时变动','热门关键词','个股人气榜-最新排名','相关股票']
rd_dict=dict(zip(rd,rd))
xg_dict=dict(zip(xg,xg))
pk_dict=dict(zip(pk_change,pk_change))
#获取全部的板块代码和名称
def get_all_bk_code_and_name():
    '''
    获取全部的板块代码和名称
    '''
    url='https://push2.eastmoney.com/api/qt/clist/get?'
    params={
        'cb':'jQuery1123025425493616713957_1665558535555',
        'pn':'1',
        'pz':'500',
        'po':'1',
        'np':'1',
        'fields':'f12,f13,f14,f174',
        'fid':'f174',
        'fs':'m:90+t:2',
        'ut':'b2884a393a59ad64002292a3e90d46a5',
        '_':'1665558535637'
    }
    res = requests.get(url=url, params=params)
    text = res.text[43:len(res.text) - 2]
    json_text = json.loads(text)
    df=pd.DataFrame(json_text['data']['diff'])
    columns=['板块代码','-','板块名称','板块资金流入']
    df.columns=columns
    return df
#获取全部的板块
def get_all_bk_data(priods='今日'):
    '''
    获取全部的板块概念数据
    实时数据
    数据类型，今日，5日，10日
    '''
    data_dict={'今日':'f62','5日':'f164','10日':'f174'}
    url='https://push2.eastmoney.com/api/qt/clist/get?'
    params={
        'cb':'jQuery1123025425493616713957_1665558535555',
        'fid':data_dict[priods],
        'po':'1',
        'pz':'200',
        'pn':'1',
        'np':'1',
        'fltt':'2',
        'invt':'2',
        'ut':'b2884a393a59ad64002292a3e90d46a5',
        'fs':'m:90 t:2',
        'fields':'f12,f14,f2,f3,f62,f184,f66,f69,f72,f75,f78,f81,f84,f87,f204,f205,f124,f1,f13'
    }
    res = requests.get(url=url, params=params)
    text = res.text[43:len(res.text) - 2]
    json_text = json.loads(text)
    df=pd.DataFrame(json_text['data']['diff'])
    columns=['-','-','今日涨跌幅','板块代码','-','板块名称','今日主力净流入-净额','今日超大单净流入-净额',
    '今日超大单净流入-净占比','今日大单净流入-净额','今日大单净流入-净占比','今日中单净流入-净额','今日中单净流入-净占比',
    '今日小单净流入-净额','今日小单净流入-净占比','-','今日主力净流入-净占比','今日主力净流入最大股','股票代码','-']
    df.columns=columns
    del df['-']
    return df
#获取板块交易数据
def get_bk_trader_data_em(code='BK1029',start_date='20220701'):
    '''
    获取板块交易数据
    数据来自东方财富日线数据
    汽车板块为例http://quote.eastmoney.com/bk/90.BK1029.html#
    code板块代码，start_date开始时间，end_date介绍时间
    '''
    loc=time.localtime()
    year=loc.tm_year
    mo=loc.tm_mon
    daily=loc.tm_mday
    if mo<=9:
        mo='0'+str(mo)
    if daily<=9:
        daily='0'+str(daily)
    end_date='{}{}{}'.format(year,mo,daily)
    url='http://66.push2his.eastmoney.com/api/qt/stock/kline/get?'
    params={
        'cb':'jQuery35105177058251439297_1659341939018',
        'secid':'90.{}'.format(code),
        'ut':'fa5fd1943c7b386f172d6893dbfba10b',
        'fields1':'f1,f2,f3,f4,f5,f6',
        'fields2':'f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61',
        'klt':'101',
        'fqt':'1',
        'beg':start_date,
        'end':end_date,
        'smplmt':'460',
        'lmt':'1000000',
        '_':'1659341939158'
    }
    res=requests.get(url=url,params=params)
    text=res.text[41:len(res.text)-2]
    json_text=json.loads(text)
    df=pd.DataFrame(json_text['data']['klines'])
    df.columns=['数据']
    data=[]
    for i in df['数据']:
        data.append(i.split(','))
    df1=pd.DataFrame(data)
    columes=['date','open','close','high','low','成交额',
    '振幅','涨跌幅','涨跌额','换手率','-']
    df1.columns=columes
    return df1
#获取板块成分股
def get_bk_stock_data_em(code='BK1029',priods='今日'):
    '''
    获取板块成分股
    数据来自东方财富
    汽车板块为例子
    code板块代码1029汽车
    https://data.eastmoney.com/bkzj/BK1029.html
    '''
    data_dict={'今日':'f3','5日':'f109','10日':'f160'}
    url='https://push2.eastmoney.com/api/qt/clist/get?'
    params={
        'cb':'jQuery112304883635439371805_1659341233428',
        'fid':data_dict[priods],
        'po':'1',
        'pz':'5000',
        'pn':'1',
        'np':'1',
        'fltt':'2',
        'invt':'2',
        'ut':'b2884a393a59ad64002292a3e90d46a5',
        'fs':'b:{}'.format(code),
        'fields':'f12,f14,f2,f3,f62,f184,f66,f69,f72,f75,f78,f81,f84,f87,f204,f205,f124,f1,f13'
    }
    res=requests.get(url=url,params=params)
    text=res.text[42:len(res.text)-2]
    json_text=json.loads(text)
    df=pd.DataFrame(json_text['data']['diff'])
    #选取股票的代码和名称就可以了
    columns=['-','最新价','今日涨跌幅','股票代码','-','股票名称','主力净流入-净额','超大单净流入','超大单净流入-占比',
    '大单净流入','大单净流入-占比','中单净流入','中单净流入-占比','小单净流入','小单净流入-占比',
    '-','主力净流入-净占比','-','-','-']
    df.columns=columns
    del df['-']
    return df
#板块分析
def get_bk_qd_ananly(code='BK1029',priods='今日'):
    '''
    板块分析
    '''
    df=get_bk_stock_data_em(code=code,priods='今日')
    index=['上涨','下跌','涨停','跌停','上涨大于5','下跌大于5']
    sz=len(df[df['今日涨跌幅']>=0]['今日涨跌幅'].tolist())
    xd=len(df[df['今日涨跌幅']<0]['今日涨跌幅'].tolist())
    zt=len(df[df['今日涨跌幅']>=10]['今日涨跌幅'].tolist())
    dt=len(df[df['今日涨跌幅']<=-10]['今日涨跌幅'].tolist())
    zt_5=len(df[df['今日涨跌幅']>=5]['今日涨跌幅'].tolist())
    dt_5=len(df[df['今日涨跌幅']<=-5]['今日涨跌幅'].tolist())
    columns=[sz,xd,zt,dt,zt_5,dt_5]
    data=pd.DataFrame(columns)
    data.index=index
    result=data.T
    return result
get_bk_qd_ananly()
#获取板块实时数据
def get_bk_now_cash_trader_data(code='BK1029'):
    '''
    获取板块实时资金数据
    code板块代码
    '''
    url='https://push2.eastmoney.com/api/qt/stock/fflow/kline/get?'
    params={
        'cb':'jQuery1123002395009316077612_1665562995811',
        'lmt':'0',
        'klt':'1',
        'fields1':'f1,f2,f3,f7',
        'fields2':'f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61,f62,f63,f64,f65',
        'ut':'b2884a393a59ad64002292a3e90d46a5',
        'secid':'90.{}'.format(code),
        '_':'1665562995812'
    }
    res=requests.get(url=url,params=params)
    text=res.text[43:len(res.text)-2]
    json_text=json.loads(text)
    df=pd.DataFrame(json_text['data']['klines'])
    df.columns=['数据']
    data_list=[]
    for m in df['数据']:
        data_list.append(m.split(','))
    data=pd.DataFrame(data_list)
    columns=['时间','今日主力净流入','  今日小单净流入','今日中单净流入','今日大单净流入','今日超大单净流入']
    data.columns=columns
    return data
#获取板块历史资金流
def get_bk_hist_cash_data(code='BK1029'):
    '''
    '''
    url='https://push2his.eastmoney.com/api/qt/stock/fflow/daykline/get?'
    params={
        'cb':'jQuery1123045213813657472657_1665564061064',
        'lmt':'0',
        'klt':'101',
        'fields1':'f1,f2,f3,f7',
        'fields2':'f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61,f62,f63,f64,f65',
        'ut':'b2884a393a59ad64002292a3e90d46a5',
        'secid':'90.{}'.format(code),
        '_':'1665564061065'
    }
    res=requests.get(url=url,params=params)
    text=res.text[43:len(res.text)-2]
    json_text=json.loads(text)
    df=pd.DataFrame(json_text['data']['klines'])
    df.columns=['数据']
    data_list=[]
    for m in df['数据']:
        data_list.append(m.split(','))
    data=pd.DataFrame(data_list)
    columns=['日期','主力净流入-净额','小单净流入-净额','中单净流入-净额','大单净流入-净额',
    '超大单净流入-净额','主力净流入-净占比','小单净流入-净占比','中单净流入-净占比','大单净流入-净占比',
    '超大单净流入-净占比','-','-','-','-']
    data.columns=columns
    del data['-']
    return data
#获取分时数据
def stock_board_industry_hist_min_em(symbol='BK1027', period= '5') :
    """
    获取分时数据
    :param period: choice of {"1", "5", "15", "30", "60"}
    :type period: str
    :return: 分时历史行情
    :rtype: pandas.DataFrame
    """
    url = "http://7.push2his.eastmoney.com/api/qt/stock/kline/get"
    params = {
        "secid": f"90.{symbol}",
        "ut": "fa5fd1943c7b386f172d6893dbfba10b",
        "fields1": "f1,f2,f3,f4,f5,f6",
        "fields2": "f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61",
        "klt": period,
        "fqt": "1",
        "beg": "0",
        "end": "20500101",
        "smplmt": "10000",
        "lmt": "1000000",
        "_": "1626079488673",
    }
    r = requests.get(url, params=params)
    data_json = r.json()
    temp_df = pd.DataFrame(
        [item.split(",") for item in data_json["data"]["klines"]]
    )
    temp_df.columns = ["日期时间","开盘","收盘","最高","最低","成交量","成交额","振幅","涨跌幅","涨跌额","换手率",]
    temp_df = temp_df[
        [ "日期时间","开盘","收盘","最高","最低","涨跌幅","涨跌额","成交量","成交额","振幅", "换手率",]
    ]
    temp_df["开盘"] = pd.to_numeric(temp_df["开盘"], errors="coerce")
    temp_df["收盘"] = pd.to_numeric(temp_df["收盘"], errors="coerce")
    temp_df["最高"] = pd.to_numeric(temp_df["最高"], errors="coerce")
    temp_df["最低"] = pd.to_numeric(temp_df["最低"], errors="coerce")
    temp_df["涨跌幅"] = pd.to_numeric(temp_df["涨跌幅"], errors="coerce")
    temp_df["涨跌额"] = pd.to_numeric(temp_df["涨跌额"], errors="coerce")
    temp_df["成交量"] = pd.to_numeric(temp_df["成交量"], errors="coerce")
    temp_df["成交额"] = pd.to_numeric(temp_df["成交额"], errors="coerce")
    temp_df["振幅"] = pd.to_numeric(temp_df["振幅"], errors="coerce")
    temp_df["换手率"] = pd.to_numeric(temp_df["换手率"], errors="coerce")
    return temp_df
#获取股票核心题材
def get_stock_title(code='SH600031'):
    '''
    获取股票的核心题材
    '''
    url='http://emweb.securities.eastmoney.com/PC_HSF10/CoreConception/PageAjax?'
    params={
        'code':code
    }
    res=requests.get(url=url,params=params)
    text=res.json()
    df=pd.DataFrame(text['ssbk'])
    return df
#股票涨停的原因
def get_stock_zt_yy(code='001269',date='20221014'):
    '''
    股票涨停的原因
    '''
    url='http://www.iwencai.com/diag/block-detail?'
    headers={
        #other_uid=Ths_iwencai_Xuangu_x6mz5rvs4ltao186pwiilqdzd8qeb94u; ta_random_userid=b4wrz2elx6; cid=44416866bf16dcf0de325039d6ade9b61663666838; cid=44416866bf16dcf0de325039d6ade9b61663666838; ComputerID=44416866bf16dcf0de325039d6ade9b61663666838; WafStatus=0; wencai_pc_version=0; PHPSESSID=71811ac3b0ed259fdb638f612fbbb237; v=A8x4YfQWw1T--deoCFXFjsz4nSHxBXCvcqmEcyaN2HcasWIXThVAP8K5VAB1
        #other_uid=Ths_iwencai_Xuangu_x6mz5rvs4ltao186pwiilqdzd8qeb94u; ta_random_userid=b4wrz2elx6; cid=44416866bf16dcf0de325039d6ade9b61663666838; cid=44416866bf16dcf0de325039d6ade9b61663666838; ComputerID=44416866bf16dcf0de325039d6ade9b61663666838; WafStatus=0; wencai_pc_version=0; PHPSESSID=71811ac3b0ed259fdb638f612fbbb237; v=A6kdfinF7pObG9InVkfYKTmbuF4Mdp2oB2rBPEueJRDPEseIk8ateJe60Q_Y
        'Cookie':'other_uid=Ths_iwencai_Xuangu_x6mz5rvs4ltao186pwiilqdzd8qeb94u; ta_random_userid=b4wrz2elx6; cid=44416866bf16dcf0de325039d6ade9b61663666838; cid=44416866bf16dcf0de325039d6ade9b61663666838; ComputerID=44416866bf16dcf0de325039d6ade9b61663666838; WafStatus=0; wencai_pc_version=0; PHPSESSID=71811ac3b0ed259fdb638f612fbbb237; v={}'.format(v),
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'
    }
    params={
        'pid':'11656',
        'codes':code,
        'codeType':'stock',
        'info':'{"view":{"nolazy":1,"parseArr":{"_v":"new","dateRange":["'+date+'","'+date+'"],"staying":[],"queryCompare":[],"comparesOfIndex":[]},"asyncParams":{"tid":9381}}}'
    }
    res=requests.get(url=url,params=params,headers=headers)
    text=res.json()
    df=pd.DataFrame(text['data']['data']['result']['reasons'])
    data=pd.DataFrame()
    data['原因']=df['abstract'].tolist()
    return data
#涨停的全部原因
def get_zt_all_yy():
    '''
    涨停的全部原因
    '''
    url='https://x-quote.cls.cn/quote/index/up_down_analysis?'
    params={
        'app':'CailianpressWeb',
        'os':'web',
        'rever':'1',
        'sv':'7.7.5',
        'type':'up_pool',
        'way':'last_px',
        'sign':'a820dce18412fac3775aa940d0b00dcb'
    }
    headers={
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'
    }
    res=requests.get(url=url,params=params,headers=headers)
    text=res.json()
    df=pd.DataFrame(text['data'])
    return df
def get_gn_and_code_data():
    '''
    概念名称和代码
    '''
    url='https://push2.eastmoney.com/api/qt/clist/get?'
    params={
        'cb':'jQuery112309428053258541502_1666102042971',
        'pn':'1',
        'pz':'500',
        'po':'1',
        'np':'1',
        'fields':'f12,f13,f14,f62',
        'fid':'f62',
        'fs':'m:90+t:3',
        'ut':'b2884a393a59ad64002292a3e90d46a5',
        '_':'1666102042979'
    }
    res=requests.get(url=url,params=params)
    text=res.text[42:len(res.text)-2]
    json_text=json.loads(text)
    df=pd.DataFrame(json_text['data']['diff'])
    columns=['概念代码','-','概念名称','-']
    df.columns=columns
    del df['-']
    return df
#获取概念成分股
def get_gn_all_stock_data(code='BK0989'):
    '''
    获取概念成分股
    BK0989      储能
    '''
    url='https://push2.eastmoney.com/api/qt/clist/get?'
    params={
        'cb':'jQuery112307649910020406439_1666103425782',
        'fid':'f3',
        'po':'1',
        'pz':'500',
        'pn':'1',
        'np':'1',
        'fltt':'2',
        'invt':'2',
        'ut':'b2884a393a59ad64002292a3e90d46a5',
        'fs':'b:{}'.format(code),
        'fields':'f12,f14,f2,f3,f62,f184,f66,f69,f72,f75,f78,f81,f84,f87,f204,f205,f124,f1,f13'
    }
    res=requests.get(url=url,params=params)
    text=res.text[42:len(res.text)-2]
    json_text=json.loads(text)
    df=pd.DataFrame(json_text['data']['diff'])
    df.rename(columns={'f14':'股票','f3':'涨跌幅'},inplace=True)
    df1=df[['股票','涨跌幅']]
    df2=df1.replace('-',0)
    count=0
    #统计A股涨停
    df_a_9=df2[df2['涨跌幅']>=9.9]
    df_a_10=df_a_9[df_a_9['涨跌幅']<=10.03]
    if len(df_a_10) !=0:
        count+=len(df_a_10['涨跌幅'].tolist())
    #统计创业板
    df_cyb=df2[df2['涨跌幅']>=20]
    if len(df_cyb) !=0:
        count+=len(df_cyb['涨跌幅'].tolist())
    return count
def get_gn_all_stock_data_jt(code='BK0989'):
    '''
    获取概念具体分析
    BK0989      储能
    '''
    url='https://push2.eastmoney.com/api/qt/clist/get?'
    params={
        'cb':'jQuery112307649910020406439_1666103425782',
        'fid':'f3',
        'po':'1',
        'pz':'500',
        'pn':'1',
        'np':'1',
        'fltt':'2',
        'invt':'2',
        'ut':'b2884a393a59ad64002292a3e90d46a5',
        'fs':'b:{}'.format(code),
        'fields':'f12,f14,f2,f3,f62,f184,f66,f69,f72,f75,f78,f81,f84,f87,f204,f205,f124,f1,f13'
    }
    res=requests.get(url=url,params=params)
    text=res.text[42:len(res.text)-2]
    json_text=json.loads(text)
    df=pd.DataFrame(json_text['data']['diff'])
    df.rename(columns={'f14':'股票','f3':'涨跌幅'},inplace=True)
    df1=df[['股票','涨跌幅']]
    df2=df1.replace('-',0)
    count=0
    #统计A股涨停
    df_a_9=df2[df2['涨跌幅']>=9.9]
    df_a_10=df_a_9[df_a_9['涨跌幅']<=10.03]
    if len(df_a_10) !=0:
        count+=len(df_a_10['涨跌幅'].tolist())
    #统计创业板
    df_cyb=df2[df2['涨跌幅']>=20]
    if len(df_cyb) !=0:
        count+=len(df_cyb['涨跌幅'].tolist())
    data=pd.DataFrame({'涨停家数':list(str(count))})
    return data
#概念涨停分析
from tqdm import tqdm
def gn_zt_count_ananly():
    '''
    概念涨停分析
    '''
    gn=get_gn_and_code_data()
    columns=gn['概念名称'].tolist()
    count=[]
    for i in tqdm(range(len(gn['概念名称'].tolist()))):
        code=gn['概念代码'].tolist()[i]
        amount=get_gn_all_stock_data(code=code)
        count.append(amount)
    data=pd.DataFrame({'概念名称':columns,'涨停家数':count})
    result=data.sort_values(by='涨停家数',ascending=False)
    return result
trader=date[-1]
trader_date=''.join(str(trader)[:10].split('-'))
zt_data=ak.stock_zt_pool_em(date=trader_date)
zt_data_dict=dict(zip(zt_data['代码'].tolist(),zt_data['名称'].tolist()))
df=get_all_bk_code_and_name()
bk_name=dict(zip(df['板块代码'].tolist(),df['板块名称'].tolist()))
gn_df=ak.stock_board_concept_name_em()
gn_dict=dict(zip(df['板块名称'].tolist(),df['板块名称'].tolist()))
stock_gn=get_gn_and_code_data()
stock_gn_dict=dict(zip(stock_gn['概念代码'].tolist(),stock_gn['概念名称'].tolist()))
app=dash.Dash(__name__)
app.layout=html.Div([
    dcc.RadioItems(options=['下载数据','不下载数据',],value='不下载数据',id='down_button',style={'font-size':25}),
    dcc.RadioItems(options=['刷新数据','不刷新数据'],value='刷新数据',id='ref'),
    dcc.Download(id='down_data'),
    dash_table.DataTable(
        id='maker_ananly',
        page_size=10,
        style_table={'font-size':18}
    ),
    dcc.RadioItems(options=['今日涨停数据','今日跌停数据','炸板股票','昨日涨停','强势涨停','新股涨停','板块轮动',
                            '题材分析','情绪分析','股票盘口异动','同花顺选股','股票热度','龙头高标','不显示数据\n',
                            '主力控盘','综合评价','用户关注指数','市场参与意愿','股票市场成本','财联社-快讯数据',
                            '股票核心题材','涨停原因','全部涨停原因'],value='今日涨停数据',id='data_type',style={'font-size':18}),
    dcc.DatePickerSingle(date=date_list[0],id='start_date'),
    dcc.DatePickerSingle(date=date_list[-1],id='end_date'),
    dcc.Dropdown(options=pk_dict,value='大笔买入',id='pk'),
    dcc.Dropdown(options=xg_dict,value='创月新高',id='xg_type'),
    dcc.Dropdown(options=rd,value='同花顺热度榜',id='rd_type'),
    dcc.Dropdown(options=stock_dict,value='SH600031',id='stock'),
    dcc.Dropdown(options=zt_data_dict,id='zt_stock'),
    dcc.Download(id='gend_down_data'),
    dash_table.DataTable(
        id='gend_data',
        page_size=10,
        style_table={'font-size':18},
    ),
    #通用图片展示
    dcc.Graph(id='gend_figure_show'),
    html.H2('股票板块题材分析'),
    dcc.RadioItems(options=['下载数据','不下载数据'],value='不下载数据',id='down_1'),
    dcc.RadioItems(options=['今日', '3日', '5日', '10日'],value='今日',id='bk_down_1'),
    html.P('选择数据可以选择今日, 3日, 5日, 10日数据'),
    dcc.RadioItems(options=['个股资金流入排行','板块代码和名称','板块概念数据','板块交易数据',
    '板块成分股排行','板块实时资金数据','板块历史资金流数据','1分钟数据','5分钟数据','15分钟数据',
    '30分钟数据','60分钟数据','板块强度分析','概念板块','概念板块成份股','概念板块指数-日频',
    '概念板块指数-分时','概念涨停分析','概念涨停分析前10','概念具体分析'],value='个股资金流入排行',id='bk_data_type_1',style={'font-size':18}),
    dcc.Dropdown(options=bk_name,value='BK1029',id='bk_stock_1'),
    dcc.Dropdown(options=gn_dict,value='中药',id='gn_type'),
    dcc.Dropdown(options=stock_gn_dict,value='BK0989',id='gn'),
    dcc.DatePickerSingle(date='20220901',id='start_date_1'),
    dcc.DatePickerSingle(date=datetime.datetime.now(),id='end_date_1'),
    dcc.Download(id='down_bk_data_1'),
    dash_table.DataTable(
        id='show_bk_data_1',
        page_size=10,
        style_table={'font-size':16}
    ),
    dcc.Graph(id='show_bk_figure_1')
])
@app.callback(
    Output(component_id='maker_ananly',component_property='data'),
    Input(component_id='ref',component_property='value')
)
def ref_data(ref):
    if ref=='刷新数据':
        df = ak.stock_market_activity_legu()
        maker_dict = dict(zip(df['item'].tolist(), df['value'].tolist()))
        maker = pd.DataFrame(maker_dict, index=range(11))[-1:]
        return maker.to_dict('records')
    else:
        pass
@app.callback(
    Output(component_id='down_data',component_property='data'),
    Input(component_id='down_button',component_property='value'),
    Input(component_id='ref',component_property='value')
)
def down_data(down_button,ref):
    if down_button=='下载数据' and ref=='不刷新数据':
        df = ak.stock_market_activity_legu()
        maker_dict = dict(zip(df['item'].tolist(), df['value'].tolist()))
        maker = pd.DataFrame(maker_dict, index=range(11))[-1:]
        return  dcc.send_data_frame(df.to_excel,filename='市场概况.xlsx')
#通用数据会调
@app.callback(
    Output(component_id='gend_data',component_property='data'),
    Input(component_id='start_date',component_property='date'),
    Input(component_id='end_date',component_property='date'),
    Input(component_id='data_type',component_property='value'),
    Input(component_id='ref',component_property='value'),
    Input(component_id='pk',component_property='value'),
    Input(component_id='xg_type',component_property='value'),
    Input(component_id='stock',component_property='value'),
    Input(component_id='rd_type',component_property='value'),
    Input(component_id='zt_stock',component_property='value')
)
def update_gend_data_show(start_date,end_date,data_type,ref,pk,xg_type,stock,rd_type,zt_stock):
    if data_type=='今日涨停数据':
        df=ak.stock_zt_pool_em(date=''.join(str(end_date)[:11].split('-')))
        return df.to_dict('records')
    elif data_type=='今日跌停数据':
        df=ak.stock_zt_pool_dtgc_em(date=''.join(str(end_date)[:11].split('-')))
        return df.to_dict('records')
    elif data_type=='炸板股票':
        df=ak.stock_zt_pool_zbgc_em(date=''.join(str(end_date)[:11].split('-')))
        return df.to_dict('records')
    elif data_type=='强势涨停':
        df=ak.stock_zt_pool_strong_em(date=''.join(str(end_date)[:11].split('-')))
        return df.to_dict('records')
    elif data_type=='昨日涨停':
        df=ak.stock_zt_pool_previous_em(date=''.join(str(end_date)[:11].split('-')))
        return df.to_dict('records')
    elif data_type=='新股涨停':
        df=ak.stock_zt_pool_sub_new_em(date=''.join(str(end_date)[:11].split('-')))
        return df.to_dict('records')
    elif data_type=='板块轮动':
        df=stock_indvid_ananly(date=''.join(str(end_date)[:11].split('-')))
        return df.to_dict('records')
    elif data_type=='题材分析':
        df=get_stock_gn_ananly(date=''.join(str(end_date)[:11].split('-')))
        return df.to_dict('records')
    elif data_type=='情绪分析':
        df=get_stock_count_zt_and_dt_amount(start_date=start_date,end_date=end_date)
        return df.to_dict('records')
    elif data_type=='股票盘口异动':
        df=ak.stock_changes_em(symbol=pk)
        return df.to_dict('records')
    elif data_type=='同花顺选股' and xg_type in ["创月新高", "半年新高", "一年新高", "历史新高"]:
        df=ak.stock_rank_cxg_ths(symbol=xg_type)
        return df.to_dict('records')
    elif data_type=='同花顺选股' and xg_type in ["创月新低", "半年新低", "一年新低", "历史新低"]:
        df=ak.stock_rank_cxd_ths(symbol=xg_type)
        return df.to_dict('records')
    elif data_type=='同花顺选股' and xg_type=='连续上涨':
        df=ak.stock_rank_lxsz_ths()
        return df.to_dict('records')
    elif data_type=='同花顺选股' and xg_type=='连续下跌':
        df=ak.stock_rank_lxsz_ths()
        return df.to_dict('records')
    elif data_type=='同花顺选股' and xg_type=='持续放量':
        df=ak.stock_rank_cxfl_ths()
        return df.to_dict('records')
    elif data_type=='同花顺选股' and xg_type=='持续缩量':
        df=ak.stock_rank_cxfl_ths()
        return df.to_dict('records')
    #向上突破
    elif data_type == '同花顺选股' and xg_type in ["5日均线", "10日均线", "20日均线", "30日均线", "60日均线", "90日均线", "250日均线", "500日均线"]:
        df=ak.stock_rank_xstp_ths(symbol=xg_type)
        return df.to_dict('records')
    elif data_type=='同花顺选股' and xg_type=='量价齐升':
        df=ak.stock_rank_ljqs_ths()
        return df.to_dict('records')
    elif data_type=='同花顺选股' and xg_type=='量价齐跌':
        df=ak.stock_rank_ljqs_ths()
        return df.to_dict('records')
    elif data_type=='同花顺选股' and xg_type=='险资举牌':
        df=ak.stock_rank_xzjp_ths()
        return df.to_dict('records')
    elif data_type=='股票热度' and rd_type==rd[0]:
        df=ak.stock_hot_follow_xq()
        return df.to_dict('records')
    elif data_type=='股票热度' and rd_type==rd[1]:
        df=ak.stock_hot_tweet_xq()
        return df.to_dict('records')
    elif data_type=='股票热度' and rd_type==rd[2]:
        df=ak.stock_hot_deal_xq()
        return df.to_dict('records')
    elif data_type=='股票热度' and rd_type==rd[3]:
        df=ak.stock_hot_rank_wc()
        return df.to_dict('records')
    elif data_type=='股票热度' and rd_type==rd[4]:
        df=ak.stock_hot_rank_em()
        return df.to_dict('records')
    elif data_type=='股票热度' and rd_type==rd[5]:
        df=ak.stock_hot_tgb()
        return df.to_dict('records')
    elif data_type=='股票热度' and rd_type==rd[6]:
        df=ak.stock_hot_rank_detail_em(symbol=stock)
        return df.to_dict('records')
    elif data_type=='股票热度' and rd_type==rd[7]:
        df=ak.stock_hot_rank_detail_realtime_em(symbol=stock)
        return df.to_dict('records')
    elif data_type=='股票热度' and rd_type==rd[8]:
        df=ak.stock_hot_keyword_em(symbol=stock)
        return df.to_dict('records')
    elif data_type=='股票热度' and rd_type==rd[9]:
        df=ak. stock_hot_rank_latest_em(symbol=stock)
        return df.to_dict('records')
    elif data_type=='股票热度' and rd_type==rd[10]:
        df=ak.stock_hot_rank_relate_em(symbol=stock)
        return df.to_dict('records')
    elif data_type=='龙头高标':
        df=get_stock_zt_gb_count(start_date=start_date,end_date=end_date)
        return df.to_dict('records')
    elif data_type=='主力控盘':
        df=ak.stock_comment_detail_zlkp_jgcyd_em(symbol=stock[2:])
        return df.to_dict('records')
    elif data_type=='综合评价':
        df=ak.stock_comment_detail_zhpj_lspf_em(symbol=stock[2:])
        return df.to_dict('records')
    elif data_type=='用户关注指数':
        df=ak.stock_comment_detail_scrd_focus_em(symbol=stock[2:])
        return df.to_dict('records')
    elif data_type=='市场参与意愿':
        df=ak.stock_comment_detail_scrd_desire_em(symbol=stock[2:])
        return df.to_dict('records')
    elif data_type=='股票市场成本':
        df=ak. stock_comment_detail_scrd_cost_em(symbol=stock[2:])
        return df.to_dict('records')
    elif data_type=='财联社-快讯数据':
        df=ak.stock_zh_a_alerts_cls()
        return df.to_dict('records')
    elif data_type=='股票核心题材':
        df=get_stock_title(code=stock)
        return df.to_dict('records')
    elif data_type=='涨停原因':
        df=get_stock_zt_yy(code=zt_stock)
        return df.to_dict('records')
    elif data_type=='全部涨停原因':
        df=get_zt_all_yy()
        del df['plate']
        return df.to_dict('records')
    else:
        pass
#显示通用图片
@app.callback(
    Output(component_id='gend_figure_show',component_property='figure'),
    Input(component_id='start_date',component_property='date'),
    Input(component_id='end_date',component_property='date'),
    Input(component_id='data_type',component_property='value'),
    Input(component_id='stock',component_property='value'),
    Input(component_id='rd_type',component_property='value')
)
def update_gend_figure_show(start_date,end_date,data_type,stock,rd_type):
    if data_type=='板块轮动':
        df = stock_indvid_ananly(date=''.join(str(end_date)[:11].split('-')))
        fig=px.bar(data_frame=df,x='行业',y='板块个数')
        return fig
    elif data_type=='题材分析':
        df = get_stock_gn_ananly(date=''.join(str(end_date)[:11].split('-')))
        fig=px.bar(data_frame=df,x='题材',y='出现的次数')
        return fig
    elif data_type=='情绪分析':
        df = get_stock_count_zt_and_dt_amount(start_date=start_date, end_date=end_date)
        fig=px.line(data_frame=df,x='时间',y=['涨停家数','跌停家数'])
        return fig
    elif data_type=='股票热度' and rd_type==rd[0]:
        df=ak.stock_hot_follow_xq()[:10]
        fig=px.bar(data_frame=df,x='股票简称',y='关注')
        return fig
    elif data_type=='股票热度' and rd_type==rd[1]:
        df=ak.stock_hot_tweet_xq()
        fig = px.bar(data_frame=df, x='股票简称', y='关注')
        return fig
    elif data_type=='股票热度' and rd_type==rd[2]:
        df=ak.stock_hot_deal_xq()
        fig = px.bar(data_frame=df, x='股票简称', y='关注')
        return fig
    elif data_type=='股票热度' and rd_type==rd[3]:
        df=ak.stock_hot_rank_wc(date=end_date)[:10]
        fig=px.bar(data_frame=df,x='股票简称',y='个股热度')
        return fig
    elif data_type=='股票热度' and rd_type==rd[4]:
        df=ak.stock_hot_rank_em()[:10]
        fig=px.bar(data_frame=df,x='股票名称',y='最新价')
        return fig
    elif data_type=='股票热度' and rd_type==rd[5]:
        df=ak.stock_hot_tgb()
        fig=px.bar(data_frame=df,x='个股代码',y='个股名称')
        return fig
    elif data_type=='股票热度' and rd_type==rd[6]:
        df=ak.stock_hot_rank_detail_em(symbol=stock)
        fig=px.line(data_frame=df,x='时间',y=['新晋粉丝','铁杆粉丝'])
        return fig
    elif data_type=='股票热度' and rd_type==rd[7]:
        df=ak.stock_hot_rank_detail_realtime_em(symbol=stock)
        px.line(data_frame=df,x='时间',y='排名')
        return fig
    elif data_type=='股票热度' and rd_type==rd[8]:
        df=ak.stock_hot_keyword_em(symbol=stock)[:10]
        fig=px.bar(data_frame=df,x='概念名称',y='热度')
        return fig
    elif data_type=='股票热度' and rd_type==rd[9]:
        df=ak.stock_hot_rank_latest_em(symbol=stock)
    elif data_type=='股票热度' and rd_type==rd[10]:
        df=ak.stock_hot_rank_relate_em(symbol=stock)
        fig=px.bar(data_frame=df,x='相关股票代码',y='涨跌幅')
        return fig
    elif data_type=='龙头高标':
        df=get_stock_zt_gb_count(start_date=start_date,end_date=end_date)
        fig=px.bar(data_frame=df,x='时间',y='高标股票名称')
        return fig
    elif data_type=='主力控盘':
        df=ak.stock_comment_detail_zlkp_jgcyd_em(symbol=stock[2:])
        fig=px.line(data_frame=df,x='date',y='value')
        return fig
    elif data_type=='综合评价':
        df=ak.stock_comment_detail_zhpj_lspf_em(symbol=stock[2:])
        fig=px.line(data_frame=df,x='日期',y='评分')
        return fig
    elif data_type=='用户关注指数':
        df=ak.stock_comment_detail_scrd_focus_em(symbol=stock[2:])
        fig=px.line(data_frame=df,x='日期',y='用户关注指数')
        return fig
    elif data_type=='市场参与意愿':
        df=ak.stock_comment_detail_scrd_desire_em(symbol=stock[2:])
        fig=px.line(data_frame=df,x='日期时间',y=['大户','全部','散户'])
        return fig
    elif data_type=='股票市场成本':
        df=ak. stock_comment_detail_scrd_cost_em(symbol=stock[2:])
        fig=px.bar(data_frame=df,x='日期',y=['市场成本','5日市场成本'])
        return fig
    else:
        df = stock_indvid_ananly(date=''.join(str(end_date)[:11].split('-')))
        fig = px.bar(data_frame=df, x='行业', y='板块个数')
        return fig
#通用数据下载
@app.callback(
    Output(component_id='gend_down_data',component_property='data'),
    Input(component_id='start_date',component_property='date'),
    Input(component_id='end_date',component_property='date'),
    Input(component_id='ref',component_property='value'),
    Input(component_id='pk',component_property='value'),
    Input(component_id='data_type',component_property='value'),
    Input(component_id='down_button',component_property='value'),
    Input(component_id='xg_type',component_property='value'),
    Input(component_id='stock',component_property='value'),
    Input(component_id='rd_type',component_property='value')
)
def update_gend_data_down(start_date,end_date,ref,pk,data_type,down_button,xg_type,stock,rd_type):
    if data_type=='今日涨停数据' and down_button=='下载数据':
        df = ak.stock_zt_pool_em(date=''.join(str(end_date)[:11].split('-')))
        return  dcc.send_data_frame(df.to_excel,filename='{}{}.xlsx'.format(''.join(str(end_date)[:11].split('-')),data_type))
    elif data_type=='今日跌停数据' and down_button=='下载数据':
        df = ak.stock_zt_pool_dtgc_em(date=''.join(str(end_date)[:11].split('-')))
        return  dcc.send_data_frame(df.to_excel,filename='{}{}.xlsx'.format(''.join(str(end_date)[:11].split('-')),data_type))
    elif data_type=='炸板股票' and down_button=='下载数据':
        df = ak.stock_zt_pool_zbgc_em(date=''.join(str(end_date)[:11].split('-')))
        return  dcc.send_data_frame(df.to_excel,filename='{}{}.xlsx'.format(''.join(str(end_date)[:11].split('-')),data_type))
    elif data_type=='强势涨停' and down_button=='下载数据':
        df = ak.stock_zt_pool_strong_em(date=''.join(str(end_date)[:11].split('-')))
        return  dcc.send_data_frame(df.to_excel,filename='{}{}.xlsx'.format(''.join(str(end_date)[:11].split('-')),data_type))
    elif data_type=='昨日涨停' and down_button=='下载数据':
        df = ak.stock_zt_pool_previous_em(date=''.join(str(end_date)[:11].split('-')))
        return  dcc.send_data_frame(df.to_excel,filename='{}{}.xlsx'.format(''.join(str(end_date)[:11].split('-')),data_type))
    elif data_type=='新股涨停' and down_button=='下载数据':
        df = ak.stock_zt_pool_sub_new_em(date=''.join(str(end_date)[:11].split('-')))
        return  dcc.send_data_frame(df.to_excel,filename='{}{}.xlsx'.format(''.join(str(end_date)[:11].split('-')),data_type))
    elif data_type=='板块轮动' and down_button=='下载数据':
        df = stock_indvid_ananly(date=''.join(str(end_date)[:11].split('-')))
        return  dcc.send_data_frame(df.to_excel,filename='{}{}.xlsx'.format(''.join(str(end_date)[:11].split('-')),data_type))
    elif data_type=='题材分析' and down_button=='下载数据':
        df = get_stock_gn_ananly(date=''.join(str(end_date)[:11].split('-')))
        return  dcc.send_data_frame(df.to_excel,filename='{}{}.xlsx'.format(''.join(str(end_date)[:11].split('-')),data_type))
    elif data_type=='情绪分析' and down_button=='下载数据':
        df = get_stock_count_zt_and_dt_amount(start_date=start_date, end_date=end_date)
        return  dcc.send_data_frame(df.to_excel,filename='{}{}.xlsx'.format(''.join(str(end_date)[:11].split('-')),data_type))
    elif data_type=='股票盘口异动' and down_button=='下载数据':
        df = ak.stock_changes_em(symbol=pk)
        return  dcc.send_data_frame(df.to_excel,filename='{}{}{}.xlsx'.format(''.join(str(end_date)[:11].split('-')),data_type,pk))
    elif data_type=='同花顺选股' and xg_type in ["创月新高", "半年新高", "一年新高", "历史新高"] and down_button=='下载数据':
        df=ak.stock_rank_cxg_ths(symbol=xg_type)
        return dcc.send_data_frame(df.to_excel,filename='{}{}.xlsx'.format(data_type,xg_type))
    elif data_type=='同花顺选股' and xg_type in ["创月新低", "半年新低", "一年新低", "历史新低"] and down_button=='下载数据':
        df=ak.stock_rank_cxd_ths(symbol=xg_type)
        return dcc.send_data_frame(df.to_excel,filename='{}{}.xlsx'.format(data_type,xg_type))
    elif data_type=='同花顺选股' and xg_type=='连续上涨' and down_button=='下载数据':
        df=ak.stock_rank_lxsz_ths()
        return dcc.send_data_frame(df.to_excel,filename='{}{}.xlsx'.format(data_type,xg_type))
    elif data_type=='同花顺选股' and xg_type=='连续下跌' and down_button=='下载数据':
        df=ak.stock_rank_lxsz_ths()
        return dcc.send_data_frame(df.to_excel,filename='{}{}.xlsx'.format(data_type,xg_type))
    elif data_type=='同花顺选股' and xg_type=='持续放量' and down_button=='下载数据':
        df=ak.stock_rank_cxfl_ths()
        return dcc.send_data_frame(df.to_excel,filename='{}{}.xlsx'.format(data_type,xg_type))
    elif data_type=='同花顺选股' and xg_type=='持续缩量' and down_button=='下载数据':
        df=ak.stock_rank_cxfl_ths()
        return dcc.send_data_frame(df.to_excel,filename='{}{}.xlsx'.format(data_type,xg_type))
    #向上突破
    elif data_type == '同花顺选股' and xg_type in ["5日均线", "10日均线", "20日均线", "30日均线", "60日均线", "90日均线", "250日均线", "500日均线"] and down_button=='下载数据':
        df=ak.stock_rank_xstp_ths(symbol=xg_type)
        return dcc.send_data_frame(df.to_excel,filename='{}{}.xlsx'.format(data_type,xg_type))
    elif data_type=='同花顺选股' and xg_type=='量价齐升' and down_button=='下载数据':
        df=ak.stock_rank_ljqs_ths()
        return dcc.send_data_frame(df.to_excel,filename='{}{}.xlsx'.format(data_type,xg_type))
    elif data_type=='同花顺选股' and xg_type=='量价齐跌' and down_button=='下载数据':
        df=ak.stock_rank_ljqs_ths()
        return dcc.send_data_frame(df.to_excel,filename='{}{}.xlsx'.format(data_type,xg_type))
    elif data_type=='同花顺选股' and xg_type=='险资举牌' and down_button=='下载数据':
        df=ak.stock_rank_xzjp_ths()
        return dcc.send_data_frame(df.to_excel,filename='{}{}.xlsx'.format(data_type,xg_type))
    elif data_type=='股票热度' and rd_type==rd[0] and down_button=='下载数据':
        df=ak.stock_hot_follow_xq()[:10]
        return dcc.send_data_frame(df.to_excel,filename='{}{}.xlsx'.format(data_type,rd_type))
    elif data_type=='股票热度' and rd_type==rd[1] and down_button=='下载数据':
        df=ak.stock_hot_tweet_xq()
        return dcc.send_data_frame(df.to_excel,filename='{}{}.xlsx'.format(data_type,rd_type))
    elif data_type=='股票热度' and rd_type==rd[2] and down_button=='下载数据':
        df=ak.stock_hot_deal_xq()
        return dcc.send_data_frame(df.to_excel,filename='{}{}.xlsx'.format(data_type,rd_type))
    elif data_type=='股票热度' and rd_type==rd[3] and down_button=='下载数据':
        df=ak.stock_hot_rank_wc(date=end_date)[:10]
        return dcc.send_data_frame(df.to_excel,filename='{}{}.xlsx'.format(data_type,rd_type))
    elif data_type=='股票热度' and rd_type==rd[4] and down_button=='下载数据':
        df=ak.stock_hot_rank_em()[:10]
        return dcc.send_data_frame(df.to_excel,filename='{}{}.xlsx'.format(data_type,rd_type))
    elif data_type=='股票热度' and rd_type==rd[5] and down_button=='下载数据':
        df=ak.stock_hot_tgb()
        return dcc.send_data_frame(df.to_excel,filename='{}{}.xlsx'.format(data_type,rd_type))
    elif data_type=='股票热度' and rd_type==rd[6] and down_button=='下载数据':
        df=ak.stock_hot_rank_detail_em(symbol=stock)
        return dcc.send_data_frame(df.to_excel,filename='{}{}.xlsx'.format(data_type,rd_type))
    elif data_type=='股票热度' and rd_type==rd[7] and down_button=='下载数据':
        df=ak.stock_hot_rank_detail_realtime_em(symbol=stock)
        return dcc.send_data_frame(df.to_excel,filename='{}{}.xlsx'.format(data_type,rd_type))
    elif data_type=='股票热度' and rd_type==rd[8] and down_button=='下载数据':
        df=ak.stock_hot_keyword_em(symbol=stock)[:10]
        return dcc.send_data_frame(df.to_excel,filename='{}{}.xlsx'.format(data_type,rd_type))
    elif data_type=='股票热度' and rd_type==rd[9] and down_button=='下载数据':
        df=ak.stock_hot_rank_latest_em(symbol=stock)
        return dcc.send_data_frame(df.to_excel,filename='{}{}.xlsx'.format(data_type,rd_type))
    elif data_type=='股票热度' and rd_type==rd[10] and down_button=='下载数据':
        df=ak.stock_hot_rank_relate_em(symbol=stock)
        return dcc.send_data_frame(df.to_excel,filename='{}{}.xlsx'.format(data_type,rd_type))
    elif data_type == '龙头高标' and down_button=='下载数据':
        df = get_stock_zt_gb_count(start_date=start_date, end_date=end_date)
        return dcc.send_data_frame(df.to_excel, filename='{}.xlsx'.format(data_type))
    elif data_type == '主力控盘' and down_button=='下载数据':
        df = ak.stock_comment_detail_zlkp_jgcyd_em(symbol=stock[2:])
        return dcc.send_data_frame(df.to_excel, filename='{}{}.xlsx'.format(data_type, stock))
    elif data_type == '综合评价' and down_button=='下载数据':
        df = ak.stock_comment_detail_zhpj_lspf_em(symbol=stock[2:])
        return dcc.send_data_frame(df.to_excel, filename='{}{}.xlsx'.format(data_type, stock))
    elif data_type == '用户关注指数' and down_button=='下载数据':
        df = ak.stock_comment_detail_scrd_focus_em(symbol=stock[2:])
        return dcc.send_data_frame(df.to_excel, filename='{}{}.xlsx'.format(data_type, stock))
    elif data_type == '市场参与意愿' and down_button=='下载数据':
        df = ak.stock_comment_detail_scrd_desire_em(symbol=stock[2:])
        return dcc.send_data_frame(df.to_excel, filename='{}{}.xlsx'.format(data_type, stock))
    elif data_type == '股票市场成本' and down_button=='下载数据':
        df = ak.stock_comment_detail_scrd_cost_em(symbol=stock[2:])
        return dcc.send_data_frame(df.to_excel, filename='{}{}.xlsx'.format(data_type, stock))
    elif data_type=='财联社-快讯数据' and down_button=='下载数据':
        df=ak.stock_zh_a_alerts_cls()
        return dcc.send_data_frame(df.to_excel,filename='{}.xlsx'.format(data_type))
#通用板块数据回调
@app.callback(
        Output(component_id='show_bk_data_1',component_property='data'),
        Input(component_id='start_date_1',component_property='date'),
        Input(component_id='end_date_1',component_property='date'),
        Input(component_id='bk_down_1',component_property='value'),
        Input(component_id='bk_data_type_1',component_property='value'),
        Input(component_id='bk_stock_1',component_property='value'),
        Input(component_id='gn_type',component_property='value'),
        Input(component_id='gn',component_property='value')
)
def update_show_bk_data(start_date,end_date,bk_down,bk_data_type,bk_stock,gn_type,gn):
    if bk_data_type=='个股资金流入排行':
        df=ak.stock_individual_fund_flow_rank(indicator=bk_down)
        return df.to_dict('records')
    elif bk_data_type=='板块代码和名称':
        df=get_all_bk_code_and_name()
        return df.to_dict('records')
    elif bk_data_type=='板块概念数据':
        df=get_all_bk_data(priods=bk_down)
        return df.to_dict('records')
    elif bk_data_type=='板块交易数据':
        df=get_bk_trader_data_em(code=bk_stock,start_date=''.join(str(start_date)[:11].split('-')))
        return df.to_dict('records')
    elif bk_data_type=='板块成分股排行':
        df=get_bk_stock_data_em(code=bk_stock)
        return df.to_dict('records')
    elif bk_data_type=='板块实时资金数据':
        df=get_bk_now_cash_trader_data(code=bk_stock)
        return df.to_dict('records')
    elif bk_data_type=='板块历史资金流数据':
        df=get_bk_hist_cash_data(code=bk_stock)
        return df.to_dict('records')
    elif bk_data_type=='1分钟数据':
        df=stock_board_industry_hist_min_em(symbol=bk_stock, period="1")
        return df.to_dict('records')
    elif bk_data_type=='5分钟数据':
        df=stock_board_industry_hist_min_em(symbol=bk_stock, period="5")
        return df.to_dict('records')
    elif bk_data_type=='15分钟数据':
        df=stock_board_industry_hist_min_em(symbol=bk_stock, period="15")
        return df.to_dict('records')
    elif bk_data_type=='30分钟数据':
        df=stock_board_industry_hist_min_em(symbol=bk_stock, period="30")
        return df.to_dict('records')
    elif bk_data_type=='60分钟数据':
        df=stock_board_industry_hist_min_em(symbol=bk_stock, period="60")
    elif bk_data_type=='概念板块':
        df=ak.stock_board_concept_name_em()
        return df.to_dict('records')
    elif bk_data_type=='概念板块成份股':
        df=ak.stock_board_concept_cons_em()
        return df.to_dict('records')
    elif bk_data_type=='概念板块指数-日频':
        df=ak.stock_board_concept_hist_em()
        return df.to_dict('records')
    elif bk_data_type=='概念板块指数-分时':
        df=ak.stock_board_concept_hist_min_em()
        return df.to_dict('records')
    elif bk_data_type=='概念涨停分析':
        df=gn_zt_count_ananly()
        return df.to_dict('records')
    elif bk_data_type=='概念涨停分析前10':
        df=gn_zt_count_ananly()[:10]
        return df.to_dict('records')
    elif bk_data_type=='概念具体分析':
        df=get_gn_all_stock_data_jt(code=gn)
        return df.to_dict('records')
#通用图片显示数据回调
@app.callback(
        Output(component_id='show_bk_figure_1',component_property='figure'),
        Input(component_id='start_date_1',component_property='date'),
        Input(component_id='end_date_1',component_property='date'),
        Input(component_id='bk_down_1',component_property='value'),
        Input(component_id='bk_data_type_1',component_property='value'),
        Input(component_id='bk_stock_1',component_property='value')
)
def update_bk_figure_data(start_date,end_date,bk_down,bk_data_type,bk_stock):
    if bk_data_type=='个股资金流入排行':
        df=ak.stock_individual_fund_flow_rank(indicator=bk_down)[:10]
        fig=px.bar(data_frame=df,x='名称',y='{}主力净流入-净额'.format(bk_down))
        return fig
    elif bk_data_type=='板块代码和名称':
        df=get_all_bk_code_and_name()
        fig=px.bar(data_frame=df,x='板块名称',y='板块资金流入')
        return fig
    elif bk_data_type=='板块概念数据':
        df=get_all_bk_data(priods=bk_down)[:10]
        fig=px.bar(data_frame=df,x='板块名称',y='今日主力净流入-净额')
        return fig
    elif bk_data_type=='板块交易数据':
        df=get_bk_trader_data_em(code=bk_stock,start_date=''.join(str(start_date)[:11].split('-')))
        fig=go.Figure(data=[go.Candlestick(x=df['date'],open=df['open'],close=df['close'],high=df['high'],low=df['low'])])
        return fig
    elif bk_data_type=='板块成分股排行':
        df=get_bk_stock_data_em(code=bk_stock)
        fig=px.bar(data_frame=df,x='股票名称',y='主力净流入-净额')
        return fig
    elif bk_data_type=='板块实时资金数据':
        df=get_bk_now_cash_trader_data(code=bk_stock)
        y_list =['今日主力净流入','今日中单净流入','今日大单净流入','今日超大单净流入']
        for m in y_list:
            df[m] = pd.to_numeric(df[m])
        fig=px.line(data_frame=df,x='时间',y=['今日主力净流入','今日中单净流入','今日大单净流入','今日超大单净流入'])
        return fig
    elif bk_data_type=='板块历史资金流数据':
        df=get_bk_hist_cash_data(code=bk_stock)
        y_list=['主力净流入-净额','小单净流入-净额','中单净流入-净额','大单净流入-净额','超大单净流入-净额']
        for m in y_list:
            df[m]=pd.to_numeric(df[m])
        fig=px.line(data_frame=df,x='日期',y=['主力净流入-净额','小单净流入-净额','中单净流入-净额','大单净流入-净额','超大单净流入-净额'])
        return fig
    elif bk_data_type=='1分钟数据':
        df=stock_board_industry_hist_min_em(symbol=bk_stock, period="1")
        df['日期时间']=pd.to_datetime(df['日期时间'])
        fig=go.Figure(data=[go.Candlestick(open=df['开盘'],close=df['收盘'],low=df['最低'],high=df['最高'])])
        return fig
    elif bk_data_type=='5分钟数据':
        df=stock_board_industry_hist_min_em(symbol=bk_stock, period="5")
        df['日期时间'] = pd.to_datetime(df['日期时间'])
        fig=go.Figure(data=[go.Candlestick(open=df['开盘'],close=df['收盘'],low=df['最低'],high=df['最高'])])
        return fig
    elif bk_data_type=='15分钟数据':
        df=stock_board_industry_hist_min_em(symbol=bk_stock, period="15")
        df['日期时间'] = pd.to_datetime(df['日期时间'])
        fig=go.Figure(data=[go.Candlestick(open=df['开盘'],close=df['收盘'],low=df['最低'],high=df['最高'])])
        return fig
    elif bk_data_type=='30分钟数据':
        df=stock_board_industry_hist_min_em(symbol=bk_stock, period="30")
        df['日期时间'] = pd.to_datetime(df['日期时间'])
        fig=go.Figure(data=[go.Candlestick(open=df['开盘'],close=df['收盘'],low=df['最低'],high=df['最高'])])
        return fig
    elif bk_data_type=='60分钟数据':
        df=stock_board_industry_hist_min_em(symbol=bk_stock, period="60")
        df['日期时间'] = pd.to_datetime(df['日期时间'])
        fig=go.Figure(data=[go.Candlestick(open=df['开盘'],close=df['收盘'],low=df['最低'],high=df['最高'])])
        return fig
    elif bk_data_type=='板块强度分析':
        df=get_bk_qd_ananly(code=bk_stock)
        fig=px.bar(data_frame=df,y=['上涨','下跌','涨停','跌停','上涨大于5','下跌大于5'])
        return fig
#通用板块数据下载
@app.callback(
        Output(component_id='down_bk_data_1',component_property='data'),
        Input(component_id='start_date_1',component_property='date'),
        Input(component_id='end_date_1',component_property='date'),
        Input(component_id='bk_down_1',component_property='value'),
        Input(component_id='bk_data_type_1',component_property='value'),
        Input(component_id='bk_stock_1',component_property='value'),
        Input(component_id='down_1',component_property='value')
)
def update_show_bk_data(start_date,end_date,bk_down,bk_data_type,bk_stock,down):
    if bk_data_type=='个股资金流入排行' and down=='下载数据':
        df=ak.stock_individual_fund_flow_rank(indicator=bk_down)
        return dcc.send_data_frame(df.to_excel,filename='{}{}.xlsx'.format(bk_data_type,bk_down))
    elif bk_data_type=='板块代码和名称' and down=='下载数据':
        df=get_all_bk_code_and_name()
        return dcc.send_data_frame(df.to_excel,filename='{}.xlsx'.format(bk_data_type))
    elif bk_data_type=='板块概念数据' and down=='下载数据':
        df=get_all_bk_data(priods=bk_down)
        return dcc.send_data_frame(df.to_excel,filename='{}{}.xlsx'.format(bk_data_type,bk_down))
    elif bk_data_type=='板块交易数据' and down=='下载数据':
        df=get_bk_trader_data_em(code=bk_stock,start_date=''.join(str(start_date)[:11].split('-')))
        return dcc.send_data_frame(df.to_excel,filename='{}{}.xlsx'.format(bk_stock,bk_data_type))
    elif bk_data_type=='板块成分股排行' and down=='下载数据':
        df=get_bk_stock_data_em(code=bk_stock)
        return dcc.send_data_frame(df.to_excel,filename='{}{}.xlsx'.format(bk_stock,bk_data_type))
    elif bk_data_type=='板块实时资金数据' and down=='下载数据':
        df=get_bk_now_cash_trader_data(code=bk_stock)
        return dcc.send_data_frame(df.to_excel,filename='{}{}.xlsx'.format(bk_stock,bk_data_type))
    elif bk_data_type=='板块历史资金流数据' and down=='下载数据':
        df=get_bk_hist_cash_data(code=bk_stock)
        return dcc.send_data_frame(df.to_excel,filename='{}{}.xlsx'.format(bk_stock,bk_data_type))
    elif bk_data_type=='1分钟数据' and down=='下载数据':
        df=stock_board_industry_hist_min_em(symbol=bk_stock, period="1")
        return dcc.send_data_frame(df.to_excel,filename='{}{}.xlsx'.format(bk_stock,bk_data_type))
    elif bk_data_type=='5分钟数据' and down=='下载数据':
        df=stock_board_industry_hist_min_em(symbol=bk_stock, period="5")
        return dcc.send_data_frame(df.to_excel,filename='{}{}.xlsx'.format(bk_stock,bk_data_type))
    elif bk_data_type=='15分钟数据' and down=='下载数据':
        df=stock_board_industry_hist_min_em(symbol=bk_stock, period="15")
        return dcc.send_data_frame(df.to_excel,filename='{}{}.xlsx'.format(bk_stock,bk_data_type))
    elif bk_data_type=='30分钟数据' and down=='下载数据':
        df=stock_board_industry_hist_min_em(symbol=bk_stock, period="30")
        return dcc.send_data_frame(df.to_excel,filename='{}{}.xlsx'.format(bk_stock,bk_data_type))
    elif bk_data_type=='60分钟数据' and down=='下载数据':
        df=stock_board_industry_hist_min_em(symbol=bk_stock, period="60")
        return dcc.send_data_frame(df.to_excel,filename='{}{}.xlsx'.format(bk_stock,bk_data_type))
if __name__=='__main__':
    app.run_server(debug=True)