'''
论numpy中matrix 和 array的区别 https://blog.csdn.net/vincentlipan/article/details/20717163
'''

import numpy
from numpy import *


def sigmoid(inx):
    return 1.0 / (1 + exp(-inx))


def gradAscent(datamatin, classlabels):
    datamatrix = mat(datamatin)
    labelmat = mat(classlabels)
    m, n = shape(datamatrix)
    alpha = 0.001
    maxcycles = 500
    weights = ones((n, 1))
    for k in range(0, maxcycles):
        h = sigmoid(datamatrix * weights)
        error = labelmat - h
        weights = weights + alpha * datamatrix.transpose() * error
    return weights
