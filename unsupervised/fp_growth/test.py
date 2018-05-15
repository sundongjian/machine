from unsupervised.fp_growth.fp import createinitset,createtree


data=[['r', 'z', 'h', 'j', 'p'],
               ['z', 'y', 'x', 'w', 'v', 'u', 't', 's'],
               ['z'],
               ['r', 'x', 'n', 'o', 's'],
               ['y', 'r', 'x', 'z', 'q', 't', 'p'],
               ['y', 'z', 'x', 'e', 'q', 's', 't', 'm']]
result=createinitset(data)
mytree,myheadertable=createtree(result,0.2)
print(myheadertable)
print(mytree.disp())

