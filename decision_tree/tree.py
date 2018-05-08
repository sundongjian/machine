'''
calcshannonent：香浓值计算。
spiltdataset：数据分割，将输入数据的某一特征列的某一特征值聚拢之后删除此特征列，返回。
chosebestfeature：选择最佳分割列。
majorlabel：选出输入的labels里占最多数的作为答案返回。
createtree：创建树。
'''

import numpy


# 这里的dataset包括答案列,这里可以使用entry_data()
def calcshannonent(dataset):
    '''
    :param dataset: dataset包括答案列的data，numpy格式
    :return: 香浓值，float
    '''
    index_num = len(dataset)
    labels = set([exm[-1] for exm in dataset])
    labels_counts = {}
    for label in labels:
        labels_counts[label] = labels_counts.get(label, 0) + 1
    shannonent = 0.0
    for num in labels_counts.values():
        prob = float(num) / index_num
        shannonent -= prob * numpy.math.log(prob, 2)  # 两次log是不同的，搞铲铲
    return shannonent


def spiltdataset(dataset, axis, value):
    '''
    :param dataset: 包括labels列的data，numpy格式
    :param axis: 该特征列。
    :param value: 该列的某一个value。
    :return: numpy格式，聚拢该列有这个value的数据后删除该列
    '''
    retdataset = []
    for exm in dataset:
        if exm[axis] == value:
            reduceexm = numpy.delete(exm, [value], axis=0)  # 用这个，直接删除value
            # reduceexm = exm[:axis].np.extend(exm[axis:])#这个有报错
            retdataset.append(reduceexm)
    return retdataset


def chosebestfeature(dataset):
    '''
    :param dataset: 包括labels列的数据
    :return: 最佳分割列，int格式
    '''
    feature_num = len(dataset[0]) - 1
    index_num = float(len(dataset))
    entryshannonent = calcshannonent(dataset)
    bestinfogain = 0.0
    bestfeature = -1
    for i in range(0, feature_num):
        univalue = set([exm[i] for exm in dataset])
        newentropy = 0.0
        for value in univalue:
            subdataset = spiltdataset(dataset, i, value)
            prob = len(subdataset) / index_num
            newentropy += prob * calcshannonent(subdataset)
        infogain = entryshannonent - newentropy
        if infogain > bestinfogain:
            bestinfogain = infogain
            bestfeature = i
        return bestfeature


def majorlabel(classlist):
    '''
    :param classlist: labels列，list格式
    :return: 占最大多数的答案
    '''
    label_count = {}
    for label in classlist:
        label_count[label] += label_count.get(label, 0) + 1
    f = zip(label_count.values(), label_count.keys())
    result = sorted(f, reverse=True)
    return result[0][0]


# 准备工作已经结束了，可以创建树了，可以预想到创建树用到递归，所以先制定停止条件
def createtree(dataset, labels):  # 这个labeis是特征名
    '''
    :param dataset: numpy格式，含labels列
    :param labels: 每列对应的特征名，numpy
    :return: 决策树
    '''
    classlist = [exm[-1] for exm in dataset]
    if classlist.count(classlist[0]) == len(classlist):  # label完全相同停止分类
        return classlist[0]
    if len(dataset[0]) == 1:  # 所有特征已经用完，返回label最多的
        return majorlabel(classlist)
    bestfeat = chosebestfeature(dataset)
    bestfeatlabel=labels[bestfeat]
    mytree = {bestfeatlabel: {}}
    del (labels[bestfeat])
    featvalues = [exm[bestfeat] for exm in dataset]
    uniquevals = set(featvalues)
    for value in uniquevals:
        sublabels = labels[:]
        mytree[bestfeat][value] = createtree(spiltdataset(dataset, bestfeat, value), sublabels)
    return mytree
