# 作者：博客园_杠上花
# 邮箱: a2578629964@163.com
# 时间：2022年1月20日
# 编码：utf-8
# 版本：python3.8
import logging
from logging import handlers
from pyfiglet import Figlet


def create_log():
    # CRITICAL > ERROR > WARNING > INFO > DEBUG > NOTSET
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    # 2.生成 handler 对象
    all_handler = handlers.TimedRotatingFileHandler('log/all.log', when='midnight', interval=1, backupCount=7)
    all_handler.setFormatter(
        logging.Formatter(
            "%(asctime)s %(process)d %(threadName)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s"))

    error_handler = logging.FileHandler('log/error.log')
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(
        logging.Formatter(
            '%(asctime)s %(process)d %(threadName)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s'))

    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('%(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)
    logger.addHandler(all_handler)
    logger.addHandler(error_handler)
    return logger

def get_banner(text, font='graffiti'):
    custom_fig = Figlet(font=font)
    return custom_fig.renderText(text)


