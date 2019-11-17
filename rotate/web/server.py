#-*- coding:utf-8 -*-
from flask import Flask,jsonify,request,render_template
import logging
import  threading
import base64
from common import utils
import os
import conf
from common.file import LabelDoneProcessor

utils.init_logger()
app = Flask(__name__)
person_img_num = 2000
logger = logging.getLogger("WebServer")
lock = threading.Lock()
logger = logging.getLogger(__name__)

@app.route("/")
def index():
    return render_template('index.html',version="version")


def load_img_base64(img_local_path):
    if not os.path.exists(img_local_path):
        logger.warning("样本文件找不到啊：%s",img_local_path)
        return None
    with open(img_local_path, 'rb') as img_f:
        img_stream = img_f.read()
        img_stream = base64.b64encode(img_stream)
    return str(img_stream,'utf-8')

# 取其中的一张图
def get_one_image(user_name):
    user_file_path = utils.get_label_file_path(user_name)

    from common.file import ReadFile
    fp = ReadFile(user_file_path)
    line,num = fp.read_one_line() # num=-1意味着没有剩余了

    logger.debug("获得标注图片：%s",line)
    return line,num

# 得到用户目前的状态
def get_status(user_name):
    # 用户目录
    user_path = os.path.join(conf.data_root,conf.everyone_dir,user_name)
    # 用户标注的文件
    txt_path = os.path.join(user_path,conf.label_txt)
    logger.debug("用户目录：%s",user_path)
    logger.debug("用户文件：%s",txt_path)

    if not os.path.exists(txt_path):
        logger.info("用户路径[%s]不存在",txt_path)
        return False
    else:
        return True

# 开始标注任务
@app.route('/start.label',methods=['GET'])
def start():
    username = request.args['username']
    if not get_status(username):
        # 没有领任务
        logger.info("[%s]未曾领受任务，启动进程领受任务",username)
        t = InitialUserSpaceThread(username)
        t.start()
        t.join()

    # 已经有任务,获取第一张图片
    logger.info("邮箱前缀为" + username + "，开始获取第一张图片")
    img_path,num = get_one_image(username) #num: -1意味着没有剩余了
    if img_path is None:
        img_stream = ""
        logger.info("邮箱前缀为" + username + "没有图片可以标注了")
    else:
        img_stream = load_img_base64(img_path)
        logger.info("邮箱前缀为" + username + "的图片获取成功")

    return jsonify({'img_stream': str(img_stream),'img_path':img_path,'remain':num})

# 这个线程类，用来从大库里领取文件
class InitialUserSpaceThread(threading.Thread):
    def __init__(self,args):
        threading.Thread.__init__(self)
        self.args = args
    def run(self):
        if lock.acquire():
            logger.info("邮箱前缀为" + self.args + "的任务开始执行")
            # time.sleep(3)
            from common.file import AssignFileProcessor
            user_file_path = utils.get_label_file_path(self.args)
            raw_file_path = os.path.join(conf.data_root,conf.raw_txt)
            afp = AssignFileProcessor(raw_file_path,user_file_path,conf.task_num_person)
            afp.process()
            logger.info("邮箱前缀为" + self.args + "的任务获取成功")
            lock.release()

# 图片标注
@app.route('/label',methods=['POST'])
def label():
    username = request.json.get('username')
    type = request.json.get('type')
    img_path = request.json.get('img_path')
    label_me(username,type,img_path)
    return 'ok'

# 如果正确的图片移到good下，错误的图片移到bad下
def label_me(user_name,type,img_path):
    user_label_file_path = utils.get_label_file_path(user_name)
    user_label_done_file_path = utils.get_label_done_file_path(user_name)
    ldp = LabelDoneProcessor(user_label_file_path,user_label_done_file_path)
    ldp.do(img_path,type)


if __name__ == '__main__':

    app.run(debug=True, port=8082)