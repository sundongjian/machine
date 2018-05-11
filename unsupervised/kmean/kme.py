''''
python中一个matrix矩阵名.A 代表将 矩阵转化为array数组类型
'''
import random
from numpy import *


def distance(veca, vecb):
    dis = sqrt(sum(power(veca - vecb, 2)))
    return dis


def randcent(database, k):
    '''
    :param database:
    :param k:
    :return:
    '''
    n = shape(database)[1]
    newmat = mat(zeros((k, n)))
    for j in range(0, n):  # 遇到了老问题 -->我真是太蠢了，下面的范围使用range这个关键词
        range_low = min(database[:, j])
        rangej = float(max(database[:, j]) - range_low)
        newmat[:, j] = range_low + rangej * random.rand(k, 1)  # 开始写成了，查了半小时错误，newaxis[:,j]...
    return newmat


def kmeans(database, k, distmean=distance, creatcen=randcent):
    m = shape(database)[1]
    cent = creatcen(database, k)
    record = mat(zeros((m, 2)))
    keep = True
    while keep:
        keep = False
        for i in range(m):
            mindist = inf
            minindex = -1
            for j in range(k):
                dist = distmean(cent[j, :], database[i, :])  # 这里加不加mat都行，加了之后是二维，不加一维
                if dist < mindist:
                    mindist = dist
                    minindex = j
            if record[i, 0] != minindex:
                keep = True
            record[i, :] = minindex, mindist
        for ce in range(k):
            newdata = database[nonzero(record[:, 0].A == ce)[0]]  # A 代表将 矩阵转化为array数组类型
            cent[ce, :] = mean(newdata, axis=0)
    return cent, record


