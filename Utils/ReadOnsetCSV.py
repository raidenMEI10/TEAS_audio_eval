import os

import numpy as np
import pandas as pd

def getonsetname(foldpath):
    # 遍历目录中的每个文件
    csv_list = []
    for filename in os.listdir(foldpath):
        # 判断文件是否为CSV格式（根据文件后缀进行判断）
        if filename.endswith('.csv'):
            csv_list.append(filename)
    return csv_list

def readonset(foldpath):
    csv_list = getonsetname(foldpath)
    list = []
    for file in csv_list:
        data = pd.read_csv(foldpath+'/'+file, header=None)
        list.append(data[0])
    return np.array(list), csv_list
