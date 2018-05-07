'''
按照单一属性原则，我们应该划分为两个类，一个是数据处理类，将数据输出为标准化，一个是机器学习算法类
数据处理：首先是数据格式，先判断数据格式
        然后是对缺省值得处理，这里默认丢弃有缺省值的行
        然后对异常值进行处理，这里细节太多，不太好统一
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
import pandas as pd
import time

class FileTypeError(TypeError):
    pass

class ParseData:

    def __init__(self,path):
        self._filepath=path
        self._dataset=None
        self._labels=None


    def parse_text(self):  # 无法应对缺省值
        with open(self._filepath) as fr:
            arraylines = fr.readlines()
        if ',' in arraylines[0]:
            symbols = ','
        elif len(arraylines[0].split('\t')) > 0:
            symbols = '\t'
        else:
            raise FileTypeError('该txt文件无法分割开')
        result=[]
        for line in arraylines:
            line = line.strip()
            split_line = line.split(symbols)
            result.append(split_line)
        df = pd.DataFrame(result)
        filename=self._filepath.split('\\')[-1].split('.')[0]
        self._filepath=r'F:\machine\file\outfile\%s%s.xlsx'% (filename,str(int(time.time())))
        print(self._filepath)
        df.to_excel(self._filepath)


    def parse_pandas(self):
        if self._filepath.split('.')[-1]:
            suffix = self._filepath.split('.')[-1]
        else:
            raise FileTypeError('没有找到文件后缀')
        if suffix in ['text', 'txt']:
            self.parse_text()
            suffix='xlsx'
        if suffix in ['xlsx', 'csv']:
            if suffix == 'csv':
                data = pd.read_csv(self._filepath)
            else:
                data = pd.read_excel(self._filepath)
            data = data.dropna()
            self._dataset=data.iloc[:, 0:-1].values
            self._labels=data.iloc[:, -1].values
        else:
            raise FileTypeError('找不到对应读取格式')


    def dataset(self):
        if self._dataset is None:
            self.parse_pandas()
        return self._dataset

    def labels(self):
        if self._labels is None:
            self.parse_pandas()
        return self._labels


def autonorm(dataset):
    minvals=dataset.min(0)
    maxvals=dataset.max(0)
    ranges=maxvals-minvals
    m=dataset.shape[0]
    normdataset=dataset-np.tile(minvals,(m,1))
    normdataset=normdataset/np.tile(ranges,(m,1))
    return normdataset

