'''
is_tree:判断是不是树
getMean：塌陷处理用到，返回左右树平均值
prune：后剪枝函数
'''
from numpy import *

from .cart_tree import splitdata


def is_tree(obj):
    return isinstance(obj, dict)


def getMean(tree):
    if is_tree(tree['right']):
        tree['right'] = getMean(tree['right'])
    if is_tree(tree['left']):
        tree['left'] = getMean(tree['left'])
    return (tree['left'] + tree['right']) / 2


def prune(tree, testdata):
    '''
    :param tree: 运行create_tree返回的结果
    :param testdata: 测试集合
    :return: 剪枝之后的数据
    '''
    if shape(testdata)[0] == 0:
        return getMean(tree)
    if is_tree(tree['right']) or is_tree(tree['left']):
        lset, rset = splitdata(testdata, tree['spind'], tree['spval'])
    if is_tree(tree['right']):
        tree['right'] = prune(tree['right'], rset)
    if is_tree(tree['left']):
        tree['left'] = prune(tree['left'], lset)
    if not is_tree(tree['right']) and not is_tree(tree['left']):
        lset, rset = splitdata(testdata, tree['spind'], tree['spval'])
        errornomerge = sum(power(lset[:, -1] - tree['left'], 2)) \
                       + sum(power(rset[:, -1] - tree['right'], 2))  # 未剪枝的error
        treemean = (tree['left'] + tree['right']) / 2
        errormerge = sum(power(testdata[:, -1] - treemean, 2))  # 剪枝之后的error
        if errormerge < errornomerge:
            print('merge')
            return treemean
        else:
            return tree
    else:
        return tree
