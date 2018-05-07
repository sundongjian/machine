'''
按照抽象数据类型分析，首先分析需要的几个操作
1。计算香浓值
2。挑选最优列
3.
'''
from math import log
#这里的dataset包括答案列
def calcshannonent(dataset):
    index_num=len(dataset)
    labels=dataset.iloc[:,-1].values
    labels_counts={}
    for label in labels:
        labels_counts[label]=labels_counts.get(label,0)+1
    shannonent=0.0
    for num in labels_counts.values():
        prob=float(num)/index_num
        shannonent-=prob*log(prob,2)
    return shannonent

def spiltdataset(dataset,axis,value):
    retdataset=[]
    for exm in dataset:
        if exm[axis]==value:
            reduceexm=exm[:axis].extend(exm[axis+1:])
            retdataset.append(reduceexm)
    return retdataset


def chosebestfeature(dataset):
    feature_num=dataset[0]-1
    index_num=float(len(dataset))
    entryshannonent=calcshannonent(dataset)
    bestinfogain=0.0
    bestfeature=-1
    for i in range(0,feature_num):
        newentropy =0.0
        univalue=set([exm[i] for exm in dataset])
        for value in univalue:
            subdataset=spiltdataset(dataset,i,value)
            prob=len(subdataset)/index_num
            newentropy+=prob*calcshannonent(subdataset)
        infogain=entryshannonent-newentropy
        if infogain > bestinfogain:
            bestinfogain=infogain
            bestfeature=i
        return bestfeature

def majorlabel(classlist):
    label_count={}
    for label in classlist:
        label_count[label]+=label_count.get(label,0)+1
    f=zip(label_count.values(),label_count.keys())
    result=sorted(f,reverse=True)

#准备工作已经结束了，可以创建树了，可以预想到创建树用到递归，所以先制定停止条件
def createtree(dataset,labels):#这个labeis是特征名
    classlist=[exm[-1] for exm in dataset]
    if classlist.count(classlist[0])==len(classlist):#label完全相同停止分类
        return classlist[0]
    if len(dataset[0])==1:#所有特征已经用完，返回label最多的
        return majorlabel(classlist)
    bestfeat=chosebestfeature(dataset)
    mytree={bestfeat:{}}
    del(labels[bestfeat])
    featvalues=[exm[bestfeat] for exm in dataset]
    uniquevals=set(featvalues)
    for value in uniquevals:
        sublabels=labels[:]
        mytree[bestfeat][value]=createtree(spiltdataset(dataset,bestfeat,value),sublabels)
    return mytree


