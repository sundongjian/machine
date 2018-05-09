'''
standRegres:解出向量ws
遗留问题：数学问题，全搞懂再自己写
'''
from numpy import *


def standRegres(xArr, yArr):
    '''
    :param xArr:[[],[]]
    :param yArr:[,,,]
    :return: 向量
    '''
    xMat = mat(xArr)
    yMat = mat(yArr).T
    xTx = xMat.T * xMat
    if linalg.det(xTx) == 0.0:
        print('This matrix is  singular ,cannot do inverse')
        return
    ws = xTx.T * (xMat.T * yMat)
    return ws


def lwlr():
    pass
