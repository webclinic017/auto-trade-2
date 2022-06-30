from django.shortcuts import render

# Create your views here.
import tushare as ts

#获取数据
def get_data(code):
    # 存放需要的数据
    dict_return = {}
    # 通过股票代码获取股票最近的数据
    data = ts.get_hist_data(code)
    # 按照日期正序排列数据
    data_30 = data[:30].iloc[::-1]
    # 涨
    data_30['rise'] = data_30['price_change'] > 0
    # 跌
    data_30['fall'] = data_30['price_change'] < 0
    # 最近30个交易日的收盘价
    close = data_30['close']
    # 收盘价x轴数据
    close_index = list(close.index)
    # 收盘价y轴数据
    close_value = close.values.tolist()
    # 统计近30交易日的涨跌次数
    df_diff = data_30[['rise','fall']].sum()
    # 将数据转为列表格式
    df_diff_index = list(df_diff.index)
    # 将数据转为列表格式
    df_diff_value = df_diff.values.tolist()
    dict_return['diff'] = [{"name":item[0],"value":item[1]} for item in list(zip(df_diff_index,df_diff_value))] # 将数据制作成饼图需要的数据格式
    # 统计近30交易日的价格变化
    price_change = data_30['price_change'].values.tolist()
    # 统计近30交易日的成交量
    volume = data_30['volume'].values.tolist()
    # 以下为将处理好的数据加入字典
    dict_return['close_index'] = close_index
    dict_return['close_value'] = close_value
    dict_return['price_change'] = price_change
    dict_return['volume'] = volume
    dict_return['df_diff_index'] = df_diff_index
    # 返回数据
    return dict_return

#查询数据
def query(request):
    #请求方式为get
    if request.method=='GET':
        #获取股票数据
        dict_return = get_data('603021')
        #传入前端
        return render(request,'query.html', {'dict_return':dict_return})
    else:
        #请求方式为post
        code = request.POST.get('name')
        #获取股票数据
        dict_return = get_data(code)
        #传入数据
        return render(request,'query.html', {'dict_return':dict_return})


