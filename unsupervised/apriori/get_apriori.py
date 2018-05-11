'''

'''
def createC1(dataset):
    C1=[]
    for item in dataset:
        for it in item:
            if it not in C1:
                C1.append(it)
    C1.sort()
    return map(frozenset,C1)

def scan(D,ck,minsupport):
    sscent={}
    for tid in D:
        for can in ck:
            if can.issubset(tid):
                