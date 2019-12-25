import os
import logging
logger = logging.getLogger(__name__)
'''
everyone!
    |
    |--[chuangliu18]
    |       |
    |       |--label.txt # 打标文件，会一行行更新
    |       |--check.txt # 复检文件，会一条条的被搬运到good/bad里
    |       |--good.txt  # 正确的文件，会一条条添加
    |       |--bad.txt   # 错误的文件，会一条条添加
    |
    |-raw.txt   # 最开始的原始文件
    |-train.txt # 从用户的label.txt合并后的文件（靠batch）
'''

# 常量设置
MODE_CHECK = "check"
MODE_ROTATE = "rotate"
ACTION_GOOD = "good"
ACTION_BAD = "bad"
ACTION_LABEL = "label"
ACTION = 'action'

# 模式：目前支持2中：校验check、和4方向标注rotate
mode= MODE_CHECK

# 返回缩放的图片
resize=0.3

# 每个人的任务数
task_num_person = 1000

# data root目录
data_root = "data"

# 总的图片目录txt文件位置
train_txt = 'train.txt'

#
raw_txt = 'raw.txt'

#
label_txt = 'label.txt'

#
check_txt = 'check.txt'

#
label_done_txt = 'label.done.txt'

#
bad_bill_txt = 'bad.bill.txt'

# 分出图片的路径
everyone_dir = "everyone"

# 正确文件路径
good_txt = 'good.txt'

# 错误文件路径
bad_txt = 'bad.txt'

def get_raw_txt_path():
    raw_txt_path = os.path.join(data_root,raw_txt)
    if not os.path.exists(raw_txt_path):
        logger.error("原始文件不存在啊：%s",raw_txt_path)
        return None
