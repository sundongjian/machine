'''
这个过程是C1-->L1-->C2-->L2--->C3-->L3的过程，即先找到最少元素的频繁集，再根据频繁集来制作超集，再检查得到新的频繁集
比价难的是apriorigen。这是制作超集的函数。比如输入【{1,2,3}{1,2,4}{1,2,5}】这时k=4，固定住相邻的集合里的前两个元素，如固定
{1,2}{1,2}如果固定住的这两个元素相等，就将两个元素求并集返回
这里版本冲突比较严重，留着明天看看吧

'''
def createC1(dataset):
    C1=[]
    for item in dataset:
        for it in item:
            if it not in C1:
                C1.append(it)
    C1.sort()
    #return map(frozenset,C1)  #这个是2.几的版本，坑爹呢这是
    #return list(map(frozenset,C1))  #这个也是错的
    return frozenset(C1)


def scan(D,ck,minsupport):
    sscent={}
    for tid in D:
        for can in ck:
            if frozenset([can]).issubset(tid):
                if can not in sscent.keys():
                    sscent[can]=1
                else:
                    sscent[can]+=1
    numitems=float(len(D))
    retlist=[]
    supportdata={}
    for key in sscent:
        support=sscent[key]/numitems
        if support >= minsupport:
            retlist.insert(0,key)
        supportdata[key]=support
    return retlist,supportdata


def apriorigen(lk,k):
    retlist=[]
    lenlk=len(lk)
    for i in range(lenlk):
        for j in range(i+1,lenlk):
            l1=list(lk[i])[:k-2]
            l2=list(lk[j])[:k-2]
            if l1==l2:
                retlist.append(lk[i] | lk[j])
    return retlist


def apriori(dataset,minsupport=0.5):
    c1=createC1(dataset)
    D=list(map(set,dataset))  #又是版本
    print(D)
    L1,supportdata=scan(D,c1,minsupport)
    L=[L1]
    k=2
    while (len(L[k-2])>0):
        ck=apriori(L[k-2],k)  #这个地方巧妙的用k k也表示想要的到的频繁集大小
        Lk,supk=scan(D,ck,minsupport)
        supportdata.update(supk)
        L.append(Lk)
        k+=1
    return L,supportdata


def generaterules(L,supportdata,minconf=0.7):
    bigruleslist=[]
    for i in range(1,len(L)):
        for freset in L[i]:  #freset还是列表
            H1=[frozenset([item]) for item in freset]  #[frozenset([item]) for item in frozenset([1,2,3]]的结果
                                                       # [frozenset({1}), frozenset({2}), frozenset({3})]

            if i>1:
                rulesfromconseq(freset,H1,supportdata,bigruleslist,minconf)
            else:
                calcconf(freset,H1,supportdata,bigruleslist,minconf)
    return bigruleslist


def calcconf(freqset,H,supportdata,br1,minconf=0.7):
    prunedH=[]
    for conseq in H:
        conf = supportdata[freqset]/supportdata[freqset-conseq]
        if conf<minconf:
            print(freqset-conseq,'---->',conseq,'conf:',conf)
            br1.append((freqset-conseq,conseq,conf))
            prunedH.append(conseq)
        return prunedH



def rulesfromconseq(freqset,H,supportdata,br1,miniconf=0.7):
    m=len(H[0])  #始终等于1，除非是最后的空
    if len(freqset) > m+1:  #H是[frozenset({1}), frozenset({2})]这样的，也就是制作两个元素的的频繁集，没有两个以上的
        hmp1=apriorigen(H,m+1)
        hmp1=calcconf(freqset,hmp1,supportdata,br1,miniconf)
        if len(hmp1)>1:
            rulesfromconseq(freqset,hmp1,supportdata,br1,miniconf)


















