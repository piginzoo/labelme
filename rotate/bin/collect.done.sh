echo "收集第一次标注的文件（即lablel.done.txt)"


if [ -e "data/train.txt" ]; then
    Date=$(date +%Y%m%d%H%M%S)
	echo "已收集的data/train.txt存在，自动备份到：data/train.$Date.txt"
    mv data/train.txt data/backup/train.$Date.txt
fi

find data/everyone -name "label.done.txt"|xargs cat > data/train.txt

echo "收集完毕"