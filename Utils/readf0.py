import os

import numpy as np


def read_f0_file(file_path):
    # 读取.f0文件内容
    with open(file_path, 'r') as f:
        lines = f.readlines()

    # 解析.f0文件内容，提取频率数据
    result_times = []
    result_pitches = []
    for i in range(len(lines)):
        if i < 8:
            continue
        if lines[i].strip():  # 忽略空行
            f0num = lines[i].split()
            result_time = float(f0num[0])
            result_pitch = float(f0num[2])

            result_times.append(result_time)
            result_pitches.append(result_pitch)

    return np.array(result_pitches), np.array(result_times)


def getf0name(targetfolder):
    # 遍历目录中的每个文件
    f0_list = []
    for filename in os.listdir(targetfolder):
        # 判断文件是否为CSV格式（根据文件后缀进行判断）
        if filename.endswith('.f0'):
            f0_list.append(filename)
    return np.array(f0_list)


if __name__ == '__main__':
    print(read_f0_file("../resultpitch/REAPER/" + getcsvname("../resultpitch/REAPER")[0]))
