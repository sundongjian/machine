'''
ParseData:读取文件路径（文件格式：text、txt、xlsx、csv）返回numpy格式数据，数据以方法调用形式返回
autonorm：将numpy数据标准化
'''
import numpy as np
import pandas as pd
import time


class FileTypeError(TypeError):
    pass


class ParseData:


    def __init__(self, path):
        self._filepath = path
        self._dataset = None
        self._labels = None
        self._entry_data = None

    def _parse_text(self):
        '''
        将txt，text文件转化为xlsx文件
        :return: 无返回值，改变属性值
        '''
        with open(self._filepath) as fr:
            arraylines = fr.readlines()
        if ',' in arraylines[0]:
            symbols = ','
        elif len(arraylines[0].split('\t')) > 0:
            symbols = '\t'
        else:
            raise FileTypeError('该txt文件无法分割开')
        result = []
        for line in arraylines:
            line = line.strip()
            split_line = line.split(symbols)
            result.append(split_line)
        df = pd.DataFrame(result)
        filename = self._filepath.split('\\')[-1].split('.')[0]
        self._filepath = r'F:\machine\file\outfile\%s%s.xlsx' % (filename, str(int(time.time())))
        print(self._filepath)
        df.to_excel(self._filepath)

    def _parse_pandas(self):
        '''
        根据数据后缀选择读取方式，简单去缺省值
        :return: 无返回值，直接改变属性值
        '''
        if self._filepath.split('.')[-1]:
            suffix = self._filepath.split('.')[-1]
        else:
            raise FileTypeError('没有找到文件后缀')
        if suffix in ['text', 'txt']:
            self._parse_text()
            suffix = 'xlsx'
        if suffix in ['xlsx', 'csv']:
            if suffix == 'csv':
                data = pd.read_csv(self._filepath)
            else:
                data = pd.read_excel(self._filepath)
            data = data.dropna()
            self._dataset = data.iloc[:, 0:-1].values
            self._labels = data.iloc[:, -1].values
            self._entry_data = data.values
        else:
            raise FileTypeError('找不到对应读取格式')

    def dataset(self):
        '''
        :return: 返回numpy数据，此数据不包含labels列
        '''
        if self._dataset is None:
            self._parse_pandas()
        return self._dataset

    def labels(self):
        '''
        :return: 返回numpy数据，数据的labels列
        '''
        if self._labels is None:
            self._parse_pandas()
        return self._labels

    def entry_data(self):
        '''
        返回整个数据
        :return:
        '''
        if self._entry_data is None:
            self._parse_pandas()
        return self._entry_data


def autonorm(dataset):
    '''
    :param dataset: dataset是numpy格式数据，不含labels列
    :return: 标准化之后的numpy格式数据
    '''
    minvals = dataset.min(0)
    maxvals = dataset.max(0)
    ranges = maxvals - minvals
    m = dataset.shape[0]
    normdataset = dataset - np.tile(minvals, (m, 1))
    normdataset = normdataset / np.tile(ranges, (m, 1))
    return normdataset
