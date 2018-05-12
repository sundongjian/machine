'''
二分法:这个理解起来很容易，但是具体操作雨点难度。将每个质心遍历，将每个执行二分算出分和未分误差值，选出误差值最小质心，将这个
这时候由一个质心变成了两个，将二分里质心为1的改质心为最后的下标加入，另外质心为0的更新为之前的质心，然后将新质心更新。。。
我讲不下去了，看代码吧
最后的一个赋值竟然出问题了，逻辑上没问题啊。数据也没问题，我从网上拷贝了一份也是错的。两天之后。我自己加array是对的

'''
from numpy import *

from unsupervised.kmean.kme import kmeans, distance


def dichmeans(dataset, k, distmeans=distance):
    '''
    :param dataset:
    :param k:
    :param distmeans:
    :return:
    '''
    m = shape(dataset)[0]
    clusterassment = mat(zeros((m, 2)))
    centroio = mean(dataset, axis=0).tolist()[0]
    centlist = [centroio]
    for j in range(0, m):
        clusterassment[j, 1] = distmeans(mat(centroio), dataset[j]) ** 2
    while len(centlist) < k:
        lowestsse = inf
        for i in range(len(centlist)):
            pstin = dataset[nonzero(clusterassment[:, 0].A == i)[0], :]
            centroidmat, splitclustass = kmeans(pstin, 2, distmeans)
            ssesplit = sum(splitclustass[:, 1])
            ssenotsplit = sum(clusterassment[nonzero(clusterassment[:, 0].A != i)[0], 1])
            if ssenotsplit + ssesplit < lowestsse:
                bestcenttosplit = i
                bestnewcentes = centroidmat
                bestclusass = splitclustass.copy()
                lowestsse = ssesplit + ssenotsplit
        print(bestclusass)
        break
        bestclusass[nonzero(bestclusass[:, 0].A == 1)[0], 0] = len(centlist)
        bestclusass[nonzero(bestclusass[:, 0].A == 0)[0], 0] = bestcenttosplit
        centlist[bestcenttosplit] = bestnewcentes[0, :]
        centlist.append(bestnewcentes[1, :])
        clusterassment[nonzero(clusterassment[:, 0].A == bestcenttosplit)[0], :] = bestclusass
    return mat(centlist), clusterassment
