import logging
import os
import conf
import utils
from main.file import AssignFile

logger = logging.getLogger(__name__)

# 用户拿到自己的任务列表
# @assign_num: 被分配的个数
# @user_name:  用户唯一的id表示，用来创建文件夹
def get_task_by_person(assign_num,user_name):

    # 读取总的大库 data/train.txt => [chuangliu]/chuangliu.txt
    train_txt_path = os.path.join(conf.data_root,conf.train_txt)
    user_file_path = utils.get_file_path(user_name)

    assign_file_processor = AssignFile(train_txt_path,user_file_path,assign_num)
    assign_file_processor.process()


#
if __name__ == '__main__':

    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--dir")
    parser.add_argument("--assign_num")
    parser.add_argument("--user_name")

    args = parser.parse_args()
    # 数据位置
    DATA_DIR = args.dir
    # 每个人一次拿的图片数
    assign_num = int(args.assign_num)
    # 邮箱前缀
    user_name = args.user_name
    get_task_by_person(assign_num,user_name)

