echo "收集不是标准样本的坏样本（为了做2分类，比如区别非单据，即lablel.bad.txt)"

if [ -e "data/bad.txt" ]; then
    Date=$(date +%Y%m%d%H%M%S)
	echo "已收集的data/bad.txt存在，自动备份到：data/bad.$Date.txt"
    mv data/bad.txt data/backup/bad.$Date.txt
fi

find data/everyone -name "bad.bill.txt"|xargs cat > data/bad.txt

echo "收集完毕"