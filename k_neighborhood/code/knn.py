import pandas as pd
import numpy as np
import logging


def classify(inX, dataset, labels, k):
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
