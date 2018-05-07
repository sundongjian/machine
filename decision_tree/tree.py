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

def chosebestfeature(dataset):
    feature_num=dataset[0]-1
    entryshannonent=calcshannonent(dataset)
    for i in range(0,feature_num):
        univalue=set([exm[i] for exm in dataset])
        for value in univalue:

