import inspect
import logging
import os
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler

import colorlog

try:
    from config import BASE_PATH
except:
    BASE_PATH = os.path.dirname(os.path.abspath(__file__))

LOG_PATH = os.path.join(os.path.join(BASE_PATH,"tmp"), "logs")


def message(func):
    def wrapper(_self, message):
        frame, filename, lineNo, functionName, code, unknowField = inspect.stack()[
            1]
        filename = os.path.basename(filename)
        message = "[{}:{}] [{}] - {}".format(filename,
                                             lineNo, functionName, message)
        func(_self, message)
    return wrapper


class Log(object):
    def __init__(self):
        self.info_log_path = os.path.join(LOG_PATH, "info")
        self.debug_log_path = os.path.join(LOG_PATH, "debug")
        self.warning_log_path = os.path.join(LOG_PATH, "warning")
        self.error_log_path = os.path.join(LOG_PATH, "error")
        self.critical_log_path = os.path.join(LOG_PATH, "critical")
        self.notset_log_path = os.path.join(LOG_PATH, "notset")
        self.log_dir_check()

        self.logs_handlers = None
        self.init_handlers()

        self.__loggers = dict()
        self.log_colors_config = {
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'red',
            'NOTSET': 'red'
        }
        self.init_loggers()

    def log_dir_check(self):
        if not os.path.exists(LOG_PATH):
            os.makedirs(LOG_PATH)
        for path in [self.info_log_path, self.error_log_path, self.debug_log_path, self.warning_log_path, self.error_log_path, self.critical_log_path, self.notset_log_path]:
            if not os.path.exists(path):
                os.makedirs(path)

    def init_handlers(self):
        logs_handler_paths = {
            RotatingFileHandler: {
                logging.WARNING: os.path.join(self.warning_log_path, 'warning.log'),
                logging.ERROR: os.path.join(self.error_log_path, 'error.log'),
                logging.CRITICAL: os.path.join(self.critical_log_path, 'critical.log'),
            },
            TimedRotatingFileHandler: {
                logging.NOTSET: os.path.join(self.notset_log_path, 'notset.log'),
                logging.DEBUG: os.path.join(self.debug_log_path, 'debug.log'),
                logging.INFO: os.path.join(self.info_log_path, 'info.log'),
            }
        }
        log_handler_params = {
            TimedRotatingFileHandler: dict(when='midnight', interval=1, backupCount=10, encoding="utf-8"),
            RotatingFileHandler: dict(
                maxBytes=1024 * 1024, backupCount=10, encoding="utf-8")
        }
        self.logs_handlers = {log_level: log_handler(
            log_path, **log_handler_params[log_handler]) for log_handler, log_level_paths in logs_handler_paths.items() for log_level, log_path in log_level_paths.items()}

    def init_loggers(self):
        def should_log(record):
            """
            定义日志过滤规则
            :param record: 日志信息,拥有日志的自有属性,如 lineno
            :return: True or False
            """
            if record.levelname not in ["INFO", "WARNING", "DEBUG"]:
                return False
            return True

        _ = '%(log_color)s[%(asctime)s] [%(levelname)s] %(message)s'
        formatter = colorlog.ColoredFormatter(
            _, log_colors=self.log_colors_config)

        for log_level, log_handler in self.logs_handlers.items():
            logger = logging.getLogger(str(log_level))

            logger.propagate = False  # 阻止向 root 传播，True会导致console两次
            logger.setLevel(log_level)
            # 一些 handler
            log_handler = log_handler
            console = logging.StreamHandler()

            # 为刚创建的日志记录器设置日志记录格式
            log_handler.setFormatter(formatter)
            console.setFormatter(formatter)

            # 对日志器等级进行配置
            console.setLevel(log_level)
            log_handler.setLevel(log_level)

            # 初始化日志过滤器,并添加至 console
            # logging_filter = logging.Filter()
            # logging_filter.filter = should_log
            # console.addFilter(logging_filter)

            # 设置 TimedRotatingFileHandler 后缀名称，跟 strftime 的格式一样
            if TimedRotatingFileHandler == type(log_handler):
                log_handler.suffix = "%Y-%m-%d_%H-%M-%S.log"

            # 为日志工具对象添加日志记录器
            logger.addHandler(console)
            logger.addHandler(log_handler)

            self.__loggers.update({log_level: logger})

    @message
    def info(self, message):
        self.__loggers[logging.INFO].info(message)

    @message
    def error(self, message):
        self.__loggers[logging.ERROR].error(message)

    @message
    def exception(self, message):
        self.__loggers[logging.ERROR].exception(message)

    @message
    def warning(self, message):
        self.__loggers[logging.WARNING].warning(message)

    @message
    def debug(self, message):
        self.__loggers[logging.DEBUG].debug(message)

    @message
    def critical(self, message):
        self.__loggers[logging.CRITICAL].critical(message)


logger = Log()

if __name__ == "__main__":
    logger.info("info")
    logger.error("error")
    logger.debug("debug")
    try:
        a = 0/0
    except Exception as e:
        logger.exception(e)
    logger.warning("warning")
    logger.critical("critical")
