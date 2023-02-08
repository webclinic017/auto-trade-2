
import os

# currentdir = os.path.split(os.path.realpath(__file__))[0] # "./"
tmp_path = os.path.join("./", "tmp")
if not os.path.exists(tmp_path):
     os.makedirs(tmp_path)

config_path =  os.path.join(tmp_path, "config.csv") 
sh_code_path =  os.path.join(tmp_path, "sh_code.csv") 
sz_code_path = os.path.join(tmp_path, "sz_code.csv")

# date format： %Y%m%d
start_date = "20000101"

# text_font = r"C:\Windows\Fonts\STFANGSO.TTF"

# https://github.com/StellarCN/scp_zh/blob/master/fonts/SimHei.ttf
# windows
# text_font = r"D:\下载\SimHei.ttf"
# mac
text_font = r"/Users/afirez/Downloads/SimHei.ttf" 


