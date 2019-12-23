import os
import logging
from commons import utils

logger = logging.getLogger(__name__)

'''
everyone!
    |
    |--[chuangliu18]
    |       |
    |       |--label.txt # 打标文件，会一行行更新
    |       |--label.done.txt # 打标文件，会一行行更新
    |       |--check.txt # 复检文件，会一条条的被搬运到good/bad里
    |       |--good.txt  # 正确的文件，会一条条添加
    |       |--bad.txt   # 错误的文件，会一条条添加
    |
    |-raw.txt   # 最开始的原始文件
    |-train.txt # 从用户的label.done.txt合并后的文件（靠batch）
    
python的文件处理方式：
    r  只能读 
    r+ 可读可写，不会创建不存在的文件。如果直接写文件，则从顶部开始写，覆盖之前此位置的内容，如果先读后写，则会在文件最后追加内容 
    w+ 可读可写，如果文件存在 则覆盖整个文件不存在则创建 
    w  只能写，  覆盖整个文件 不存在则创建 
    a  只能写，  从文件底部添加内容 不存在则创建 
    a+ 可读可写，从文件顶部读取内容 从文件底部添加内容 不存在则创建
'''

# 标注，用于把label.txt=>label.done.txt中
# 也支持回滚，只要把do(image=None)即可，他使用done文件中的最后一行
class LabelDoneProcessor:
    def __init__(self,src_path,dst_path):
        # if not os.path.exists(src_path):
        #     raise FileExistsError("源文件不存在："+label_path)
        self.src_path = src_path
        self.dst_path = dst_path

    # 标注为坏样本
    def bad(self):
        return self.__do(None,None)

    # 标注为好样本
    def good(self):
        return self.__do(None,None)

    # 标注他
    def label(self,image,label):
        return self.__do(image,label)

    # 回滚他
    def rollback(self):
        return self.__do(None,None)

    # image,label=None的时候，只是把label.txt/good.txt最后一行，搬家到bad.txt而已，不做处理
    def __do(self,image,label):

        # 读源src文件，取出最后一行

        if not os.path.exists(self.src_path):
            logger.error("源src文件[%s]不存在",self.src_path)
            return "文件不存在："+self.src_path

        src_file = open(self.src_path, "r+")
        src_lines = src_file.readlines()
        if len(src_lines)==0:
            logger.warning("源src文件[%s]已经没有内容了，无法往目标dst文件搬运了",self.src_path)
            return "到头了，无法回滚了"
        src_left_lines = src_lines[:-1] # 去除最后一行，剩下的行
        last_line = src_lines[-1]  # 去除最后一行
        src_file.close() # 先把src文件关上

        # 更新源src文件
        new_src_file = open(self.src_path,"w")
        new_src_file.writelines(src_left_lines)
        new_src_file.close()
        logger.debug("源src文件已更新（去除了最后一行）：%s",self.src_path)

        # 追加源src的最后一行到目标dst文件中
        dst_file = open(self.dst_path, "a")

        # 这个不考虑前台传过的内容，只用源src文件的最后一行
        if image is None:
            try:
                content = utils.get_rollback_line(last_line)
            except Exception as e:
                str = "解析行错误{}:{}".format(last_line, str(e))
                logger.error(str)
                dst_file.close()
                return str
        else:
            content = image + " " + label

        dst_file.write(content)
        logger.debug("目标dst文件尾部插入：%s", content)
        dst_file.write("\n")
        dst_file.close()
        logger.debug("目标dst文件更新：%s", self.dst_path)
        return 'ok'

# 处理把一个文件中的N行放到另外一个文件中
class AssignFileProcessor:

    def __init__(self,src_path,dst_path,assign_num):
        if not os.path.exists(src_path):
            raise FileExistsError("源文件不存在："+src_path)

        self.src_file = open(src_path,"r")
        self.src_path = src_path

        self.dst_file = open(dst_path,"w")
        self.dst_path = dst_path
        self.assign_num = assign_num


    def close(self):
        self.src_file.close()
        self.dst_file.close()

    def process(self):

        lines = self.src_file.readlines()
        logger.debug("原始文件%d行",len(lines))
        if self.assign_num >= len(lines):
            logger.debug("需要分配的行数[%d]大于文件行数[%d]",self.assign_num,len(lines))
            dst_lines = lines
            src_lines = []
        else:
            dst_lines = lines[:self.assign_num]
            src_lines = lines[self.assign_num:]

        self.dst_file.writelines(dst_lines)
        new_src_file = open(self.src_path,"w")
        new_src_file.writelines(src_lines)
        new_src_file.close()

        logger.debug("保存了目标文件：%s,%d行",self.dst_path,len(dst_lines))
        logger.debug("保存了源文件：%s,%d行", self.src_path, len(src_lines))

        self.close()


# 专门为打标设计的文件，每次更新"第一行"，更新的时候，按照image去查找，更新对应的label
class ReadFile:
    def read_one_line(self):
        lines = self.file.readlines()
        self.file.close()
        if len(lines)==0:
            logger.debug("无法读出最后一行，无数据了")
            return None,-1 # -1意味着没有剩余了
        logger.debug("读出标签文件中的最后一行：%s",lines[0])
        return lines[-1].strip(),len(lines) - 1

    def __init__(self, file_path):
        if not os.path.exists(file_path):
            raise FileExistsError("文件不存在："+file_path)
        self.file_path = file_path
        self.file = open(file_path,"r")


