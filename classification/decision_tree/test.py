from classification.decision_tree.tree import createtree
from parsedata.parsedata import ParseData

file_path = r'F:\machine\file\Book1.xlsx'
labels = ['a', 'b', 'c', 'd']
da = ParseData(file_path)
data = da.entry_data()
result = createtree(data, labels)  # dataset是整个数据，labels是特征，因为numpy不会显示特征名字，所以另外输入
print(result)
