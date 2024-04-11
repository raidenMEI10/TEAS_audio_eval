import csv
import os




def ReadPitch(filename='result.csv'):
    pitch=[]
    pitch_time=[]

    with open(filename, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            pitch_time.append(row[0])
            pitch.append(row[1])

    return pitch, pitch_time

def getcsvname(targetfolder):
    # 遍历目录中的每个文件
    csv_list=[]
    for filename in os.listdir(targetfolder):
        # 判断文件是否为CSV格式（根据文件后缀进行判断）
        if filename.endswith('.csv'):
            csv_list.append(filename)
    return csv_list
