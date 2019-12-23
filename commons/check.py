
import logging
import random
import os
import shutil
import sys

import conf





# 如果正确的图片移到good下，错误的图片移到bad下
def move_img_good_or_bad(user_name,type,img_path):
    user_path = os.path.join('%s%s' % (conf.person_path, user_name))
    to_good_path =  os.path.join('%s%s%s' % (conf.person_path, user_name, good_path))
    to_bad_path =  os.path.join('%s%s%s' % (conf.person_path, user_name, bad_path))
    if type=='good':
        if not os.path.isdir(to_good_path):
            os.mkdir(to_good_path)
        moveFileto(img_path,to_good_path)
    else:
        if not os.path.isdir(to_bad_path):
            os.mkdir(to_bad_path)
        moveFileto(img_path,to_bad_path)

    # 修改src下的txt文件
    txt_name = os.path.join('%s%s' % (user_name, '.txt'))
    txt_path = os.path.join('%s%s%s' % (user_path, '/', txt_name))
    file = open(txt_path, 'r')
    lines = file.readlines()  # 读取所有行
    label = lines[0]
    with open(txt_path, "w", encoding="utf-8") as f_w:
        for line in lines:
            if lines[0] in line:
                continue
            f_w.write(line)
    # 写入good或者bad文件夹中的txt
    write_label_to_newfile(label,user_name,type)
    return len(lines)

# 将label写入该用户的good文件夹或者bad文件夹
def write_label_to_newfile(label,user_name,type):
    user_txt_name = os.path.join('%s%s' % (user_name, ".txt"))
    # 源文件路径
    new_txt_path = ''
    if type == 'good':
        new_txt_path = os.path.join('%s%s%s%s%s%s' % (conf.person_path, user_name ,"/",good_path,"/",user_txt_name))
    else:
        new_txt_path = os.path.join('%s%s%s%s%s%s' % (conf.person_path, user_name ,"/",bad_path,"/",user_txt_name))
    logger.info("将label加入到%s",new_txt_path)
    fopen = open(new_txt_path, 'a+')
    write_txt = label
    fopen.write('%s%s' % (write_txt, os.linesep))
    fopen.close()




# 将label写入该用户的good文件夹或者bad文件夹
def write_label_to_newfile(label,user_name,type):
    user_txt_name = os.path.join('%s%s' % (user_name, ".txt"))
    # 源文件路径
    new_txt_path = ''
    if type == 'good':
        new_txt_path = os.path.join('%s%s%s%s%s%s' % (conf.person_path, user_name ,"/",good_path,"/",user_txt_name))
    else:
        new_txt_path = os.path.join('%s%s%s%s%s%s' % (conf.person_path, user_name ,"/",bad_path,"/",user_txt_name))
    logger.info("将label加入到%s",new_txt_path)
    fopen = open(new_txt_path, 'a+')
    write_txt = label
    fopen.write('%s%s' % (write_txt, os.linesep))
    fopen.close()

def moveFileto(sourceDir,  targetDir):
    shutil.move(sourceDir,  targetDir)


#
if __name__ == '__main__':

    import argparse

    init_logger()
    # 邮箱前缀
    user_name = 'hengyang4'
    img_path = get_img_in_src(user_name)

