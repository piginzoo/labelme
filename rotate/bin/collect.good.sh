echo "收集对标注过的，再做过一次的校验的标注文件："

if [ -e "data/train.done.txt" ]; then
    Date=$(date +%Y%m%d%H%M%S)
	echo "已收集的data/train.done.txt存在，自动备份到：data/train.done.$Date.txt"
    mv data/train.done.txt data/backup/train.done.$Date.txt
fi

find data/everyone -name "good.txt"|xargs cat > data/train.done.txt

echo "收集完毕"