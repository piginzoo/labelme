#-*- coding:utf-8 -*-
from flask import Flask,jsonify,request,render_template,session
import logging
import threading
import base64
import os
from commons.file import LabelDoneProcessor
from commons import utils
import conf
import cv2

utils.init_logger()
app = Flask(__name__)
app.config['SECRET_KEY'] = '123456'
person_img_num = 2000
logger = logging.getLogger("WebServer")
lock = threading.Lock()
logger = logging.getLogger(__name__)

if conf.mode == conf.MODE_CHECK:
    logger.info("2次标注模式")
if conf.mode == conf.MODE_ROTATE:
    logger.info("4方向标注模式")

@app.route("/")
def index():
    return render_template('index.html',version="version")

def load_img_base64(img_local_path):
    if not os.path.exists(img_local_path):
        logger.warning("样本文件找不到啊：%s",img_local_path)
        return None

    image = cv2.imread(img_local_path)
    if conf.resize!=1:
        image = cv2.resize(image,(0,0),fx=conf.resize,fy=conf.resize)
        logger.debug("图片Resize:%f,%s",conf.resize,img_local_path)

    base64_str = cv2.imencode('.jpg',image)[1].tostring()
    img_stream = base64.b64encode(base64_str)
    return str(img_stream,'utf-8')

# 取其中的一张图
def get_one_image(user_name):
    user_file_path = utils.get_label_file_path(user_name)

    from commons.file import ReadFile
    fp = ReadFile(user_file_path)
    line,num = fp.read_one_line() # num=-1意味着没有剩余了

    logger.debug("获得标注图片：%s",line)
    return line,num

# 得到用户目前的状态
def get_status(user_name):
    # 用户标注的文件
    txt_path = utils.get_label_file_path(user_name)
    logger.debug("等待用户标注的文件：%s",txt_path)

    if not os.path.exists(txt_path):
        logger.info("等待用户标注的文件[%s]不存在",txt_path)
        return False
    else:
        return True

# 这个线程类，用来从大库里领取文件
class InitialUserSpaceThread(threading.Thread):
    def __init__(self,args):
        threading.Thread.__init__(self)
        self.args = args
    def run(self):
        if lock.acquire():
            logger.info("邮箱前缀为" + self.args + "的任务开始执行")
            # time.sleep(3)
            from commons.file import AssignFileProcessor
            user_file_path = utils.get_label_file_path(self.args)
            repository_file = utils.get_label_repository_file_path()
            afp = AssignFileProcessor(repository_file,user_file_path,conf.task_num_person)
            afp.process()
            logger.info("邮箱前缀为" + self.args + "的任务获取成功")
            lock.release()

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
    logger.info("邮箱前缀为" + username + "，获取一张图片")
    line,num = get_one_image(username) #num: -1意味着没有剩余了

    if line is None or line.strip()=="" :
        logger.info("邮箱前缀为" + username + "没有图片可以标注了")
        return "" # ""表示任务完成，诡异哈

    cols = line.split()
    # logger.debug(cols)
    if len(cols)==0:
        logger.warning("标签文件中读出的行为空")
        return ""
    if len(cols)==1:
        image_path = cols[0]
        label = ""
    else:
        image_path = cols[0]
        label = " ".join(cols[1:])

    img_stream = load_img_base64(image_path)
    logger.info("[%s]获得[%s]/[%s]",username,image_path,label)

    return jsonify({'img_stream': str(img_stream),'img_path':image_path,'label':label,'remain':num,'mode':conf.mode})

# 图片标注
@app.route('/label',methods=['POST'])
def label():
    __pre_process(conf.ACTION_LABEL)
    username = request.json.get('username')
    img_path = request.json.get('img_path')
    type = request.json.get('type')
    r = __label_me(username,type,img_path)
    if r is None: return 'ok'
    return r

# 图片标注
@app.route('/bad',methods=['POST'])
def bad():
    __pre_process(conf.ACTION_BAD)
    username = request.json.get('username')
    img_path = request.json.get('img_path')
    r = __bad(username)
    if r is None: return 'ok'
    return r

# 返回前一张
@app.route('/rollback',methods=['POST'])
def rollback():
    username = request.json.get('username')
    r = __rollback_me(username)
    if r is None: return 'ok'
    return r

# 图片判定是好的，还是坏的，针对2次check标注完的内容的
@app.route('/good',methods=['POST'])
def good():
    __pre_process(conf.ACTION_GOOD)
    username = request.json.get('username')
    img_path = request.json.get('img_path')
    return __good(username)

# 记录一下动作
def __pre_process(action):
    session[conf.ACTION] = action

# 如果正确的图片移到good下，错误的图片移到bad下
def __good(user_name):
    check_path = utils.get_label_file_path(user_name)
    good_path = utils.get_label_done_file_path(user_name)
    if check_path is None or good_path is None:
        return "无法找到回滚文件"
    ldp = LabelDoneProcessor(src_path=check_path,dst_path=good_path)
    return ldp.good()

# 如果正确的图片移到good下，错误的图片移到bad下
def __rollback_me(user_name):
    src,dst = utils.get_rollback_file_path(user_name,session[conf.ACTION])
    if src is None or dst is None:
        return "无法找到回滚文件"
    ldp = LabelDoneProcessor(src_path=src,dst_path=dst)
    return ldp.rollback()

# 如果正确的图片移到good下，错误的图片移到bad下
def __label_me(user_name,type,img_path):
    user_label_file_path = utils.get_label_file_path(user_name)
    user_label_done_file_path = utils.get_label_done_file_path(user_name)
    ldp = LabelDoneProcessor(user_label_file_path,user_label_done_file_path)
    return ldp.label(img_path,type)

# 如果正确的图片移到good下，错误的图片移到bad下
def __bad(user_name):
    good_path = utils.get_label_file_path(user_name)
    bad_path = utils.get_bad_txt_file_path(user_name)
    ldp = LabelDoneProcessor(good_path,bad_path)
    return ldp.bad()

if __name__ == '__main__':
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=True, port=8082)