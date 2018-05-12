from simplify_data.simple_svd.svd import recommend
from parsedata.parsedata import ParseData
import numpy




file_path=r'F:\machine\file\hyxd_movie_01newdata4.xlsx'
data = ParseData(file_path)
da=numpy.mat(data.dataset())
print(recommend(da,1,))

