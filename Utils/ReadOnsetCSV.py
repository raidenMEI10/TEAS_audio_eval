import csv
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

def readonset(filename):
    onset = []
    offset = []

    with open(filename, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            onset.append(row[1])
            offset.append(row[2])

    return onset, offset
