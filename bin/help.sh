#!/usr/bin/env bash
echo "========================================================================================"
echo "init.sh           从某个目录，收集样本，产生data/raw.txt"
echo "server.sh         启动web服务器，参数端口，运行之前修改conf.py的mode模式，确定是2次打标还是做4分类"
echo "collect.done.sh   收集4分类中的结果，合并到一起到data/train.txt"
echo "collect.good.sh   收集2次校验打标的结果，合并到一起到data/train.done.txt"
echo "collect.bad.sh    收集2次校验/4分类中有问题的样本，合并到一起到data/bad.txt"
echo "debug.sh          调试模式启动，可以重新加载python、网页修改，适合调试模式"
echo "pack.sh           把打标后的结果，连通图片们，一起打包"
echo "========================================================================================"