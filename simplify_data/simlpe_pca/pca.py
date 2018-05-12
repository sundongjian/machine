'''
pca数据降维
'''
from numpy import *
def pca(datamat, topNfeat=2):
    '''
    :param datamat:
    :param topNfeat: 选出最大腾征向量个数
    :return:
    '''
    meanvals = mean(datamat, axis=0)
    meanremoved = datamat - meanvals  # 去除平均值
    covmat = cov(meanremoved, rowvar=0)  # 计算协方差矩阵
    eigvals, eigvects = linalg.eig(mat(covmat))  # 计算协方差矩阵的特征值和特征向量
    eigvalind = argsort(eigvals)  # 将特征值从大到小排序
    eigvalind = eigvalind[:-(topNfeat + 1):-1]  # 根据特征结果逆序得到topNfeat个最大特征向量
    redEigvects = eigvects[:, eigvalind]  # topNfeat个最大特征向量
    lowDDataMat = meanremoved * redEigvects   #将数据转换到新空间，同样还是不懂，明天把矩阵搞懂
    reconMat = (lowDDataMat * redEigvects.T) + meanvals
    return lowDDataMat, reconMat
