from logistics_value.stand_logis import standRegres
from parsedata.parsedata import autonorm
from parsedata.parsedata import ParseData



file_path=r'F:\machine\file\hyxd_movie_01newdata4.xlsx'
da = ParseData(file_path)
datamatin=da.dataset()
datamatin=autonorm(datamatin)
classlabels=da.labels()
print(standRegres(datamatin, classlabels))