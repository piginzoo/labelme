import conf
import os
import logging

logger = logging.getLogger(__name__)

def __get_file_path(user_name):
    user_dir = os.path.join(conf.data_root, conf.everyone_dir, user_name)
    logger.info("邮箱前缀为" + user_name + "的用户的文件路径为" + user_dir)
    if not os.path.isdir(user_dir):
        logger.info("用户[%s]目录不存在，创建他", user_name)
        os.makedirs(user_dir)
    return user_dir

def get_label_file_path(user_name):
    user_dir = __get_file_path(user_name)

    # 用户对应的txt
    user_txt_path = os.path.join(user_dir, conf.label_txt)
    logger.debug("根据用户名[%s]，得到标签文件Label.txt路径：%s",user_name,user_txt_path)
    return user_txt_path

def get_label_done_file_path(user_name):
    user_dir = __get_file_path(user_name)
    # 用户对应的txt
    user_txt_path = os.path.join(user_dir, conf.label_done_txt)
    logger.debug("根据用户名[%s]，得到完成标签Label.Done.txt文件路径：%s",user_name,user_txt_path)
    return user_txt_path


def get_bad_txt_file_path(user_name):
    user_dir = __get_file_path(user_name)
    # 用户对应的txt
    bad_bill_txt_path = os.path.join(user_dir, conf.bad_bill_txt)
    logger.debug("根据用户名[%s]，得到完成标签Label.bad.txt文件路径：%s", user_name, bad_bill_txt_path)
    return bad_bill_txt_path

import time
from logging import handlers
def init_logger(dir="logs",
         level=logging.DEBUG,
         when="D",
         backup=30,
         _format="%(levelname)s: %(asctime)s: %(filename)s:%(lineno)d行 %(message)s"):

    train_start_time = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
    filename = dir+'/log-'+train_start_time + '.log'
    print("日志文件：", filename)
    _dir = os.path.dirname(filename)
    if not os.path.isdir(_dir):os.makedirs(_dir)

    logger = logging.getLogger()

    logger.setLevel(level)
    print("设置日志等级：",level)

    formatter = logging.Formatter(_format)

    handler = handlers.TimedRotatingFileHandler(filename, when=when, backupCount=backup)

    handler.setLevel(level)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    print("设置日志文件输出方式：",filename,"/",level,"/",when,"/",backup)

    handler = logging.StreamHandler()
    handler.setLevel(level)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    print("设置日志屏幕打印输出方式")