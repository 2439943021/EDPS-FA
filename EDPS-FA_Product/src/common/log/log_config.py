import configparser
import sys
from loguru import logger
from datetime import datetime
import os

# print("当前工作目录:", os.getcwd())
# 创建ConfigParser对象
config = configparser.ConfigParser()
# 读取配置文件
config.read('src/common/config/log_config.ini', encoding='utf-8')
# print("读取的配置文件:", config.sections())
section = "Logging"
# 从配置文件中获取日志目录
log_dir = config.get(section, "log_dir")
interval_hours = config.getint(section, "interval_hours")
backup_count = config.getint(section, "backup_count")


class SimpleLogConfigurator:
    """
    简化的日志配置类，用于配置全局日志文件。
    """

    def __init__(self, log_dir=log_dir, interval_hours=interval_hours, backup_count=backup_count):
        """
        初始化日志配置器
        """
        self.logger = self._configure_logging(log_dir, interval_hours, backup_count)

    def _configure_logging(self, log_dir, interval_hours, backup_count):
        """
        配置全局日志文件
        """
        os.makedirs(log_dir, exist_ok=True)
        logger.remove()  # 清除默认配置

        # 添加日志文件配置
        logger.add(
            sink=os.path.join(log_dir, "daily_log_{time:%Y%m%d}.log"),
            rotation=f"{interval_hours} hours",
            retention=f"{backup_count} days",
            encoding='utf-8',
            enqueue=True,
            backtrace=True,
            diagnose=True,
        )
        # 添加终端输出配置
        logger.add(
            sink=sys.stdout,
            format="<green>{time:YYYY-MM-DD at HH:mm:ss}</green> | <level>{level: <8}</level> | <level>{message}</level>",
            colorize=True
        )

        return logger

# 使用示例
if __name__ == "__main__":
    log_configurator = SimpleLogConfigurator()
    logger = log_configurator.logger

    for _ in range(10):
        logger.info("这是一个信息日志，时间：{}", datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        import time
        time.sleep(1)
