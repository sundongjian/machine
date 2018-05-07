'''
按照单一属性原则，我们应该划分为两个类，一个是数据处理类，将数据输出为标准化，一个是机器学习算法类
数据处理：首先是数据格式，先判断数据格式
        然后是对缺省值得处理，这里默认丢弃有缺省值的行
        然后对异常值进行处理
        数据处理过程标准化有点难，我们可以用四分位数消除异常值，但是如果数量过少怎么办
        最后返回数据的属性，如数据的行数等等
数据格式分为两类，一类是text格式，这个需要按行读取，另一类是csv，xls，因此按照工厂模式
这里考虑是不是需要进行数据的标准化
数据处理用pandas，输出为numpy，这样比较合理
ADT AnalyzeData:
    AnalyzeData(self,path)
    num
'''
import numpy as np
import  pandas as pd
class FileTypeError(TypeError):
    pass

def parse_text(filepath):#无法应对缺省值
    with open(filepath) as fr:
        arraylines=fr.readlines()
    numberlines=len(arraylines)
    column=len(arraylines[0].split('\t'))-1
    returnmat=np.zeros(numberlines,column)
    classlabels=[]
    index=0
    for line in arraylines:
        line=line.strip()
        split_line=line.split['\t']
        returnmat[index,:]=split_line[0:-1]
        classlabels.append(split_line[-1])
        index+=1
    return returnmat,classlabels


def parse_pandas(filepath,suffix):
    if suffix=='csv':
        data=pd.read_csv(filepath)
    else:
        data=pd.read_excel(filepath)
    return data[0:-1].values,data[-1].values


def parse_data(filepath):
    if filepath.split('.')[-1]:
        suffix=filepath.split('.')[-1]
    else:
        raise FileTypeError('没有找到文件后缀')
    if suffix in ['text' ,'txt']:
        parse_text(filepath)
    elif suffix in ['xls' ,'csv']:
        parse_pandas(filepath,suffix)
    else:
        raise FileTypeError('找不到对应读取格式')


