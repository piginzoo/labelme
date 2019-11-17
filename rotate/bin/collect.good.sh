if [ ! -d "data/images" ]; then
	echo "图片必须要放到[data/images]目录下"
	exit -1
fi

if [ -e "data/raw.txt" ]; then
	echo "图片data/raw.txt已经存在，谨慎谨慎，如果确定是从新开始，请删除"
	exit -1
fi


ls -Al data/images/*|awk '{print $9}'>data/raw.txt

echo "已生成数据文件data/raw.txt，可以启动标注服务了！"