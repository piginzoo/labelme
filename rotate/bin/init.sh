if [ ! -d "data/images" ]; then
	echo "图片必须要放到[data/images]目录下"
	exit -1
fi

mkdir data/everyone
mkdir data/backup

if [ -e "data/raw.txt" ]; then
    Date=$(date +%Y%m%d%H%M%S)
	echo "图片data/raw.txt已经存在，自动备份到 => data/raw.$Date.txt"
    mv data/raw.txt data/backup/raw.$Date.txt
fi


ls -Al data/images/*|awk '{print $9}'>data/raw.txt

echo "已生成数据文件data/raw.txt，可以启动标注服务了！"