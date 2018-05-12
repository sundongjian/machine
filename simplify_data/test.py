
from parsedata.parsedata import ParseData
from simplify_data.simlpe_pca.pca import pca
from numpy import *


def pa(datamat,topNfeat=2):
    meanvals=mean(datamat,axis=0)
    meanremoved=datamat-meanvals  #去除平均值
    covmat=cov(meanremoved,rowvar=0)  #计算协方差矩阵

    print(covmat)
    eigvals,eigvects=linalg.eig(mat(covmat))  #计算协方差矩阵的特征值和特征向量
    print(eigvals)
    print(eigvects)


    eigvalind=argsort(eigvals)  #将特征值从大到小排序
    eigvalind=eigvalind[:-(topNfeat+1):-1]  #根据特征结果逆序得到topNfeat个最大特征向量
    redEigvects=eigvects[:,eigvalind]  #topNfeat个最大特征向量
    lowDDataMat=meanremoved*redEigvects
    reconMat=(lowDDataMat*redEigvects.T)+meanvals
    return lowDDataMat ,reconMat


file_path=r'F:\machine\file\hyxd_movie_01newdata4.xlsx'
data = ParseData(file_path)
da=data.dataset()
m,n=pa(da,3)


