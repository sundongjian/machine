import numpy
import pandas

from adaboost.adboost_tree import adaclassify
from adaboost.adboost_tree import addbosttrainds
from parsedata.parsedata import ParseData

inx=numpy.array([])
file_path=r'F:\machine\file\hyxd_movie_01newdata4.xlsx'
da = ParseData(file_path)
data = da.dataset()
# classlabels=da.labels()
classlabels=numpy.mat(pandas.read_excel(file_path).iloc[:,[-1]]) #过一会改parsedata，两个返回的维度不一样
classifierarr=addbosttrainds(data,classlabels)
print(classifierarr)
print(adaclassify(inx,classifierarr))


