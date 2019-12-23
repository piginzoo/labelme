Date=$(date +%Y%m%d%H%M)

if [ ! -e data/raw.txt ]; then
    echo "请先运行 bin/init.sh 初始化data/raw.txt文件"
    exit
fi

if [ "$1" = "stop" ]; then
    echo "停止Web服务器"
    ps aux|grep python|grep labelme_server|awk '{print $2}'|xargs kill -9
    exit
fi

if [ "$1" = "" ]; then
    echo "格式：server.sh <port>"
    exit
fi

backup(){
    Date=$(date +%Y%m%d%H%M%S)
    if [ ! -d "data/backup" ]; then
        mkdir data/backup
    fi
    tar czvf  data/backup/backup.$Date.tar.gz data/raw.txt data/train.txt data/train.done.txt data/everyone/
    echo "备份旧的train.txt\raw.txt、trian.done.txt、everyone目录"
}

# 先备个份！太危险了！
backup

nohup \
gunicorn\
    web.labelme_server:app \
    --workers=10 \
    --worker-class=gevent \
    --bind=0.0.0.0:$1 \
    --timeout=300 \
    >> /dev/null 2>&1 &
