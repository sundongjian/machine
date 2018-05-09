import numpy
import pandas

from tree_logistic.cart_tree import creattree
from tree_logistic.prune import prune
from parsedata.parsedata import ParseData


file_path=r'F:\machine\file\hyxd_movie_01newdata4.xlsx'
test_path=r'F:\machine\file\hyxd_movie_01newdata5.xlsx'
da = ParseData(file_path)
data=da.entry_data()
test=ParseData(test_path)
testdata=test.entry_data()
tree=creattree(data)
print(tree)
print(prune(tree,testdata))

