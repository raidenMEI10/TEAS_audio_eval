import math

import librosa
import mido

from NLS import aqurire_wav

def pyin_used():
    # 加载音频文件
    filename = './audio_data/高山流水.wav'
    print("to here")
    audio_data, sample_rate = librosa.load(filename, sr=48000)
    hop = 240
    length = 2048  # 288
    frame_hop = hop / sample_rate
    frame_len = length / sample_rate
    print('帧移', frame_hop, 's', '\n帧长', frame_len, 's')
    # print(f"帧移 {441/sample_rate}s")

    # 使用pYIN算法进行音高估计
    f0, voiced_flag, voiced_probs = librosa.pyin(audio_data, sr=sample_rate, hop_length=hop, frame_length=length)  # 琵琶最低音A2(标的A4实则低两个八度)，最高音E6(标的E8实则低两个八度)

    # 打印结果
    print('f0.size = ', f0.size)
    print('起始时间 结束时间')
    for i in range(f0.size):
        StartTime = '{:.3f}'.format(round(frame_hop * (i), 4))  # <class 'str'>
        EndTime = '{:.3f}'.format(round(frame_len + frame_hop * (i), 4))  # <class 'str'>
        Hz = f0[i]  # <class 'str'> else float # Hz='{:.2f}'.format(round(f0[i],2)) if not math.isnan(f0[i]) else f0[i]#<class 'str'> else float
        midi = round(librosa.hz_to_midi(f0[i])) if not math.isnan(f0[i]) else f0[i]
        midi = str(midi)
        note = librosa.hz_to_note(f0[i]) if not math.isnan(f0[i]) else f0[i]
        note = str(note)
        note = note.replace("♯", "#")
        Prob = " {:^22}".format(voiced_probs[i])

def read_midi():
    # 打开MIDI文件
    pattern = mido.MidiFile('./audio_data/高山流水.mid')

    for i, track in enumerate(pattern.tracks):  # enumerate()：创建索引序列，索引初始为0
        print('Track {}: {}'.format(i, track.name))
        note_start_time = []
        list = []
        note_end_time = []
        pitches = []
        temp = 0
        print(type(track))
        for msg in track:
            list.append(msg)

        for msg in list:  # 每个音轨的消息遍历
            print(msg)
            if msg.type == 'note_on':
                note_start_time.append(msg.time + temp)
                pitches.append(msg.note)
                temp += msg.time
                for i in range(len(list)):
                    if list[i].note == msg.note and list[i].type == 'note_off':
                        note_end_time.append(list[i].time + temp)
                        temp += msg.time
                        del list[i]
        return note_start_time, note_end_time, pitches


def audio_eval(name):
    if name == 'Pyin':
        pyin_used()

    elif name == 'BNLS':
        aqurire_wav('audio_data')


if __name__ == '__main__':
    audio_eval('Pyin')
