from loguru import logger
import sys

# 日志级别: 
# debug 调试信息打印日志比较详细，级别最低
# info 正常的提示信息，级别较低
# waring 警告信息，不影响代码往下运行，级别较高
# error  出错了，级别最高

# 日志级别排序
# DEBUG < INFO < WARNING < ERROR

logger.remove()   # 删掉默认设置
fmt = '[{time}][{level}][{file.path}:line:{line}:function_name:{function}] || msg={message}'
logger.add(sys.stdout,format=fmt,level="DEBUG") # 系统标准输出，设置日志级别并在控制台打印出来，是打印此级别以上的日志
logger.add("a.log",format=fmt,level="DEBUG",encoding="utf-8",enqueue=True,rotation="1 day")  # 将日志写入文件
# enqueue=True,异步写日志
# rotation可以设置大小，超过多大就产生一个新文件 1 kb ,500 m ,1 g
# rotation可以多长时间，1 day   1 hour
# rotation几点创建新文件，00:00  1:00
# retention = 7 days #多长时间后会删除以前产生的日志,当前的日志不会受影响
logger.add('a.log', level='DEBUG', encoding='utf-8', enqueue=True, rotation='20 kb')  # 文件超过多大就新生成一个新文件
logger.add('a.log', level='DEBUG', encoding='utf-8', enqueue=True, rotation='01:00')  # 每天1点创建新文件
logger.add('a.log', level='DEBUG', encoding='utf-8', enqueue=True, rotation='2 week')  # 文件超过2周就清理掉
logger.add('a.log', level='DEBUG', encoding='utf-8', enqueue=True, retention='7 days')  # 7天后会删除之前产生的日志

logger.debug("debug") # 打印信息比较多
logger.info("info")   # 正常的提示信息
logger.warning("warning") # 警告
logger.error("error")  # 错误
