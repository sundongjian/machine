'''
这个树有些复杂，需要用到数据结构
createinitset：将每行数据做frozenset处理之后做成字典
treeNode：做成的节点抽象数据类型
createtree：创建树
updateTree：更新树
updateheader：相同元素指针

'''


def createinitset(dataset):
    retdict = {}
    for trains in dataset:
        retdict[frozenset(trains)] = 1
    return retdict


class treeNode:
    def __init__(self, namevalue, numoccur, parentNode):
        '''
        self.nodelink：保存下一个相同节点的信息
        :param namevalue: 单个元素
        :param numoccur: 数量
        :param parentNode: 父节点，此处没有用到
        '''
        self.name = namevalue  # 名字
        self.nodelink = None  #
        self.count = numoccur  # 计数
        self.parent = parentNode  # 父节点
        self.children = {}  # 子节点

    def inc(self, numoccur):
        self.count += numoccur

    def disp(self, ind=1):
        '''
        :param ind: 可以将树可视化表现出来
        :return:
        '''
        print(' ' * ind, self.name, ' ', self.count)
        for child in self.children.values():
            child.disp(ind + 1)


def createtree(dataset, minsup):
    '''
    :param dataset:经过 createinitset函数处理过的数据
    :param minsup: 最小支持度
    :return: 树和指针
    '''
    headertable = {}
    for exm in dataset:
        for item in exm:
            headertable[item] = headertable.get(item, 0) + dataset[exm]  # 这里为什么不+1 又是用的frozenset，可害苦我了
    print(headertable)
    for k in headertable.keys():
        if headertable[k] < minsup:
            del headertable[k]
    freqitemset = set(headertable.keys())
    if len(freqitemset) == 0:
        return None, None
    for k in headertable:
        headertable[k] = [headertable[k], None]
    print(headertable)
    rettree = treeNode('null set', 1, None)
    for trainset, count in dataset.items():
        localid = {}
        for item in trainset:
            if item in freqitemset:
                localid[item] = headertable[item][0]  # 这个地方应该没有[0]有--->重定义headertable[k]=[headertable[k],None]
        if len(localid) > 0:
            # ordereditems1=[m[1] for m in sorted(zip(localid.values(),localid.keys()),reverse=True)]
            ordereditems = [v[0] for v in sorted(localid.items(), key=lambda p: p[1], reverse=True)]
            print(ordereditems)
        updateTree(ordereditems, rettree, headertable, count)
    return rettree, headertable


def updateTree(items, intree, headertable, count):
    '''
    :param items: createtree调用时传进的参数，是经过排序的完整一行
    :param intree: 树结构
    :param headertable: 指针字典，如果有，value为指向该元素的节点
    :param count: 改整行的value值，也就是1
    :return: 只有树结构操作，无返回值
    '''
    if items[0] in intree.children:
        intree.children[items[0]].inc(count)  # 如果items[0]是这个节点的一个子节点
    else:
        intree.children[items[0]] = treeNode(items[0], count, intree)  # 如果不是，另外创建一个作为子节点
        if headertable[items[0]][1] == None:
            headertable[items[0]][1] = intree.children[items[0]]  # 记录当前的位置
        else:
            updateheader(headertable[items[0]][1], intree.children[items[0]])  # 更新当前的位置
    if len(items) > 1:
        updateTree(items[1::], intree.children[items[0]], headertable, count)  # 这个[1::]最后一个：后面跟跳几个


def updateheader(nodertotest, targetnode):
    '''
    headertable[items[0]][1]即nodertotest里存储的是一个节点，如果存储的这个节点的nodelink是none，那么直接将新节点
    赋值为存储的这个节点的nodelink属性
    这个时候这个节点的nodelink属性已经不是none了，如果这时候又有一个相同元素要加入，那么就要作为属性赋值给这个链条的末端
    nodelink属性
    :param nodertotest:指针字典里存储的节点
    :param targetnode:现在等待连接同元素的节点
    :return:
    '''
    while nodertotest.nodelink != None:
        nodertotest = nodertotest.nodelink
    nodertotest.nodelink = targetnode
