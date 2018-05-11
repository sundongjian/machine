from unsupervised.apriori.get_apriori import apriori,generateRules



#
dataset=[[1, 3, 4], [2, 3, 5], [1, 2, 3, 5], [2, 5]]
a,b=apriori(dataset)
print(a,b)
generateRules(a, b, minConf=0.1)
# freq=frozenset([1,2,3,5,6,7])
# H1 = [frozenset([item]) for item in freq]
# print(H1)
# print(H1[0].issubset({1,2}))
#

