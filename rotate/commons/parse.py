#coding=utf-8
'''
用于解析ali的调用结果

1. 遍历文件夹读取文件夹中的json文件和image图片
2. 拿出json将坐标信息整理成新的文件
3. 将新的坐标文件和对应的图片文件存入到新的位置

find . -name "*.json"|xargs -I {} cp {} ~/Downloads/ocr_labels
find . -name "*.JPG" |xargs -I {} cp {} ~/Downloads/ocr_images
'''
import os
import json
import shutil
import time
import sys
import logging
from tqdm import tqdm

logger = logging.getLogger(__name__)

OUTPUT_JSONS="ocr_jsons"
OUTPUT_LABELS="ocr_labels"
OUTPUT_IMAGES="ocr_images"

json_list = os.listdir(OUTPUT_JSONS)

# 根据image名字查找对应的json文件名字
# ocr_o_zvh7ompl1572337865068_srzp6iku1572338057163_2607751124123628233.JPG  ==>
# ocr_alij_zvh7ompl1572337865068_wZqMcZHA1572338061470_3168825272996898667.json
def get_json_file_name(image_name):
    names = image_name.split("_")
    for json_file_name in json_list:
        json_names = json_file_name.split("_")
        if names[2] == json_names[2] and \
           names[3] == json_names[3]:
           return os.path.join(OUTPUT_JSONS,json_file_name)
    return None

def init_logger():
    logname = 'log.txt'
    formatter = '%(asctime)s : %(levelname)s : %(message)s' 

    fh = logging.FileHandler(logname, mode='w', encoding='utf-8')
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)

    logging.basicConfig(format=formatter,level=logging.DEBUG,
        handlers=[logging.StreamHandler(),fh])


# 遍历指定目录，显示目录下的所有文件名
# 20190930/AHNSYH/ocr_alij_8lqkOy4w1569807700899_4maFLEqb1569807894382_1206319688692093944.jpg
count = 0
def process_dir(images_dir):
    global count
    dirs = os.listdir(images_dir)
    pbar = tqdm(total=len(dirs))
    for dir_or_file_name in dirs:
        
        # 得到纯文件名，不包含路径，包含后缀
        file_name = os.path.basename(dir_or_file_name)
        # 后缀
        name,subfix = os.path.splitext(file_name)

        # 找到图片文件    
        if (subfix == '.jpg' or subfix == '.JPG'):
            count = count +1
            # 处理每张图片，只传入
            try:
            	process_one_image(file_name,name)
            except Exception as e:
            	logger.error("解析发生错误：[%s]%s",file_name,str(e))
        pbar.update(1)    
    logger.debug("共有" + str(count) + "个文件")

# 读取文件内容并打印,prefix_name是不包含文件后缀的名字
def process_one_image(image_name,prefix_name):
    # ocr_o_zvh7ompl1572337865068_srzp6iku1572338057163_2607751124123628233.JPG
    # ocr_alij_zvh7ompl1572337865068_wZqMcZHA1572338061470_3168825272996898667.json
    json_file_path = get_json_file_name(prefix_name)

    if json_file_path is None:
        logger.warning("图片[%s]对应的json文件不存在！",image_name)
        return
    if not os.path.exists(json_file_path):
        logger.warning("图片[%s]对应的json文件[%s]不存在！",image_name,json_file_path)
        return
    label_file_path = os.path.join(OUTPUT_LABELS,prefix_name+".txt")	
    logger.debug("正在处理json文件：%s=>%s",json_file_path,label_file_path)
    json_file =  open(json_file_path, 'r') 
    

    for content in json_file:
        # logger.debug("读取到得内容如下：%s", content)
        result = parse_json(content)
        if result!='':
            write_lable_file(label_file_path,result)
        else:
            logger.warnning("处理json文件有问题：%s",image_name)
    json_file.close()

# 输入多行文字，写入指定文件并保存到指定文件夹
def write_lable_file(label_file_path,result):
    label_file = open(label_file_path, 'w')
    label_file.write('%s%s' % (result, os.linesep))
    label_file.close()

# 解析json结构
def parse_json(content):
    jsonLine = json.loads(content)
    prism_wordsInfo = jsonLine['prism_wordsInfo']
    result = ''
    for info in prism_wordsInfo:
        dataList = []
        word = info['word']
        for pos in info['pos']:
            x = pos['x']
            y = pos['y']
            dataList.append(x)
            dataList.append(y)
        dataList.append(word)
        dataStr = str(dataList).replace("[","").replace("]","").replace("\\","") + '\n'
        result = result + dataStr
    return result



if __name__ == '__main__':
    init_logger()
    if not os.path.exists(OUTPUT_LABELS):
    	os.mkdir(OUTPUT_LABELS)
    process_dir(OUTPUT_IMAGES)