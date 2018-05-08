import numpy

from adaboost.adboost_tree import adaclassify
from adaboost.adboost_tree import addbosttrainds
from parsedata.parsedata import ParseData

inx=numpy.array([])
file_path=''
da = ParseData(file_path)
data = da.dataset()
classlabels=da.labels()
classifierarr=addbosttrainds(data,classlabels)
adaclassify(inx,classifierarr)


