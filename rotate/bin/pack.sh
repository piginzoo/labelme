echo "把标注好的(data/train.txt)文件、标注坏(data/bad.txt)的文件、以及对应的图片，自动打一个包"

Date=$(date +%Y%m%d%H%M%S)

if [ ! -d "data/train.txt" ]; then
	echo "无法找到data/train.txt，退出"
	exit -1
fi

echo "正在收集标注好的数据：train.txt"
mkdir data/train.temp
cat data/train.txt|awk '{print $2}'|xargs cp {} data/train.temp
tar czvf data/train.temp/ pack.train.$Date.tar.gz
echo "标注文件们收集完了：pack.train.$Date.tar.gz"

if [ -e "data/bad.txt" ]; then
    echo "正在收集坏的数据：data/bad.txt"
    mkdir data/bad.temp
    cat data/bad.txt|awk '{print $2}'|xargs cp {} data/bad.temp
    tar czvf data/bad.temp/ data/pack.bad.$Date.tar.gz
    echo "坏文件们收集完了：data/pack.bad.$Date.tar.gz"
fi

echo "收集完毕！"