import logging
from utils.path_tool import get_abs_path
import os
from datetime import datetime

# 日志保存的根目录
LOG_ROOT = get_abs_path('logs')

os.makedirs(LOG_ROOT, exist_ok=True)

# 日志的格式配置 error info debug
DEFAULT_LOG_FORMAT = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s',
)

# 创建一个日志器，既能打印到控制台，又能保存到文件
def get_logger(name: str = 'agent', console_level: int = logging.INFO, file_level: int = logging.DEBUG,
               log_file=None) -> logging.Logger:
    """

    :param name:日志器名字
    :param console_level:控制台显示什么级别
    :param file_level:文件记录什么级别
    :param log_file:日志文件名
    :return:
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # 避免重复添加Handler
    if logger.hasHandlers():
        return logger

    # 控制台Handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(console_level)
    console_handler.setFormatter(DEFAULT_LOG_FORMAT)

    logger.addHandler(console_handler)

    # 文件Handler 每天一个新文件 名字格式：agent_20250423.log
    if not log_file:
        log_file = os.path.join(LOG_ROOT, f"{name}_{datetime.now().strftime('%Y%m%d')}.log")


    file_handler = logging.FileHandler(log_file,encoding='utf-8')
    file_handler.setLevel(file_level)
    file_handler.setFormatter(DEFAULT_LOG_FORMAT)

    logger.addHandler(file_handler)

    return logger

# 快捷获取日志器
logger = get_logger()

if __name__ == '__main__':
    logger.info('信息日志')
    logger.error('错误日志')
    logger.warning('警告日志')
    logger.debug('调试日志')

