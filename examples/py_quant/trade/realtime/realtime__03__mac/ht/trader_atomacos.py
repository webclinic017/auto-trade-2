import time
import atomacos

app = atomacos.getAppRefByBundleId('cn.com.htzq.macstock')  # 替换为目标应用的 bundle id
window = app.windows()[0]  # 获取窗口

print(window.findAll())

# 查找 table 元素
table = None
for element in window.elements():
    if element.AXRole == 'AXTable':
        table = element
        break

if table is None:
    print('找不到 table 元素')
    exit()

# 遍历 table 的所有行和列
for row in table.AXRows:
    for cell in row.AXCells:
        print(cell.AXValue)