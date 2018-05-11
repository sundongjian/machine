from unsupervised.kmean.kme import kmeans
from unsupervised.kmean.dichotomy_tree import dichmeans
from parsedata.parsedata import ParseData
import numpy


file_path=r'F:\machine\file\hyxd_movie_01newdata4.xlsx'
test_path=r'F:\machine\file\hyxd_movie_01newdata3.xlsx'
da = ParseData(test_path)
data=da.entry_data()[:107,:]
print(kmeans(data,2))
print(dichmeans(numpy.array(data),5))#这样就对了，好奇怪，明天专门研究一下这些格式问题和相互赋值问题

# data=[[1,2,3],[23,35,56,],[34,1],[23,45,78,],[12,289,],[12,56,17],[34,67,89,],[3,34,12],[16,47,89,],[45,78,89]]
# print(dichmeans(numpy.mat(data),5))#这样是对的，奇怪

