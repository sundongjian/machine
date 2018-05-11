from unsupervised.apriori.get_apriori import apriori,apriorigen



#
dataset=[[1,2,3],[23,35,56,],[34,56,78,],[23,45,78,],[12,45,89,],[12,56,17],[34,67,89,],[12,34,12],[16,47,89,],[45,78,89]]
a,b=apriori(dataset)
print(a,b)
# freq=frozenset([1,2,3,5,6,7])
# H1 = [frozenset([item]) for item in freq]
# print(H1)
# print(H1[0].issubset({1,2}))
#

