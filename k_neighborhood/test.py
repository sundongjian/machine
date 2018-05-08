import numpy as np

from k_neighborhood.code.knn import classify
from parsedata.parsedata import ParseData


file_path=r'F:\machine\file\Book1.xlsx'
file_path1=r'F:\machine\file\yob1893.txt'

da=ParseData(file_path)
dataset=da.dataset()
labels=da.labels()
inx=np.array([1,2,3,5])
classify(inx,dataset,labels,3)


