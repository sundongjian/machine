'''
stumpclassify：将超过阈值的设为-1，其他为1
buildstump：计算最佳分类列，该列最佳阈值和阈值符号，加权错误率
addbosttrainds：根据返回的加权错误率计算alpha，然后计算D，继续进行迭代，直到达到指定次数或者错误率为0
'''

from numpy import *


def stumpclassify(datamatrix, dimen, threshval, inequal):
    '''
    :param datamatrix: 数据，matrix型
    :param dimen: 列
    :param threshval: 阈值
    :param inequal: 阈值符号
    :return: 返回预测结果，将超过阈值的设为-1，其他为0
    '''
    retarray = ones((shape(datamatrix)[0]), 1)
    if inequal == 'lt':
        retarray[datamatrix[:, dimen] <= threshval] = -1.0
    else:
        retarray[datamatrix[:, dimen] > threshval] = -1.0


def buildstump(dataarr, classlabels, D):
    '''

    :param dataarr: 数据集
    :param classlabels: 答案集
    :param D: 权重
    :return: beststump包含列，阈值和阈值符号的字典 minerror最小加权错误率  bestclassest最佳预测结果
    '''
    datamatrix = mat(dataarr)
    classmat = mat(classlabels)
    m, n = shape(datamatrix)
    numsteps = 10.0
    minerror = inf
    for i in range(0, n):
        range_low = datamatrix[:, i].min()
        range_high = datamatrix[:, i].max()
        range = range_high - range_low
        stepsize = range / numsteps
        beststump = {}
        for j in range(-1, numsteps):  # 为什么要从-1开始？
            for inequal in ['lt', 'gt']:
                threshval = range_low + stepsize * j
                predictedval = stumpclassify(datamatrix, i, threshval, inequal)  # 这里要注意，什么是阈值，当inequal=lt的
                # 的时候，小于阈值的就是不满足条件的，设为-1
                errmat = mat(ones(m, 1))
                errmat[predictedval == classmat] = 0
                weighterror = D.T * errmat  # 计算加权错误率
                if weighterror < minerror:
                    minerror = weighterror
                    bestclassest = predictedval.copy()
                    beststump['dim'] = i
                    beststump['thresh'] = threshval
                    beststump['inequal'] = inequal
        return beststump, minerror, bestclassest


def addbosttrainds(dataarr, classlabels, numlt=40):
    '''
    :param dataarr: 数据集
    :param classlabels: 答案集
    :param numlt: 迭代次数
    :return: 列表，该列表子元素为字典，每个字典都是一个弱分类器。字典记录了每次迭代最佳列，最佳阈值和阈值符号，alpha值
    '''
    weakclassarr = []
    m = shape(dataarr)[0]
    D = mat(ones(m, 1) / m)
    aggclassest = mat(zeros((m, 1)))
    for i in range(numlt):
        beststump, error, classest = buildstump(dataarr, classlabels, D)
        print('D:', D)
        alpha = float(0.5 * log(1.0 - error) / max(error, 1e-16))  # a=1/2ln((1-er)/er)  er为加权错误率
        beststump['alpha'] = alpha
        weakclassarr.append(beststump)
        print('classest:', classest.T)
        expon = multiply(-1 * alpha * mat(classlabels).T, classest)  # 区分正负号，正确分类为-a，错误分类为a，这种方式值得学习
        D = multiply(D, exp(expon))
        D = D / sum()  # 下一轮迭代的D值
        aggclassest += alpha * classest  # 每次对a*最佳分类进行叠加
        aggerror = multiply(sign(aggclassest) != mat(classlabels).T, ones((m, 1)))  # 计算叠加之后的最佳分类的错误，值得学习
        errorrate = aggerror.sum() / m
        if errorrate == 0.0:
            break
    return weakclassarr


def adaclassify(dattoclass, classifierarr):
    '''
    :param dattoclass: 待测数据集
    :param classifierarr: 分类器集合
    :return: 分类结果
    '''
    datamatrix = mat(dattoclass)
    m = shape(datamatrix)
    aggclassest = mat(zeros((m, 1)))
    for i in range(len(classifierarr)):
        classest = stumpclassify(datamatrix, classifierarr[i]['dim'],
                                 classifierarr[i]['thresh'], classifierarr[i]['inequal'])
        aggclassest = classifierarr[i]['alpha'] * classest
        print(aggclassest)
    return sign(aggclassest)
