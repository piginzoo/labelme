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


nohup \
gunicorn\
    web.labelme_server:app \
    --workers=10 \
    --worker-class=gevent \
    --bind=0.0.0.0:$1 \
    --timeout=300
    >> /dev/null 2>&1 &