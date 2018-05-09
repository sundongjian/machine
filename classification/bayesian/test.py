import numpy as np

from classification.bayesian.bay import test

file_path = r'F:\machine\file\Book1.xlsx'
inx = np.array([0, 1, 1, 0])
result = test(inx, file_path)
print(result)
