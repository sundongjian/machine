import numpy
import pandas

from tree_logistic.cart_tree import creattree
from parsedata.parsedata import ParseData


file_path=r'F:\machine\file\hyxd_movie_01newdata4.xlsx'
da = ParseData(file_path)
data=da.entry_data()
print(creattree(data))


