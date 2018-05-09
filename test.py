
import numpy
from parsedata.parsedata import ParseData
# aggclassest = numpy.mat(numpy.zeros((10, 1)))
# print( numpy.mat(aggclassest)*numpy.mat(aggclassest).T)
a=[[1,2],[1,2],[1,2],[1,2],[1,2]]
print(numpy.mat(a))
file_path=r'F:\machine\file\hyxd_movie_01newdata4.xlsx'
da = ParseData(file_path)
data = da.dataset()
print(numpy.mat(data))