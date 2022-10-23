# -*- coding: utf-8 -*-


# 注意：由于近期接口地址有变动，pip安装或升级完毕，
# 需要按如下替换步骤更新后方可使用如下代码，
# 否则将无法访问到数据，或者程序接口会报错。
# (如无法访问，详见http://t.csdn.cn/nVWS7)
# =导入问财包=
# 安装：pip install wencai
# 升级：pip install wencai --upgrade
# 替换：将我的压缩包解压，覆盖python安装目录下Lib\site-packages\下的wencai目录。（个别地址和函数有修改，修改后才可以使用wencai及更好的使用问财）


# 文件名：wencai_xg.py
import wencai as wc
# 若需中文字段则cn_col=True,chromedriver路径不在根目录下需指定execute_path
wc.set_variable(cn_col=True)

def xg_wencai(query,perpage=20):
    '''
    功能：调用问财接口筛选股票
    参数：query查询条件，perpage反馈的条目数
    '''
    import wencai as wc
    # 若需中文字段则cn_col=True,chromedriver路径不在根目录下需指定execute_path
    wc.set_variable(cn_col=True)
    r = wc.search(query,perpage)
    return r.round(3)

if __name__ == '__main__':
    # 实用基础篇
    if 1:
    	# 选股条件
        query = '非st；非停牌；股价大于5元；流通市值50亿到750亿；股价突破444日均线；'
        # 控制一次最多选多少支股票
        perpage = 10
        df = xg_wencai(query,perpage)
        print(df)
        # df_table(df,query)
        # 写入EXCEL文件
        df.to_excel("xg_wencai.xlsx", encoding="utf8")
        # 有人说我只要股票代码
        code_list = df['股票代码'].values.tolist()
        # 取5只股票代码
        print(code_list[0:5]) 
