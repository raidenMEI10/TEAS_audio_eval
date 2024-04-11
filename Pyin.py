import librosa
import math
import numpy as np


def pyin1_normal():
    # 加载音频文件
    filename = './audio_data/高山流水.wav'
    audio_data, sample_rate = librosa.load(filename, sr=48000)
    hop = 240
    length = 2048  # 288
    frame_hop = hop / sample_rate
    frame_len = length / sample_rate
    print('帧移', frame_hop, 's', '\n帧长', frame_len, 's')
    # print(f"帧移 {441/sample_rate}s")

    # 使用pYIN算法进行音高估计
    f0, voiced_flag, voiced_probs = librosa.pyin(audio_data, sr=sample_rate, hop_length=hop, frame_length=length,
                                                 fmin=librosa.note_to_hz('C2'), fmax=librosa.note_to_hz(
            'C7'))  # 琵琶最低音A2(标的A4实则低两个八度)，最高音E6(标的E8实则低两个八度)

    # 打印结果
    print('f0.size = ', f0.size)
    print('起始时间 结束时间')
    file = open("Pyin_Output/PyinOutput_All.txt", "w")
    for i in range(f0.size):
        StartTime = '{:.3f}'.format(round(frame_hop * (i), 4))  # <class 'str'>
        EndTime = '{:.3f}'.format(round(frame_len + frame_hop * (i), 4))  # <class 'str'>
        Hz = f0[
            i]  # <class 'str'> else float # Hz='{:.2f}'.format(round(f0[i],2)) if not math.isnan(f0[i]) else f0[i]#<class 'str'> else float
        midi = round(librosa.hz_to_midi(f0[i])) if not math.isnan(f0[i]) else f0[i]
        midi = str(midi)
        note = librosa.hz_to_note(f0[i]) if not math.isnan(f0[i]) else f0[i]
        note = str(note)
        note = note.replace("♯", "#")
        Prob = " {:^22}".format(voiced_probs[i])
        # print(StartTime, EndTime, "{:^21}".format(Hz), "{:^4}".format(midi), "{:^4}".format(note), voiced_flag[i], Prob)#print(type(voiced_flag[i]))#<class 'numpy.bool_'>
        file.write(
            StartTime + ' ' + EndTime + ' ' + "{:^21}".format(Hz) + ' ' + "{:^4}".format(midi) + ' ' + "{:^4}".format(
                note) + ' ' + Prob + "\n")
    # 关闭文件
    file.close()


def pyin2_plotTXT():
    # 加载音频文件
    filename = './audio_data/高山流水.wav'
    audio_data, sample_rate = librosa.load(filename, sr=48000)
    hop = 240
    length = 2048  # 288
    frame_hop = hop / sample_rate
    frame_len = length / sample_rate
    print('帧移', frame_hop, 's', '\n帧长', frame_len, 's')

    # 使用pYIN算法进行音高估计
    f0, voiced_flag, voiced_probs = librosa.pyin(audio_data, sr=sample_rate, hop_length=hop, frame_length=length,
                                                 fmin=librosa.note_to_hz('C2'), fmax=librosa.note_to_hz(
            'C7'))  # 琵琶最低音A2(标的A4实则低两个八度)，最高音E6(标的E8实则低两个八度)

    # 打印结果
    print('f0.size = ', f0.size)
    print('起始时间 结束时间')
    NotesOutput_Files = {
        'E4': 'Pyin_PlotOut/Progress/1 PyinPlotOut_E4.txt',
        'F#4': 'Pyin_PlotOut/Progress/2 PyinPlotOut_F#4.txt',
        'A4': 'Pyin_PlotOut/Progress/3 PyinPlotOut_A4.txt',
        'B4': 'Pyin_PlotOut/Progress/4 PyinPlotOut_B4.txt',
        'D5': 'Pyin_PlotOut/Progress/5 PyinPlotOut_D5.txt',
        'E5': 'Pyin_PlotOut/Progress/6 PyinPlotOut_E5.txt'
    }
    for i in range(6):
        TXTname = list(NotesOutput_Files.values())[i]
        with open(TXTname, 'w') as outfile:  # 使用 'w' 模式打开文件，清空文件内容
            pass
    for i in range(f0.size):
        StartTime = '{:.3f}'.format(round(frame_hop * i, 4))  # <class 'str'>
        # EndTime = '{:.3f}'.format(round(frame_len + frame_hop * i, 4))  # <class 'str'>
        midi = librosa.hz_to_midi(f0[i]) if not math.isnan(f0[i]) else f0[i]
        midi = str(midi)
        note = librosa.hz_to_note(f0[i]) if not math.isnan(f0[i]) else f0[i]
        note = str(note)
        note = note.replace("♯", "#")
        # if voiced_probs[i] > 0.5:
        if note in NotesOutput_Files:
            output_file = NotesOutput_Files[note]
            with open(output_file, 'a') as file:  # 'a' 表示以追加模式（Append Mode）打开文件。'w'才是覆盖
                file.write(StartTime + ' ' + "{:^21}".format(midi) + "\n")
                # file.write(StartTime + ' ' + EndTime + ' ' + "{:^21}".format(midi) + ' ' + "{:^4}".format(note) + "\n")


def pyin1_write():
    # 定义文件路径
    input_file = 'Pyin_Output/PyinOutput_All.txt'
    output_files = {
        'E4': 'Pyin_Output/1 PyinOutput_E4.txt',
        'F#4': 'Pyin_Output/2 PyinOutput_F#4.txt',
        'A4': 'Pyin_Output/3 PyinOutput_A4.txt',
        'B4': 'Pyin_Output/4 PyinOutput_B4.txt',
        'D5': 'Pyin_Output/5 PyinOutput_D5.txt',
        'E5': 'Pyin_Output/6 PyinOutput_E5.txt'
    }
    # 打开输入文件进行读取和处理
    with open(input_file, 'r') as file:
        lines = file.readlines()
    for i in range(6):
        TXTname = list(output_files.values())[i]
        with open(TXTname, 'w') as file:  # 使用 'w' 模式打开文件，清空文件内容
            pass
    # 根据第五列的值将行写入对应的文件
    for line in lines:
        data = line.strip().split()
        if len(data) >= 5:
            value = data[4]
            if value in output_files:
                output_file = output_files[value]
                with open(output_file, 'a') as file:  # 'a' 表示以追加模式（Append Mode）打开文件。'w'才是覆盖
                    file.write(line)
    # print所有的.txt文件名
    output_files_list = list(output_files.values())
    print()
    print(output_files_list)
    print("文件写入完成 ！")


def fromPyin2Seperate():
    def read_float_from_file(file_path):
        with open(file_path, 'r') as file:
            first_line = file.readline()
            last_line = file.readlines()[-1]
            first_float = float(first_line.split()[0])
            last_float = float(last_line.split()[0])  # 1])
            return first_float, last_float

    file_names = [
        'Pyin_Output/1 PyinOutput_E4.txt',
        'Pyin_Output/2 PyinOutput_F#4.txt',
        'Pyin_Output/3 PyinOutput_A4.txt',
        'Pyin_Output/4 PyinOutput_B4.txt',
        'Pyin_Output/5 PyinOutput_D5.txt',
        'Pyin_Output/6 PyinOutput_E5.txt'
    ]
    notes = ['E4', 'F#4', 'A4', 'B4', 'D5', 'E5']
    output_lines = []
    i = 0
    for file_name in file_names:
        first_float, last_float = read_float_from_file(file_name)
        a_formatted = "{:.1f}".format(first_float - 0.05)
        b_formatted = "{:.1f}".format(last_float - 0.05)
        output_lines.append(f"{notes[i]}   {a_formatted}   {b_formatted}\n")
        i += 1
    with open('Pyin_Output/SeperateWavByNote.txt', 'w') as output_file:
        output_file.writelines(output_lines)


def mono_hzmeanAndwinlength_forstft_writeTXT():
    def calculate_mean_of_column(file_path, column_index):
        with open(file_path, 'r') as file:
            column_data = [float(line.split()[column_index - 1]) for line in file]
            mean_value = sum(column_data) / len(column_data)
            return mean_value

    file_names = [
        'Pyin_Output/1 PyinOutput_E4.txt',
        'Pyin_Output/2 PyinOutput_F#4.txt',
        'Pyin_Output/3 PyinOutput_A4.txt',
        'Pyin_Output/4 PyinOutput_B4.txt',
        'Pyin_Output/5 PyinOutput_D5.txt',
        'Pyin_Output/6 PyinOutput_E5.txt'
    ]
    notes = ['E4', 'F#4', 'A4', 'B4', 'D5', 'E5']
    output_lines = []
    i = 0
    for file_name in file_names:
        hz_mean = calculate_mean_of_column(file_name, column_index=3)
        output_lines.append(f"{notes[i]}   {hz_mean}   {round(1 / hz_mean * 44100)}\n")
        i += 1
    with open('Pyin_Output/mono_HzMean_forSTFT.txt', 'w') as output_file:
        output_file.writelines(output_lines)


def pyin2_writePlotTXT():
    def read_and_match_and_modify_data(pyinOUT_list, startend_filename):
        # 步骤1：读取.txt文件B并提取起始时间和结束时间
        start_end_times = []
        with open(startend_filename, 'r') as file:
            lines = file.readlines()
            for line in lines:
                line = line.strip().split()[1:]
                start, end = map(float, line)
                start_end_times.append((start, end))
        # 步骤2：读取.txt文件中的数据  # print(line)#['10.2', '12.7']，之前错误原因
        data_list = []
        min_time = []
        max_time = []
        for filename in pyinOUT_list:
            with open(filename, 'r') as file:
                lines = file.readlines()
                times = [float(line.split()[0]) for line in lines]
                min_time.append(times[0])
                max_time.append(times[-1])  # pyin结果里最早和最晚
                data_list.append(lines)
        # 步骤3：匹配起始时间和结束时间，并进行必要的修改
        modified_data_list = []
        for i, datas in enumerate(data_list):  # print(datas)
            start, end = start_end_times[i]
            modified_data = []
            # print(datas)
            # for data in datas:
            #     print(data)
            #     time, value = map(float, data.split())
            while True:  # line = datas[0][0] # time = float(line[0])
                time = float(datas[0].split()[0])
                time = round(time, 3)
                start = round(start, 3)
                end = round(end, 3)
                if time <= end:  # 开始这个音
                    if min_time[i] > start:  # 在开头补0
                        # print('min_time[i] > start，在开头补0。')
                        modified_data.append(f"{str(start)} 0\n")
                        start += 0.005
                    elif len(datas) > 1:
                        # print('len(datas) > 1，正常添加pyin结果')
                        modified_data.append(datas[0])
                        datas = datas[1:]
                    elif len(datas) == 1:  # 没发生过
                        print('len(datas) == 1，pyin结果的最后一个音。')  # 没发生过
                        modified_data.append(line)
                        if max_time[i] < end:
                            print('max_time[i] < end，末尾补0 ！')  # 没发生过
                            modified_data.append(f"{str(time)} 0\n")
                            max_time[i] += 0.005
                        elif max_time[i] == end:
                            print('max_time = end，末尾补0 ！')  # 没发生过
                            modified_data.append(f"{str(time)} 0\n")
                            break
                elif time > end:  # 到下个单音了
                    print('time > end ! Break !')
                    break
            print(modified_data)
            modified_data_list.append(modified_data)

        return modified_data_list

    # 需要处理的六个含有两列数据的.txt文件列表
    input_SIXtxt_list = ['Pyin_PlotOut/Progress/1 PyinPlotOut_E4.txt', 'Pyin_PlotOut/Progress/2 PyinPlotOut_F#4.txt',
                         'Pyin_PlotOut/Progress/3 PyinPlotOut_A4.txt',
                         'Pyin_PlotOut/Progress/4 PyinPlotOut_B4.txt', 'Pyin_PlotOut/Progress/5 PyinPlotOut_D5.txt',
                         'Pyin_PlotOut/Progress/6 PyinPlotOut_E5.txt']

    # 步骤3：读取.txt文件，匹配起始时间和结束时间，并在开头和结尾补0
    # modified_data_list = match_and_modify_data(filled_data_list, start_end_times)
    modified_data_list = read_and_match_and_modify_data(input_SIXtxt_list, 'Pyin_Output/SeperateWavByNote.txt')
    # print(modified_data_list)
    # 将修改后的数据写入新的.txt文件
    outputs = ['Pyin_PlotOut/1 PyinPlotOut_E4.txt', 'Pyin_PlotOut/2 PyinPlotOut_F#4.txt',
               'Pyin_PlotOut/3 PyinPlotOut_A4.txt',
               'Pyin_PlotOut/4 PyinPlotOut_B4.txt', 'Pyin_PlotOut/5 PyinPlotOut_D5.txt',
               'Pyin_PlotOut/6 PyinPlotOut_E5.txt']
    for i, modified_data in enumerate(modified_data_list):
        with open(outputs[i], 'w') as file:
            file.writelines(modified_data)


def pyin_Main():
    pyin1_normal()
    pyin1_write()
    fromPyin2Seperate()
    mono_hzmeanAndwinlength_forstft_writeTXT()

    pyin2_plotTXT()
    pyin2_writePlotTXT()


if __name__ == '__main__':
    # pyin2_plotTXT()
    pyin2_writePlotTXT()
    # pyin1_normal()
    # pyin_write()
    # fromPyin2Seperate()
    # mono_hzmeanAndwinlength_forstft_writeTXT()
    # Pyin_PlotBoxesLines()
