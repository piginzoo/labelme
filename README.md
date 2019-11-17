# 需求

想做一个相对比较简单的标注系统，满足自身需要。
主要是通过鼠标的点击，或者输入，快速的标注内容。
至于需要复杂的交互的标注，比如圈出有效区域的方式，暂不在考虑之列。

另外一个就是复审，比如我们已经得到了标注内容，我们需要复审，这样也可以通过这个系统来做。

总结一下，就是一个实用简单的标注系统。

## 整个过程

原始图片再data里面，

对于新打标注的，raw.txt，其实是当个数据库使用，整个文件，可以使用init.sh来自动生成，默认是图片是放在data/images中的。

这样的好处是不用搬运图片，只搬运标签文件中的文件行就成。
完成后，会运行bin/collect.sh来自动收集每个人的完成文件label.done.txt，
合并成标注完成文件train.txt。
复审的时候，需要首先为每个人分配复审任务，放置到check.txt中，
然后他完成一张复审，就会追加到good.txt（复审正确）或者bad.txt（复审错误）中，check.txt
最后，再运行bin/collect.done.sh，生成最后的标准文件train.done.txt

## 目录结构
为了兼容标注和复核，需要设计一个文件夹结构
```
everyone!
    |
    |--[piginzoo]
    |       |
    |       |--label.txt        # 打标文件，会一行行的减少
    |       |--label.done.txt   # 打标完成文件，会一行行增加
    |       |    
    |       |--check.txt        # 复检文件，会一条条的被搬运到good/bad里   
    |       |--good.txt         # 复检正确的文件，会一条条添加
    |       |--bad.txt          # 复检错误的文件，会一条条添加
    |
    |-raw.txt           # 最开始的原始文件，是用来给每个人分配label.txt的大库
    |-train.txt         # 从用户的label.txt合并后的文件（靠batch），并为每个人的提供check.txt的大库
    |-train.done.txt    # 从用户的label.done.txt合并后的文件（靠batch）        
```    

## 为一个人初始化任务
首先，登录后，检查这个登录用户piginzoo是否存在登录名文件夹，
如果不存在，按照用户名创建目录piginzoo，并搬运文件记录到新文件label.txt，
然后开始启动标注。

## 标注
标注的时候，读取这个人的标注任务文件label.txt的第一行，吐给前端，
标注完成后，从个人标注文件label.txt去除这一行，并添加到label.done.txt。

## 复查
复查的时候，会先给这个人分配check.txt，
然后每次标准，动态更新check.txt(减少第一行)，good.txt或者bad.txt（追加一行）


