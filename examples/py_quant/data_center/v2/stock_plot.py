"""
用于绘制股票k线
"""
import matplotlib as mpl
import matplotlib.pyplot as plt
import mplfinance as mpf
import numpy as np
import talib as ta

import stock_constant as sc
import stock_db as sdb

# 下载的字体路径
zhfont = mpl.font_manager.FontProperties(fname=sc.text_font)
# 标题格式，字体为中文字体，颜色为黑色，粗体，水平中心对齐
title_font = {'fontproperties': zhfont,
              'size': '16',
              'color': 'black',
              'weight': 'bold',
              'va': 'bottom',
              'ha': 'center'}
# 红色数字格式（显示开盘收盘价）粗体红色24号字
large_red_font = {'fontproperties': zhfont,
                  'size': '24',
                  'color': 'red',
                  'weight': 'bold',
                  'va': 'bottom'}
# 绿色数字格式（显示开盘收盘价）粗体绿色24号字
large_green_font = {'fontproperties': zhfont,
                    'size': '24',
                    'color': 'green',
                    'weight': 'bold',
                    'va': 'bottom'}
# 小数字格式（显示其他价格信息）粗体红色12号字
small_red_font = {'fontproperties': zhfont,
                  'size': '12',
                  'color': 'red',
                  'weight': 'bold',
                  'va': 'bottom'}
# 小数字格式（显示其他价格信息）粗体绿色12号字
small_green_font = {'fontproperties': zhfont,
                    'size': '12',
                    'color': 'green',
                    'weight': 'bold',
                    'va': 'bottom'}
# 标签格式，可以显示中文，普通黑色12号字
normal_label_font = {'fontproperties': zhfont,
                     'size': '12',
                     'color': 'black',
                     'va': 'bottom',
                     'ha': 'right'}
# 普通文本格式，普通黑色12号字
normal_font = {'fontproperties': zhfont,
               'size': '12',
               'color': 'black',
               'va': 'bottom',
               'ha': 'left'}


def kline(code, start_time, end_time):
    """
    绘制某股票某时间段的日行情k线图
    :param code:
    :param start_time:
    :param end_time:
    :return:
    """
    # 数据库读取数据
    df = sdb.stock_daily(code=code, start_time=start_time, end_time=end_time)
    print(df)
    # 重命名列
    df.rename(
        columns={
            'date': 'Date', 'open': 'Open',
            'high': 'High', 'low': 'Low',
            'close': 'Close', 'volume': 'Volume'},
        inplace=True)
    start_index = 20
    end_index = 147
    df_data = df.iloc[start_index:end_index]
    # 读取显示区间最后一个交易日的数据
    last_data = df_data.iloc[-1]

    # 设置图片边缘距离
    plt.subplots_adjust(left=0.08, right=0.92, top=0.92, bottom=0.08)

    # 设置marketcolors
    # up:设置K线线柱颜色，up意为收盘价大于等于开盘价
    # down:与up相反，这样设置与国内K线颜色标准相符
    # edge:K线线柱边缘颜色(i代表继承自up和down的颜色)，下同。详见官方文档)
    # wick:灯芯(上下影线)颜色
    # volume:成交量直方图的颜色
    # inherit:是否继承，选填
    mc = mpf.make_marketcolors(
        up='red',
        down='green',
        edge='in',
        wick='in',
        volume='in',
        inherit=True)

    # 设置图形风格
    # gridaxis:设置网格线位置
    # gridstyle:设置网格线线型
    # y_on_right:设置y轴位置是否在右
    m_style = mpf.make_mpf_style(
        gridaxis='both', gridstyle='-.',
        figcolor='(0.82, 0.83, 0.85)',
        gridcolor='(0.82, 0.83, 0.85)',
        y_on_right=False,
        marketcolors=mc)

    # 获取figure对象，以便对Axes对象和figure对象的自由控制
    fig = mpf.figure(style=m_style, figsize=(12, 8),
                     facecolor=(0.82, 0.83, 0.85))
    # 主图相对figure 底部 0.06，0.25，宽（0.88）、高（0.60）
    ax1 = fig.add_axes([0.06, 0.25, 0.88, 0.60])
    # 指标图 sharex 关键字指明与ax1在x轴上对齐，且共用x轴
    ax2 = fig.add_axes([0.06, 0.15, 0.88, 0.10], sharex=ax1)
    # macd
    ax3 = fig.add_axes([0.06, 0.05, 0.88, 0.10], sharex=ax1)
    # 设置y轴标签
    ax1.set_ylabel('price')
    ax2.set_ylabel('volume')
    ax3.set_ylabel('macd')

    # 在figure对象上添加文本对象，用于显示各种价格和标题
    fig.text(0.50, 0.94, '平安银行', **title_font)
    fig.text(0.12, 0.90, '开/收: ', **normal_label_font)
    fig.text(0.14, 0.89, '%.2f / %.2f' % (np.around(last_data["Open"], 2),
                                          np.round(last_data["Close"], 2)), **large_red_font)
    fig.text(0.12, 0.86, f'{last_data.name.date()}', **normal_label_font)
    change = last_data["Close"] - last_data["Open"]
    fig.text(0.14, 0.86, '%.2f' % change, **small_red_font)
    change_percent = (change / last_data["Open"]) * 100
    fig.text(0.22, 0.86, '%.2f%%' % change_percent, **small_red_font)
    fig.text(0.40, 0.90, '高: ', **normal_label_font)
    fig.text(0.40, 0.90, '%.2f' % (last_data["High"]), **small_red_font)
    fig.text(0.40, 0.86, '低: ', **normal_label_font)
    fig.text(0.40, 0.86, '%.2f' % (last_data["Low"]), **small_green_font)
    fig.text(0.55, 0.90, '量(万手): ', **normal_label_font)
    fig.text(0.55, 0.90, '%.2f' % (np.round(last_data["Volume"] / 10000, 3)), **normal_font)
    fig.text(0.55, 0.86, '额(亿元): ', **normal_label_font)
    fig.text(0.55, 0.86, '%.2f' % (last_data["amount"] / 100000000), **normal_font)

    ap = []
    # 通过金融库 talib 生成移动平均线，为了生成没空白的，使用原数据
    N = [5, 10, 20, 60]
    for i in N:
        df['MA' + str(i)] = ta.EMA(df['Close'], timeperiod=i)
    # 通过ax=ax1参数指定把新的线条添加到ax1中，与K线图重叠
    # 通过ax=ax1参数指定把新的线条添加到ax1中，与K线图重叠，注意均线切片iloc[20:147]与ax1时间维度一样
    ap.append(mpf.make_addplot(df[['MA5', 'MA10', 'MA20', 'MA60']].iloc[start_index:end_index], ax=ax1))

    # 通过金融库 talib 生成MACD指标，
    short_win = 12  # 短期EMA平滑天数
    long_win = 26  # 长期EMA平滑天数
    macd_win = 9  # DEA线平滑天数
    macd_tmp = ta.MACD(df['Close'], fastperiod=short_win, slowperiod=long_win, signalperiod=macd_win)
    DIF = macd_tmp[0][start_index:end_index]
    DEA = macd_tmp[1][start_index:end_index]
    MACD = macd_tmp[2][start_index:end_index]

    # 生成一个空列表用于存储多个addplot
    # 在ax3图表中绘制 MACD指标中的快线和慢线
    ap.append(mpf.make_addplot(DIF, ax=ax3))
    ap.append(mpf.make_addplot(DEA, ax=ax3))
    # 使用柱状图绘制快线和慢线的差值，根据差值的数值大小，分别用红色和绿色填充
    # 红色和绿色部分需要分别填充，因此先生成两组数据，分别包含大于零和小于等于零的数据
    bar_r = np.where(MACD > 0, MACD, 0)
    bar_g = np.where(MACD <= 0, MACD, 0)
    # 使用柱状图填充（type='bar')，设置颜色分别为红色和绿色
    ap.append(mpf.make_addplot(bar_r, type='bar', color='red', ax=ax3))
    ap.append(mpf.make_addplot(bar_g, type='bar', color='green', ax=ax3))

    # 注意添加均线参数，macd, addplot=ap
    mpf.plot(df_data,
             ax=ax1,
             volume=ax2,
             addplot=ap,
             style=m_style,
             type='candle')
    fig.show()


if __name__ == '__main__':
    kline('000001', '2022-01-01', '2022-09-30')
    pass