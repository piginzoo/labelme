Date=$(date +%Y%m%d%H%M)

if [ ! -e data/raw.txt ]; then
    echo "请先运行 bin/init.sh 初始化data/raw.txt文件"
    exit
fi

if [ "$1" = "stop" ]; then
    echo "停止Web服务器"
    ps aux|grep python|grep server|awk '{print $2}'|xargs kill -9
    exit
fi

#nohup \
gunicorn\
    web.server:app \
    --workers=1 \
    --worker-class=gevent \
    --bind=0.0.0.0:8082 \
    --timeout=300
    #>> ./logs/sample_classify_$Date.log 2>&1 &