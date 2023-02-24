import requests
from bs4 import BeautifulSoup
import websocket
import easyquotation
import json
import jsonpath
import pandas as pd
# import easytrader
import akshare as ak
import pandas as pd
import requests
import matplotlib.pyplot as plt
import time
from tqdm import tqdm
plt.rcParams['font.family']='SimHei'
plt.rcParams['axes.unicode_minus']=False
#东方财富涨停股票数据
def get_zt_data_em():
    '''
    从东方财富获取股票涨停数据
    数据同花顺，财联社都有
    date时间查询
    '''
    #自动填充时间
    loc=time.localtime()
    year=loc.tm_year
    mo=loc.tm_mon
    daily=loc.tm_mday
    if mo<=9:
        mo='0'+str(mo)
    if daily<=9:
        daily='0'+str(daily)
    date='{}{}{}'.format(year,mo,daily)
    url='http://push2ex.eastmoney.com/getTopicZTPool?'
    params={
        'cb':'callbackdata7986788',
        'ut':'7eea3edcaed734bea9cbfc24409ed989',
        'dpt':'wz.ztzt',
        'Pageindex':'0',
        'pagesize':'5000',
        'sort':'fbt:asc',
        'date':date,
        '_':'1659186604092',
    }
    res=requests.get(url=url,params=params)
    text=res.text[20:len(res.text)-2]
    json_text=json.loads(text)
    print(json_text)
    df=pd.DataFrame(json_text['data']['pool'])
    #涨停数据统计
    columns=['股票代码','市场代码','股票名称','最新价',
    '涨跌幅','成交额','流通市值',
    '总市值','换手率','连板数',
    '首次封板时间','最后封板时间',
    '封板资金','炸板次数','所属行业','涨停统计']
    df.columns=columns
    #将涨停天数统计下来
    days=[]
    ct=[]
    for m in df['涨停统计']:
        dict_data=dict(m)
        days.append(dict_data['days'])
        ct.append(dict_data['ct'])
    df['天数']=days
    df['涨停次数']=ct
    del df['涨停统计']
    return df
#昨日涨停
def get_zr_zt_data_em():
    '''
    东方财富
    昨日涨停的股票
    '''
    #自动填充时间
    loc=time.localtime()
    year=loc.tm_year
    mo=loc.tm_mon
    daily=loc.tm_mday
    if mo<=9:
        mo='0'+str(mo)
    if daily<=9:
        daily='0'+str(daily)
    date='{}{}{}'.format(year,mo,daily)
    url='http://push2ex.eastmoney.com/getYesterdayZTPool?'
    params={
        'cb':'callbackdata5648188',
        'ut':'7eea3edcaed734bea9cbfc24409ed989',
        'dpt':'wz.ztzt',
        'Pageindex':'0',
        'pagesize':'5000',
        'sort':'zs:desc',
        'date':date,
        '_':'1659188682177'
    }
    res=requests.get(url=url,params=params)
    text=res.text[20:len(res.text)-2]
    json_text=json.loads(text)
    df=pd.DataFrame(json_text['data']['pool'])
    columns=['股票代码','市场代码','股票名称','最新价',
    '涨停价','涨跌幅','成交额','流通市值',
    '总市值','换手率','振幅','涨速','昨日封板时间',
    '昨日连板数','所属行业','涨停统计']
    df.columns=columns
    #将涨停天数统计下来
    days=[]
    ct=[]
    for m in df['涨停统计']:
        dict_data=dict(m)
        days.append(dict_data['days'])
        ct.append(dict_data['ct'])
    df['天数']=days
    df['涨停次数']=ct
    del df['涨停统计']
    print(df)
    return df
#强势涨停
def get_qs_zt_data_em():
    '''
    东方财富
    强势涨停数据
    '''
    #自动填充时间
    loc=time.localtime()
    year=loc.tm_year
    mo=loc.tm_mon
    daily=loc.tm_mday
    if mo<=9:
        mo='0'+str(mo)
    if daily<=9:
        daily='0'+str(daily)
    date='{}{}{}'.format(year,mo,daily)
    url='http://push2ex.eastmoney.com/getTopicQSPool?'
    params={
        'cb':'callbackdata6530158',
        'ut':'7eea3edcaed734bea9cbfc24409ed989',
        'dpt':'wz.ztzt',
        'Pageindex':'0',
        'pagesize':'20',
        'sort':'zdp:desc',
        'date':date,
        '_':'1659190809217'
    }
    res=requests.get(url=url,params=params)
    text=res.text[20:len(res.text)-2]
    json_text=json.loads(text)
    df=pd.DataFrame(json_text['data']['pool'])
    columns=['股票代码','市场代码','股票名称','最新价',
    '涨停价','-','涨跌幅','成交额','流通市值',
    '总市值','换手率','-','-','量比',
    '-','涨停统计','所属行业',]
    df.columns=columns
    #将涨停天数统计下来
    days=[]
    ct=[]
    for m in df['涨停统计']:
        dict_data=dict(m)
        days.append(dict_data['days'])
        ct.append(dict_data['ct'])
    df['天数']=days
    df['涨停次数']=ct
    del df['涨停统计']
    del df['-']
    print(df)
    return df
#公司核心题材查询
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
#获取板块交易数据
def get_bk_trader_data_em(code='1029',start_date='20220701'):
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
        'secid':'90.BK{}'.format(code),
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
    print(df1)
    return df1
#获取板块成分股
def get_bk_stock_data_em(code='1029'):
    '''
    获取板块成分股
    数据来自东方财富
    汽车板块为例子
    code板块代码1029汽车
    https://data.eastmoney.com/bkzj/BK1029.html
    '''
    url='https://push2.eastmoney.com/api/qt/clist/get?'
    params={
        'cb':'jQuery112304883635439371805_1659341233428',
        'fid':'f62',
        'po':'1',
        'pz':'5000',
        'pn':'1',
        'np':'1',
        'fltt':'2',
        'invt':'2',
        'ut':'b2884a393a59ad64002292a3e90d46a5',
        'fs':'b:BK{}'.format(code),
        'fields':'f12,f14,f2,f3,f62,f184,f66,f69,f72,f75,f78,f81,f84,f87,f204,f205,f124,f1,f13'
    }
    res=requests.get(url=url,params=params)
    text=res.text[42:len(res.text)-2]
    json_text=json.loads(text)
    df=pd.DataFrame(json_text['data']['diff'])
    #选取股票的代码和名称就可以了
    df.rename(columns={'f12':'股票代码','f14':'名称'},inplace=True)
    df1=df[['股票代码','名称']]
    print(df1)
    return df1
#板块资金流入排行
def get_bk_cash_float_rank():
    '''
    板块流入今日排行
    数据来自东方财富
    '''
    df=ak.stock_sector_fund_flow_rank(indicator='今日')
    print(df)
    return df
#东方财富人气排行前100
def get_rq_100_rank():
    '''
    东方财富股票人气排行前100
    '''
    #链接
    url_list=['https://push2.eastmoney.com/api/qt/ulist.np/get?fltt=2&np=3&ut=a79f54e3d4c8d44e494efb8f748db291&invt=2&secids=0.000625,0.000837,0.002665,0.002514,1.600418,0.000678,0.300068,1.600586,0.002896,0.300044,0.002547,0.000899,0.000957,0.002532,0.002339,0.002337,0.002666,0.002703,1.600218,0.000547&fields=f1,f2,f3,f4,f12,f13,f14,f152,f15,f16&cb=qa_wap_jsonpCB1659364385567',
    'https://push2.eastmoney.com/api/qt/ulist.np/get?fltt=2&np=3&ut=a79f54e3d4c8d44e494efb8f748db291&invt=2&secids=0.002564,0.002031,1.603366,1.603335,0.000599,0.002534,0.002593,0.002708,0.002008,0.002276,0.002444,0.002689,0.002938,0.300537,0.300487,0.000531,0.002369,1.603530,0.002685,0.002921&fields=f1,f2,f3,f4,f12,f13,f14,f152,f15,f16&cb=qa_wap_jsonpCB1659364407242',
    'https://push2.eastmoney.com/api/qt/ulist.np/get?fltt=2&np=3&ut=a79f54e3d4c8d44e494efb8f748db291&invt=2&secids=0.000533,1.603728,0.002209,0.002599,0.000629,1.601127,0.002340,1.603799,0.300098,1.600375,1.603286,1.603650,0.001258,1.603897,0.300750,1.603396,0.002231,0.000596,0.002475,0.300629&fields=f1,f2,f3,f4,f12,f13,f14,f152,f15,f16&cb=qa_wap_jsonpCB1659364424789',
    'https://push2.eastmoney.com/api/qt/ulist.np/get?fltt=2&np=3&ut=a79f54e3d4c8d44e494efb8f748db291&invt=2&secids=1.603577,0.002594,1.603602,0.002138,0.300059,1.601975,0.300337,0.002885,0.002825,1.603070,0.002507,0.002917,0.002206,0.002947,0.000565,0.002229,0.002635,0.002581,0.002753,0.002669&fields=f1,f2,f3,f4,f12,f13,f14,f152,f15,f16&cb=qa_wap_jsonpCB1659364444108',
    'https://push2.eastmoney.com/api/qt/ulist.np/get?fltt=2&np=3&ut=a79f54e3d4c8d44e494efb8f748db291&invt=2&secids=0.000821,0.002210,1.603201,1.603757,1.603261,1.605567,0.002362,1.601311,1.601633,1.603915,0.002290,0.002454,0.002976,0.002077,0.002494,0.002591,0.002384,1.600348,0.002911,0.002466&fields=f1,f2,f3,f4,f12,f13,f14,f152,f15,f16&cb=qa_wap_jsonpCB1659364462279']
    df=pd.DataFrame()
    #解析数据
    def params_data(url=None):
        res=requests.get(url=url)
        text=res.text[28:len(res.text)-2]
        json_text=json.loads(text)
        df=pd.DataFrame(json_text['data']['diff'])
        columns=['-','最新价','涨跌幅','涨跌额','代码','市场','名称','-','-','-']
        df.columns=columns
        del df['-']
        return df
    for i in tqdm(range(0,len(url_list))):
        df1=params_data(url=url_list[i])
        df=pd.concat([df,df1],ignore_index=True)
    print(df)
    return df
#东方财富人气飙升榜
def get_rq_bs_rank_100():
    url_list=['https://push2.eastmoney.com/api/qt/ulist.np/get?fltt=2&np=3&ut=a79f54e3d4c8d44e494efb8f748db291&invt=2&secids=1.688272,0.002857,0.300720,1.603602,1.688786,0.300331,1.603800,1.688260,0.832491,0.300964,1.603683,0.300632,0.002947,1.688282,0.300576,1.688618,0.300429,1.600375,1.688027,1.605567&fields=f1,f2,f3,f4,f12,f13,f14,f152,f15,f16&cb=qa_wap_jsonpCB1659365713518',
    'https://push2.eastmoney.com/api/qt/ulist.np/get?fltt=2&np=3&ut=a79f54e3d4c8d44e494efb8f748db291&invt=2&secids=1.688102,1.688161,0.300637,0.300951,0.002852,1.688183,0.300218,0.002494,1.603939,1.688499,1.688265,1.688655,1.688314,0.002387,1.600234,1.605318,0.002599,1.688095,1.603931,0.300631&fields=f1,f2,f3,f4,f12,f13,f14,f152,f15,f16&cb=qa_wap_jsonpCB1659365828179',
    'https://push2.eastmoney.com/api/qt/ulist.np/get?fltt=2&np=3&ut=a79f54e3d4c8d44e494efb8f748db291&invt=2&secids=0.300236,0.300879,0.002377,1.688001,0.301158,1.688456,0.300566,1.600241,0.300758,0.300620,0.300705,0.002917,1.688233,0.002890,0.002870,0.300484,0.002913,1.688772,0.002634,1.688072&fields=f1,f2,f3,f4,f12,f13,f14,f152,f15,f16&cb=qa_wap_jsonpCB1659365857107',
    'https://push2.eastmoney.com/api/qt/ulist.np/get?fltt=2&np=3&ut=a79f54e3d4c8d44e494efb8f748db291&invt=2&secids=1.603926,0.002313,0.002919,1.688312,0.301160,1.605080,0.300221,0.300384,0.002636,0.300799,0.300379,0.301021,0.002165,0.002442,1.688375,1.603228,1.688046,0.002086,0.002138,1.603639&fields=f1,f2,f3,f4,f12,f13,f14,f152,f15,f16&cb=qa_wap_jsonpCB1659365875711',
    'https://push2.eastmoney.com/api/qt/ulist.np/get?fltt=2&np=3&ut=a79f54e3d4c8d44e494efb8f748db291&invt=2&secids=0.300890,1.688261,0.300667,1.601798,0.002281,0.300076,0.300209,1.688718,1.688151,0.002142,0.002336,0.002851,1.600225,1.600880,0.300881,1.600725,1.601163,1.600388,0.300538,0.300644&fields=f1,f2,f3,f4,f12,f13,f14,f152,f15,f16&cb=qa_wap_jsonpCB1659365894084']
    df=pd.DataFrame()
    #解析数据
    def params_data(url=None):
        res=requests.get(url=url)
        text=res.text[28:len(res.text)-2]
        json_text=json.loads(text)
        df=pd.DataFrame(json_text['data']['diff'])
        columns=['-','最新价','涨跌幅','涨跌额','代码','市场','名称','-','-','-']
        df.columns=columns
        del df['-']
        return df
    for i in tqdm(range(0,len(url_list))):
        df1=params_data(url=url_list[i])
        df=pd.concat([df,df1],ignore_index=True)
    print(df)
    return df
def stock_changes_em(symbol: str = "大笔买入") -> pd.DataFrame:
    """
    东方财富-行情中心-盘口异动
    http://quote.eastmoney.com/changes/
    :param symbol: choice of {'火箭发射', '快速反弹', '大笔买入', '封涨停板', '打开跌停板', '有大买盘', '竞价上涨', '高开5日线', '向上缺口', '60日新高', '60日大幅上涨', '加速下跌', '高台跳水', '大笔卖出', '封跌停板', '打开涨停板', '有大卖盘', '竞价下跌', '低开5日线', '向下缺口', '60日新低', '60日大幅下跌'}
    :type symbol: str
    :return: 盘口异动
    :rtype: pandas.DataFrame
    """
    url = "http://push2ex.eastmoney.com/getAllStockChanges"
    symbol_map = {
        "火箭发射": "8201",
        "快速反弹": "8202",
        "大笔买入": "8193",
        "封涨停板": "4",
        "打开跌停板": "32",
        "有大买盘": "64",
        "竞价上涨": "8207",
        "高开5日线": "8209",
        "向上缺口": "8211",
        "60日新高": "8213",
        "60日大幅上涨": "8215",
        "加速下跌": "8204",
        "高台跳水": "8203",
        "大笔卖出": "8194",
        "封跌停板": "8",
        "打开涨停板": "16",
        "有大卖盘": "128",
        "竞价下跌": "8208",
        "低开5日线": "8210",
        "向下缺口": "8212",
        "60日新低": "8214",
        "60日大幅下跌": "8216",
    }
    reversed_symbol_map = {v: k for k, v in symbol_map.items()}
    params = {
        "type": symbol_map[symbol],
        "pageindex": "0",
        "pagesize": "5000",
        "ut": "7eea3edcaed734bea9cbfc24409ed989",
        "dpt": "wzchanges",
        "_": "1624005264245",
    }
    r = requests.get(url, params=params)
    data_json = r.json()
    temp_df = pd.DataFrame(data_json["data"]["allstock"])
    temp_df["tm"] = pd.to_datetime(temp_df["tm"], format="%H%M%S").dt.time
    temp_df.columns = [
        "时间",
        "代码",
        "_",
        "名称",
        "板块",
        "相关信息",
    ]
    temp_df = temp_df[
        [
            "时间",
            "代码",
            "名称",
            "板块",
            "相关信息",
        ]
    ]
    temp_df["板块"] = temp_df["板块"].astype(str)
    temp_df["板块"] = temp_df["板块"].map(reversed_symbol_map)
    return temp_df
#对涨停板进行分析
class params_zt_data():
    '''
    对涨停股票进行分析
    '''
    def __init__(self,df):
        self.df=df
    #对今天涨停的行业板块进行统计
    def count_hy_data(self):
        '''
        统计行业数据
        '''
        #获取数据
        import time
        loc=time.localtime()
        #五周的第几天，0星期五
        wdaily=loc.tm_wday
        dict_wdaily={'0':'星期一','1':'星期二','2':'星期三','3':'星期四','4':'星期五',}
        xq=dict_wdaily[str(wdaily)]
        hy_list=self.df['所属行业'].tolist()
        self.df.to_html(r'./{}涨停.html'.format(xq))
        #去掉重复的数据
        hy_list_tuple=list(set(hy_list))
        hy_data_count=[]
        for i in hy_list_tuple:
            hy_data_count.append(hy_list.count(i))
        hy_df=pd.DataFrame({'行业':hy_list_tuple,'板块个数':hy_data_count})
        #对数据进行排序
        hy=hy_df.sort_values(by='板块个数',ascending=False)
        hy.to_html(r'./{}板块统计.html'.format(xq))
        #绘图
        plt.bar(hy['行业'],hy['板块个数'])
        plt.title('行业个数统计前10')
        plt.xlabel('行业')
        plt.ylabel('板块个数')
        plt.savefig(r'./{}板块统计.png'.format(xq))
        plt.close()
        #对全部涨停的股票进行概念分析
        print(df)
        gn=pd.DataFrame()
        #将全部的数据合并
        for stock in df['股票代码'].tolist():
            try:
                if stock[0:1]=='0':
                    stock='SZ'+stock
                else:
                    stock='SH'+stock
                #获取涨停股票全部的概念数据
                gn_df=get_comple_title_em(code=stock)
                gn=pd.concat([gn,gn_df],ignore_index=True)
            except:
                print('获取失败')
        #对核心题材进行统计,去掉重复的概念
        bk=list(set(gn['核心题材'].tolist()))
        bk_count=[]
        for m in bk:
            bk_count.append(gn['核心题材'].tolist().count(m))
        bk_df=pd.DataFrame({'题材':bk,'出现的次数':bk_count})
        bk_df.to_html(r'./{}全部概念.html'.format(xq))
        #对数据进行排序，前10
        bk_df_sort=bk_df.sort_values(by='出现的次数',ascending=False,ignore_index=True)[:8] 
        bk_df_sort.to_html(r'./{}概念前8.html'.format(xq))
        #绘图
        plt.bar(bk_df_sort['题材'],bk_df_sort['出现的次数'])
        plt.title('涨停出现的概念前10排行')
        plt.xlabel('概念')
        plt.ylabel('出现的次数')
        plt.savefig(r'./{}概念前8'.format(xq))
        plt.close()
df=get_zt_data_em()
params_zt_data(df=df).count_hy_data()
#获取涨停数据
def stock_zt_data_params():
    '''
    股票涨停进板分析
    '''
    import time
    loc=time.localtime()
    #一周的第几天，0星期五
    wdaily=loc.tm_wday
    dict_wdaily={'0':'星期一','1':'星期二','2':'星期三','3':'星期四','4':'星期五'}
    xq=dict_wdaily[str(wdaily)]
    df=get_zt_data_em()
    print(df)
    #统计首板
    df_sb=df[df['天数']==1]
    df_sb.to_html(r'./{}首板.html'.format(xq))
    #联系涨停
    df_lx=df[df['天数']==df['涨停次数']]
    df_lx.to_html(r'./{}连续涨停.html'.format(xq))
    df=df_lx
    #一板晋级成功
    df_yb_jj=df[df['天数']<=2]
    df_yb_jj_1=df_yb_jj[df_yb_jj['天数']>1]
    df_yb_jj_1.to_html(r'./{}一板晋级.html'.format(xq))
    #三板晋级成功
    df_yb_jj_3=df[df['天数']<=3]
    df_yb_jj_3_1=df_yb_jj_3[df_yb_jj_3['天数']>2]
    df_yb_jj_3_1.to_html(r'./{}三板晋级.html'.format(xq))
    #五板晋级成功
    df_yb_jj_5=df[df['天数']<=5]
    df_yb_jj_5_1=df_yb_jj_5[df_yb_jj_5['天数']>4]
    df_yb_jj_5_1.to_html(r'./{}五板晋级.html'.format(xq))
    #7板晋级成功
    df_yb_jj_7=df[df['天数']<=20]
    df_yb_jj_7_1=df_yb_jj_7[df_yb_jj_7['天数']>6]
    df_yb_jj_7_1.to_html(r'./{}七板晋级.html'.format(xq))
    pkyd=stock_changes_em()
    print(pkyd)
    pkyd.to_html(r'./{}大笔买入.html'.format(xq))
stock_zt_data_params()