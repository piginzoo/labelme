if [ "$1" == "" ]; then
	echo "命令格式：init.sh <图片目录>"
	exit -1
fi

if [ ! -d $1 ]; then
	echo "图片目录不存在"
	exit -1
fi

mkdir data/everyone
mkdir data/backup

if [ -e "data/raw.txt" ]; then
    Date=$(date +%Y%m%d%H%M%S)
	echo "图片data/raw.txt已经存在，自动备份到 => data/raw.$Date.txt"
    mv data/raw.txt data/backup/raw.$Date.txt
fi


ls -Al $1/*|awk '{print $9}'>data/raw.txt

echo "已生成数据文件data/raw.txt，可以启动标注服务了！"