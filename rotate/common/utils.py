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


def init_logger():
    logging.basicConfig(
        format='%(asctime)s : %(levelname)s : %(message)s',
        level=logging.DEBUG,
        handlers=[logging.StreamHandler()])
