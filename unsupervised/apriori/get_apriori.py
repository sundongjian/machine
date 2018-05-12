'''
这个过程是C1-->L1-->C2-->L2--->C3-->L3的过程，即先找到最少元素的频繁集，再根据频繁集来制作超集，再检查得到新的频繁集
比价难的是apriorigen。这是制作超集的函数。比如输入【{1,2,3}{1,2,4}{1,2,5}】这时k=4，固定住相邻的集合里的前两个元素，如固定
{1,2}{1,2}如果固定住的这两个元素相等，就将两个元素求并集返回
createC1：由apriori调用。将单个元素排序后进行frozenset处理装进列表（老的版本map已经是对象了，不可迭代
scanD：将新构造出来的项进行频繁集过滤处理
aprioriGen：用原来大小为m的频繁集构造大小为m+1的新项
apriori：调度函数，循环调用scanD，aprioriGen，用单个大小进行频繁集过滤，然后再创建大1的新频繁集，再过滤，再创建
generateRules：发现规则
calcConf：进行支持度计算
rulesFromConseq：将大于2的构造为m+1(事实就是2)的新项，进行支持度计算
'''


def createC1(dataSet):
    '''
    :param dataSet: 由每行数据个数可以不一样的组成，能够排序，也就是数字，字符串也可以但无太大意义
    :return: 经过frozenset处理的不重复单元素列表
    '''
    C1 = []
    for transaction in dataSet:
        for item in transaction:
            if not [item] in C1:
                C1.append([item])

    C1.sort()
    # return map(frozenset, C1)#frozen set, user can't change it.
    return list(map(frozenset, C1))


def scanD(D, Ck, minSupport):
    '''
    :param D: 列表里包着字典的格式，字典是dataset里每行整体
    :param Ck: 构造的新项
    :param minSupport: 最小支持度
    :return: 满足最小支持度的项组成的列表和每个项支持度统计的字典
    '''
    ssCnt = {}
    for tid in D:
        for can in Ck:
            if can.issubset(tid):
                # if not ssCnt.has_key(can): # python3 can not support
                if not can in ssCnt:
                    ssCnt[can] = 1
                else:
                    ssCnt[can] += 1
    numItems = float(len(D))
    retList = []  #
    supportData = {}
    for key in ssCnt:
        support = ssCnt[key] / numItems
        if support >= minSupport:
            retList.insert(0, key)
        supportData[key] = support
    return retList, supportData


def aprioriGen(Lk, k):
    '''
    :param Lk: 原来的项
    :param k: 构造成大小为k的项
    :return: 新项
    '''
    retList = []
    lenLk = len(Lk)
    for i in range(lenLk):
        for j in range(i + 1, lenLk):
            L1 = list(Lk[i])[:k - 2];
            L2 = list(Lk[j])[:k - 2]
            L1.sort();
            L2.sort()
            if L1 == L2:
                retList.append(Lk[i] | Lk[j])
    return retList


def apriori(dataSet, minSupport=0.5):
    '''
    :param dataSet: 每行数据数量可以不一样的数据集
    :param minSupport: 最小支持度
    :return: 频繁集组成的列表嵌套和支持度统计字典
    '''
    C1 = createC1(dataSet)
    D = list(map(set, dataSet))  # python3
    L1, supportData = scanD(D, C1, minSupport)  #
    L = [L1]
    k = 2
    while (len(L[k - 2]) > 0):
        Ck = aprioriGen(L[k - 2], k)
        Lk, supK = scanD(D, Ck, minSupport)
        supportData.update(supK)
        L.append(Lk)
        k += 1
    return L, supportData


def generateRules(L, supportData, minConf=0.7):
    '''
    :param L: 由apriori产生的频繁集列表
    :param supportData: #支持度字典
    :param minConf: 最小可信度
    :return: 规则列表
    '''
    bigRuleList = []
    for i in range(1, len(L)):

        for freqSet in L[i]:
            H1 = [frozenset([item]) for item in freqSet]

            if (i > 1):

                rulesFromConseq(freqSet, H1, supportData, bigRuleList, minConf)
            else:
                calcConf(freqSet, H1, supportData, bigRuleList, minConf)  # 调用函数2
    return bigRuleList


def calcConf(freqSet, H, supportData, brl, minConf=0.7):
    '''
    :param freqSet: 大频繁集项
    :param H: 子集项
    :param supportData: 支持度字典
    :param brl: 用来记录生成规则的列表
    :param minConf: 最小支持度
    :return:
    '''
    prunedH = []
    for conseq in H:
        conf = supportData[freqSet] / supportData[freqSet - conseq]
        if conf >= minConf:
            print(freqSet - conseq, '-->', conseq, 'conf:', conf)

            brl.append((freqSet - conseq, conseq, conf))
            prunedH.append(conseq)
    return prunedH


def rulesFromConseq(freqSet, H, supportData, brl, minConf=0.7):
    '''
    :param freqSet: 大频繁集项
    :param H: 单个子集
    :param supportData:
    :param brl:
    :param minConf:
    :return:
    '''
    m = len(H[0])
    if (len(freqSet) > (m + 1)):
        Hmp1 = aprioriGen(H, m + 1)
        Hmp1 = calcConf(freqSet, Hmp1, supportData, brl, minConf)
        if (len(Hmp1) > 1):
            rulesFromConseq(freqSet, Hmp1, supportData, brl, minConf)
