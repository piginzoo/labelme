import os
import logging

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

class LabelDoneProcessor:
    def __init__(self,label_path,label_done_path):
        if not os.path.exists(label_path):
            raise FileExistsError("源文件不存在："+label_path)

        self.label_file = open(label_path,"r+")
        self.label_path = label_path

        self.label_done_file = open(label_done_path,"a")
        self.label_done_path = label_done_path

    def do(self,image,label):
        lines = self.label_file.readlines()
        if len(lines)==0:
            logger.warning("个人标注文件已经没有内容了")
            return False
        lines = lines[1:] # 去除第一行
        self.label_file.close()

        new_label_file = open(self.label_path,"w")
        new_label_file.writelines(lines)
        new_label_file.close()
        logger.debug("个人标注文件已更新：%s",self.label_path)

        self.label_done_file.write(image+" "+label)
        self.label_done_file.write("\n")
        self.label_done_file.close()
        logger.debug("个人标注完成文件(Done)已更新：%s", self.label_done_path)


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
            logger.debug("无法读出第一行，无数据了")
            return None,-1 # -1意味着没有剩余了
        logger.debug("读出标签文件中的第一行：%s",lines[0])
        return lines[0].strip(),len(lines) - 1

    def __init__(self, file_path):
        if not os.path.exists(file_path):
            raise FileExistsError("文件不存在："+file_path)
        self.file_path = file_path
        self.file = open(file_path,"r")


