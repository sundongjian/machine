'''
classify:k-邻近算法分类器构造。
'''
import numpy as np



def classify(inX, dataset, labels, k):
    '''
    :param inX: 待测的参数，numpy。
    :param dataset: 不含labels的numpy格式。
    :param labels: 数据的答案列。
    :param k: 算出距离排序之后，选择最近的k个点。
    :return: 返回最近k个点中label占最多的作为结果返回
    '''
    datasize = dataset.shape[0]
    print(datasize)
    diffmat = np.tile(inX, (datasize, 1)) - dataset
    sqdiffmat = diffmat ** 2
    sqdistance = sqdiffmat.sum(axis=1)
    distance = sqdistance ** 0.5
    sorteddistance = distance.argsort()
    classcount = {}
    for i in range(0, k):
        label = labels[sorteddistance[i]]
        classcount[label] = classcount.get(label, 0) + 1
    f = zip(classcount.values(), classcount.keys())
    print(sorted(f, reverse=True)[0][1])
    return sorted(f, reverse=True)[0][1]
