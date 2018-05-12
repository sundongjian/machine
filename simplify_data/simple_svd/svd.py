'''
eucidSim:相似度，欧式
pearsSim：皮尔逊相似度
cosSim：余弦相似度
standest：将待比较位置和所有同行不为0的列进行比较，最后得到期望值
svdEst：将数据转换到低纬度空间，其他和standest相同
recommend：调度
'''

from numpy import *
from numpy import linalg as la


def eucidSim(ina, inb):  # 欧氏相似度，1、（1+距离）
    return 1.0 / (1.0 + la.norm(ina - inb))


def pearsSim(ina, inb):  # 皮尔逊相似度
    if len(ina) < 3:
        return 1.0
    return 0.5 + 0.5 * corrcoef(ina, inb, rowvar=0)[0][1]


def cosSim(ina, inb):  # 余弦相似度
    num = float(ina.T * inb)
    denom = la.norm(ina) * la.norm(inb)
    return 0.5 + 0.5 * (num / denom)


def standest(dataset, user, simmeas, item):
    '''
    :param dataset:
    :param user: 行
    :param simmeas: 相似度函数，调用时给赋值
    :param item: 该user的待评分列
    :return:
    '''
    n = shape(dataset)[1]
    simtotal = 0
    ratsimtoal = 0
    for j in range(n):
        userrating = dataset[user, j]
        if userrating == 0:
            continue
        overlab = nonzero(logical_and(dataset[:, item].A > 0, dataset[:, j].A > 0))[0]
        if len(overlab) == 0:
            similarity = 0
        else:
            similarity = simmeas(dataset[overlab, item], dataset[overlab, j])
        simtotal += similarity
        ratsimtoal += similarity * userrating
    if simtotal == 0:
        return 0
    else:
        return ratsimtoal / simtotal


def svdEst(dataMat, user, simMeas, item):
    '''
    同standest
    :param dataMat:
    :param user:
    :param simMeas:
    :param item:
    :return:
    '''
    n = shape(dataMat)[1]
    simTotal = 0.0;
    ratSimTotal = 0.0
    U, Sigma, VT = la.svd(dataMat)
    Sig4 = mat(eye(4) * Sigma[:4])
    xformeditems = dataMat.T * U[:, :4] * Sig4.I  # 这里还是不明白
    for j in range(n):
        userRating = dataMat[user, j]
        if userRating == 0 or j == item: continue
        similarity = simMeas(xformeditems[item, :].T, \
                             xformeditems[j, :].T)
        print('the %d and %d similarity is :%f' % (item, j, similarity))
        simTotal += similarity
        ratSimTotal += similarity * userRating
    if simTotal == 0:
        return 0
    else:
        return ratSimTotal / simTotal


def recommend(datasetmat, user, N=3, simmeas=cosSim, estmethon=standest):
    '''
    :param datasetmat: 默认行为user，列为菜品
    :param user:
    :param N: 选取前N个相似度最高的打分，其他搁置
    :param simmeas: 相似度函数名
    :param estmethon: 评分函数
    :return:
    '''
    unrateditems = nonzero(datasetmat[user, :].A == 0)[1]  # 未评级的列
    if not unrateditems:
        return ' %s have rated everything' % user
    itemscore = []
    for item in unrateditems:
        estimatedscore = estmethon(datasetmat, user, simmeas, item)
        itemscore.append((item, estimatedscore))
    return sorted(itemscore, key=lambda j: j[1], reverse=True)[:N]
