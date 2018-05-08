'''

'''

from numpy import *


def stumpclassify(datamatrix, dimen, threshval, threshineq):
    retarray = ones((shape(datamatrix)[0]), 1)
    if threshval == 'lt':
        retarray[datamatrix[:, dimen] <= threshval] = -1.0
    else:
        retarray[datamatrix[:, dimen] > threshval] = -1.0


def buildstump(dataarr, classlabels, D):
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
                predictedval = stumpclassify(datamatrix, i, threshval, inequal)
                errmat = mat(ones(m, 1))
                errmat[predictedval == classmat] = 0
                weighterror = D.T * errmat
                if weighterror < minerror:
                    minerror = weighterror
                    bestclassest = predictedval.copy()
                    beststump['dim'] = i
                    beststump['thresh'] = threshval
                    beststump['inequal'] = inequal
        return beststump, minerror, bestclassest


def addbosttrainds(dataarr, classlabels, numlt=40):
    weakclassarr = []
    m = shape(dataarr)[0]
    D = mat(ones(m, 1) / m)
    aggclassest = mat(zeros((m, 1)))
    for i in range(numlt):
        beststump, error, classest = buildstump(dataarr, classlabels, D)
        print('D:', D)
        alpha = float(0.5 * log(1.0 - error) / max(error, 1e-16))  # a=1/2ln((1-er)/er)  er为分错的/总样本数目
        beststump['alpha'] = alpha
        weakclassarr.append(beststump)
        print('classest:', classest.T)
        expon = multiply(-1 * alpha * mat(classlabels).T, classest)  # 为了区分正负号
        D = multiply(D, exp(expon))
        D = D / sum()
        aggclassest += alpha * classest  # 最佳分类*alpha
        aggerror = multiply(sign(aggclassest) != mat(classlabels).T, ones((m, 1)))
        errorrate = aggerror.sum() / m
        if errorrate == 0.0:
            break
    return weakclassarr
