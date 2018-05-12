'''

'''

from numpy import *
from numpy import linalg as la

def eucidSim(ina,inb):  #欧氏相似度，1、（1+距离）
    return 1.0/(1.0+la.norm(ina-inb))


def pearsSim(ina,inb):  #皮尔逊相似度
    if len(ina)<3:
        return 1.0
    return 0.5+0.5*corrcoef(ina,inb,rowvar=0)[0][1]


def cosSim(ina,inb):  #余弦相似度
    num=float(ina.T*inb)
    denom=la.norm(ina)*la.norm(inb)
    return 0.5+0.5*(num/denom)


def standest(dataset,user,simmeas,item):
    n=shape(dataset)[1]
    simtotal=0
    ratsimtoal=0
    for j in range(n):
        userrating=dataset[user,j]
        if userrating==0:
            continue
        overlab=nonzero(logical_and(dataset[:,item].A>0,dataset[:,j].A>0))[0]
        if len(overlab)==0:
            similarity=0
        else:
            similarity=simmeas(dataset[overlab,item],dataset[overlab,j])
        simtotal+=similarity
        ratsimtoal+=similarity*userrating
    if simtotal==0:
        return 0
    else:
        return ratsimtoal/simtotal


def recommend(datasetmat,user,N=3,simmeas=cosSim,estmethon=standest):
    unrateditems=nonzero(datasetmat[user,:].A==0)[1]  #未评级的列
    if not unrateditems:
        return ' %s have rated everything'%user
    itemscore=[]
    for item in unrateditems:
        estimatedscore=estmethon(datasetmat,user,simmeas,item)
        itemscore.append((item,estimatedscore))
    return sorted(itemscore,key=lambda j:j[1],reverse=True)[:N]



