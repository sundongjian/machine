'''
朴素贝叶斯
theory_trainnb0:求出理论上p(x|y)和p(y)的概率。选择非词袋模式
actual_trainnb0：为防止溢出和防止0出现做出的处理
classifyNB：最后的计算和比较
test：将test放在模块里供外面的接口调用
'''
import numpy as np
# from  math import log   不能直接应用 math 库里的东西到 ndarray 上,得用numpy中的函数。如np.exp
from numpy import log

from parsedata.parsedata import ParseData


def theory_trainnb0(dataset, labels):
    '''
    :param dataset: 由每一个单词构成的单词矩阵，该文档出现该单词为1，没有为0.numpy格式，不含labels
    :param labels: 答案列，labels可以为numpy和list，消极为0，积极为1
    :return: p0vect, p1vect, negative_prop, positive_prob 分别为消极概率向量，积极概率向量，消极先验概率，积极先验概率
    '''
    index_num = len(dataset)
    feature_num = len(dataset[0])
    negative_prop = (index_num - sum(labels)) / index_num
    positive_prob = 1 - negative_prop
    p0_num = np.zeros(feature_num)
    p1_num = np.zeros(feature_num)
    p0 = 0
    p1 = 1
    for i in range(0, index_num):
        if labels[i] == 0:
            p0_num += dataset[i]  # 对应特征词+
            p0 += sum(dataset[i])
        elif labels == 1:
            p1_num += dataset[i]
            p1 += sum(dataset[i])
    p0vect = p0_num / p0
    p1vect = p1_num / p1
    return p0vect, p1vect, negative_prop, positive_prob


# 实际算法,防止出现*0，小数太小，取log
def actual_trainnb0(dataset, labels):
    '''
    基本同上
    :param dataset:
    :param labels:
    :return:
    '''
    index_num = len(dataset)
    feature_num = len(dataset[0])
    negative_prop = (index_num - sum(labels)) / index_num
    positive_prob = 1 - negative_prop
    p0_num = np.ones(feature_num)
    p1_num = np.ones(feature_num)
    p0 = 0
    p1 = 1
    for i in range(0, index_num):
        if labels[i] == 0:
            p0_num += dataset[i]  # 对应特征词+
            p0 += sum(dataset[i])
        else:
            p1_num += dataset[i]
            p1 += sum(dataset[i])
    p0vect = log(p0_num / p0)
    p1vect = log(p1_num / p1)
    return p0vect, p1vect, negative_prop, positive_prob


def classifyNB(inx, p0vect, p1vect, negative_prop, positive_prob):
    '''
    :param inx: 待测向量
    :param p0vect: 消极概率向量
    :param p1vect: 积极概率向量
    :param negative_prop: 消极先验概率
    :param positive_prob: 积极先验概率
    :return:
    '''
    p1 = sum(inx * p0vect) + log(positive_prob)
    p0 = sum(inx * p1vect) + log(negative_prop)
    if p1 > p0:
        return 1
    else:
        return 0


def test(inx, path):
    '''
    :param inx: 待测向量
    :param path: 数据路径
    :return: 结果
    '''
    da = ParseData(path)
    dataset = da.dataset()
    labels = da.labels()
    p0vect, p1vect, negative_prop, positive_prob = actual_trainnb0(dataset, labels)
    result = classifyNB(inx, p0vect, p1vect, negative_prop, positive_prob)
    return result

