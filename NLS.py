import numpy as np
import librosa
import re
import matplotlib.pyplot as plt
import os

plt.rcParams['font.sans-serif'] = ['SimSun']  # 设置中文字体为黑体
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
def aqurire_wav(path=''):
    wavfiles = []
    wav_datas = []
    for file in os.listdir(path):
        if file.endswith('.wav'):
            wavfiles.append(file)

    pattern = re.compile(r'[A-Z]+[0-9]')
    note_labels = []
    duration_times = []
    for name in wavfiles:
        note_labels.append(pattern.findall(name))
    # print(wavfiles)
    for wavfile in wavfiles:  # 这里修改了一下，适配 1/4 到 7/8 的部分。前面和后面的乱七八糟音没法卡零点，对小周期做DFT
        wav_data, sr = librosa.load('SeperatedVibratoMonos/'+wavfile, sr = 44100)
        duration_times.append(len(wav_data)/sr)#.wav总时长
        wav_data = wav_data[round(0.25*len(wav_data)):round(7/8*len(wav_data)):]
        # print(len(y))
        # print('***********************')
        wav_datas.append(wav_data)

    return wav_datas, sr, note_labels, duration_times
# 六个单音的wav_data组成的list

def cutsmall_audio(audio,sr,note_label):#切小窗
    # print(note_label[0])
    # print(type(note_label))#<class 'list'>
    # 打开文件并逐行读取数据
    with open('Pyin_Output/mono_HzMean_forSTFT.txt', 'r') as file:
        Pyin_NoteHzList={}#字典，key为note，value为hz
        for line in file:
            # 分割每一行数据并获取第二列（索引为1）的元素
            data = line.strip().split()
            # 将第二列元素添加到列表中
            Pyin_NoteHzList[data[0]]=data[1]
    # HZ = librosa.note_to_hz(note_label)
    HZ=Pyin_NoteHzList[note_label[0]]
    # print('HZ =',HZ)
    frame_time = 1/sr
    # print('frame_time =',frame_time)
    T = 1/float(HZ)
    # print('T =',T)
    zero_points = []
    wav_times = []
    for i in range(1,len(audio)):
        # print(audio[0],audio[1],audio[2])
        if audio[i] >0 and audio[i-1] < 0:  # 必须wav_data振幅波形图里 ↗ 这个方向
            zero_points.append( (i-1)*frame_time+abs(frame_time*audio[i-1]/(abs(audio[i])+abs(audio[i-1]))) )  # 所有的过零点
            # print('i =',i)

    modify_zero_points = []
    modify_zero_points.append(zero_points[0])
    while len(zero_points) > 1:
        zero_distance = []
        # for zero_point in zero_points:
        for index in range(1, len(zero_points)):
            zero_distance.append(abs(zero_points[index] - zero_points[0] - T))  # 每个过零点 与 第一个(坐标0)过零点 的距离，与一个周期T做减（越小则说明这两个过零点卡的周期最准，是所求）
        # print('zero_distance =',zero_distance)
        match = zero_distance.index(min(zero_distance)) + 1  # 匹配最正确的周期应该几个过零点为一周期。.index返回下标
        # if match!=2: print(count, '\'s match ≠ 2 ！！！=', match)
        # print("match =", match)
        # for zero_point in zero_points[match]:#0:match+1:match]:
        modify_zero_points.append(zero_points[match])
        zero_points = zero_points[match:]

    result_Strength = []
    # print('modify_zero_points =',modify_zero_points)
    for i in range(1, len(modify_zero_points)):
        temp_Strength = []
        temp_wav_time = []
        first=1
        for j in range(len(audio)):
            if j*frame_time > modify_zero_points[i]:  # print('break !')
                break
            elif j*frame_time > modify_zero_points[i-1]:  # print('append !')
                if first == 1:
                    temp_Strength.append(audio[j-1])  # 每对过零点 卡的周期 前一个采样点信号强度
                    temp_wav_time.append((j-1)*frame_time)  # 每对过零点 卡的周期 前一个采样点时间点：这样的周期才是完整的，如果只取两过零点中间的采样点会缺掉第一个负的强度导致两端强度一正一负
                    first+=1
                temp_Strength.append(audio[j])  # 每对过零点 卡的周期里的 信号强度
                temp_wav_time.append(j*frame_time)  # 每对过零点 卡的周期里的 时间点
        result_Strength.append(temp_Strength)
        wav_times.append(temp_wav_time)
        # print(len(temp_Strength))
    # print("zero_points =",zero_points)
    # print('result_Strength[0] =',result_Strength[0])
    return result_Strength, modify_zero_points, wav_times, match
# result：列表，其中每个元素都是一个小音频片段的数据。这些小音频片段是按照找到的零点位置和匹配的周期数来从原始音频信号中切割出来的。
# 第一个维度（外层列表）代表每个被切分出来的音频片段。第二个维度（内部列表）代表每个音频片段中的样本点：数据以时间序列形式存储，每一个样本点对应一个时间帧的音频信号的强度。
# 一个周期可能多上多下。出现重复的才算周期


def plot_result(y_ZeroResult, zero_point, wav_times):#match是跳距
    # print(y_ZeroResult[0][0],y_ZeroResult[0][1],y_ZeroResult[0][2])
    for i in range(len(y_ZeroResult)):
        y_zero_point = np.zeros(2)
        cut_zero = zero_point[i:i+2]
        plt.plot(wav_times[i],y_ZeroResult[i],linewidth=0.2)
        plt.scatter(wav_times[i], y_ZeroResult[i], color='b', s=10)
        plt.scatter(cut_zero,y_zero_point,color='r')
        plt.xlabel('time')
        plt.ylabel('audio')
        plt.show()

def Calculate_NLS(wav_data,zero_time,cycle_duration):#在DTFT基础上
    if len(zero_time)==2:
        parameter = float(zero_time[1]-zero_time[0])/float(cycle_duration[-1]-cycle_duration[0])
    else: parameter = 1
    N = len(wav_data)#125
    n = np.arange(N)
    k = n.reshape((N, 1))
    e = np.exp(-2j * np.pi * k * parameter * n / N)  # print(len(e))=125#print(e==e.T)#全是True
    # 2. 计算ATA矩阵
    EH=np.conjugate(e.T)#共轭对称#print(EH==e)大部分False
    # print(np.dot(EH, e))
    eeH = np.dot(e, EH)#本来是eTe，但是
    # eeH = np.dot(e, EH)#本来是eTe，但是
    # 3. 求ATA矩阵的逆矩阵
    # eeH_inverse = np.linalg.pinv(eeH)
    # print('\n\n\n\n')
    # print(e_inverse*e)
    # print('\n\n\n\n')
    # print(np.dot(e_inverse,e))
    # print('\n\n\n\n')
    # print(e_inverse*e == np.dot(e_inverse,e))
    # input()
    # return np.dot(np.dot(eeH_inverse,e), wav_data)  # 计算两个数组的点积
    return np.dot(np.dot(eeH,e), wav_data)  # 计算两个数组的点积。这个貌似图最对
    # return np.dot(eeH, wav_data)  # 计算两个数组的点积

def ForPlot_NLS(zero_result,zero_point,wav_time):#过零点卡周期的图，每帧内
    zero__result = zero_result - np.mean(zero_result)  # 使其中心点为0
    NLS_result = Calculate_NLS(zero__result,zero_point,wav_time)
    NLS_result = NLS_result[1:8]#[1:8]
    NLS_result = np.abs(NLS_result)
    NLS_result = NLS_result / np.max(abs(NLS_result))
    db_result = librosa.amplitude_to_db(NLS_result)
    return db_result

def Plot_Main(wav_data,sr,note_label,duration_time):
    resultStrength, zero_point, wav_time, match = cutsmall_audio(wav_data, sr, note_label)
    # plot_result(resultStrength, zero_point, wav_time)  # 画每个过零点卡出的周期内

    sample_rate = 44100
    win_len = 131
    image = []
    for n in range(len(resultStrength)):
        LENGTH=len(ForPlot_NLS(resultStrength[n],zero_point[2*n:2*n+2],wav_time[n]))
        new_ForPlot=ForPlot_NLS(resultStrength[n],zero_point[2*n:2*n+2],wav_time[n])
        if LENGTH!=7:
            for i in range(7-LENGTH):
                new_ForPlot=np.append(new_ForPlot,0)
            image.append(new_ForPlot)
        else:image.append(new_ForPlot)# + 70)  # dB最小值变为0
    # for n in range(len(resultStrength)):#212次循环，7s半一次 = 26.5分钟
    #     image.append(ForPlot_NLS(resultStrength[n],zero_point[2*n:2*n+2],wav_time[n]))# + 70)  # dB最小值变为0

    image = [[image[j][i] for j in range(len(image))] for i in range(len(image[0]))]
    image = np.array(image)
    # plt.figure()
    plt.subplot(7, 1, 7)
    # print('image=', image)
    # print('image.shape=', image.shape[1])
    # 转置频谱数据，将频率显示在纵轴上，时间步长显示在横轴上
    plt.imshow(image, cmap='inferno', aspect='auto', origin='lower')  # , extent=[0, 2, 0, image.shape[0]])
    # librosa.display.specshow(image, sr=sample_rate, win_length=win_len, n_fft=win_len, hop_length=win_len, x_axis='time')
    y_ticks = [0, 1, 2, 3, 4, 5, 6]  # 设置刻度的位置
    y_tick_labels = ["F0", "F1", "F2", "F3", "F4", "F5", "F6"]  # 设置刻度的标签
    plt.yticks(y_ticks, y_tick_labels)  # 设置纵坐标刻度和标签
    plt.title('基于NLS的连续音高同步泛音谱')  # 离散音高同步谱')#'DFT 1-E4 Spectrogram')
    start_time = duration_time * 0.25
    # 设置自定义 x 轴刻度位置和标签
    def average_adjacent_elements(input_list, startTime):
        # 新的长度为334的列表
        result_list = []
        for i in range(0, len(input_list) - 1):
            # 求相邻两个数的均值
            average = startTime + (input_list[i] + input_list[i + 1]) / 2.0
            if i % 30 == 0:
                # 将均值添加到结果列表中
                result_list.append(round(average, 3))
        return result_list

    plt.xticks(np.arange(0, image.shape[1], 30), average_adjacent_elements(zero_point, start_time))
    # plt.xlim(0-start_time,2-start_time)#0,2))
    plt.xlabel('')  # '时间(秒)')#'Time') 大图里最底下显示这仨字即可
    plt.ylabel('泛音列')  # '谐波Harmonics')

def NLS_Main(choice):
    audiopath = 'SeperatedVibratoMonos'  # 存放六个单音.wav的文件夹
    wav_datas,sr,note_labels,duration_times=aqurire_wav(audiopath)#print(sr)#44100

    note_labels[1]=['F#4']
    # print('note_labels=',note_labels)
    Plot_Main(wav_datas[choice],sr,note_labels[choice],duration_times[choice])

    # print(all_results)
    # print(sr)


if __name__ == '__main__':
    NLS_Main(2)#3-A4






