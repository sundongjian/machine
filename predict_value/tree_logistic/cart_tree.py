'''
与前面的决策树作对比，香浓值计算误差改成总方差，分割函数要有，创建树要有，选择最佳列要有
legleaf：计算最后的叶节点，也就是最后一列平均值
regErr：返回labels列的总方差
splitdata：分左右枝
creattree：创建树
choosebestsplit：选择最佳列，最佳value
'''
from numpy import *


def legleaf(dataset):
    return mean(dataset[:, -1])


def regErr(dataset):
    return var(dataset[:, -1]) * shape(dataset)[0]


def splitdata(dataset, feat, val):
    '''
    nonzero(dataset[:, feat] > val)[0]返回的是feat列大于val的所有行
    :param dataset: 数据，含答案行
    :param feat: 最佳列，int
    :param val: 最佳值
    :return: 左右叶
    '''
    mt0 = dataset[nonzero(dataset[:, feat] > val)[0], :]  # 参考书是错的
    mt1 = dataset[nonzero(dataset[:, feat] <= val)[0], :]
    return mt0, mt1


def creattree(dataset, leafType=legleaf, errType=regErr, ops=(1, 4)):
    '''
    :param dataset: 含答案
    :param leafType: 将函数作为参数，这增加了函数的可扩展性，调用时该函数名就可以换函数
    :param errType: 同上
    :param ops: 1是继续分割的方差下限，4是分割后两部分的个数下线
    :return: 字典格式的分割结果
    '''
    feat, val = choosebestsplit(dataset, leafType, errType, ops)
    if feat is None:
        return val
    retTree = {}
    retTree['spind'] = feat
    retTree['spval'] = val
    left_set, right_set = splitdata(dataset, feat, val)
    retTree['left'] = creattree(left_set, leafType, errType, ops)
    retTree['right'] = creattree(right_set, leafType, errType, ops)
    return retTree


def choosebestsplit(dataset, leafType, errType, ops=(1, 4)):
    '''
    :param dataset: 含答案列
    :param leafType:
    :param errType:
    :param ops:
    :return: 最佳分割列和最佳分割值
    '''
    tols = ops[0]
    toln = ops[1]
    if len(set(dataset[:, -1].T.tolist())) == 1:  # 前面不用转置也没问题的
        return None, leafType(dataset)
    m, n = shape(dataset)
    s = errType(dataset)
    bests = inf
    bestindex = 0
    bestvalue = 0
    for feat in range(0, n - 1):  # 这个刚才写错了，n是总列数，去掉答案类是n-1列，下标是n-2列
        for splitval in set(dataset[:, feat]):
            mt0, mt1 = splitdata(dataset, feat, splitval)
            if shape(mt0)[0] < toln or shape(mt1)[0] < toln:
                continue
            news = errType(mt0) + errType(mt1)
            if news < bests:
                bests = news
                bestvalue = splitval
                bestindex = feat
    if (s - bests) < tols:
        return None, leafType(dataset)
    mat0, mat1 = splitdata(dataset, bestindex, bestvalue)
    if (shape(mat0)[0]) < toln or (shape(mat1)[1] < toln):
        return None, leafType(dataset)
    return bestindex, bestvalue
