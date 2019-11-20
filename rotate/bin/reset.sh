echo "将重新开始所有人的任务，已完成、未完成都会被重置，慎重！慎重！慎重！"

if [ -e "data/everyone" ]; then
    Date=$(date +%Y%m%d%H%M%S)
	echo "data/everyone自动备份到 => data/backup/everyone.$Date.txt"
    mv data/everyone data/backup/everyone.$Date
fi

echo "重置完成，请重启Web服务。"