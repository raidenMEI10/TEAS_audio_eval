import math

import mir_eval
import numpy as np

from Utils import ReadCSV, readf0


def modifyarray(pitch, time):
    onsettime = []
    offsettime = []
    modifypitch = []

    for i in range(len(pitch) - 1):
        if pitch[i] == 0:
            continue

        if abs(pitch[i] - pitch[i + 1]) > 1.5:
            for j in range(i + 1, len(pitch) - 1):
                if pitch[j] == 0:
                    break
                if abs(pitch[j] - pitch[j + 1]) > 1.5:
                    onsettime.append(time[i])
                    offsettime.append(time[j])
                    modifypitch.append(pitch[(i + j) // 2])
                    i = j
                    break

    modifypitch = np.array(modifypitch)
    newtime = np.column_stack((np.array(onsettime), np.array(offsettime)))
    print("size of newtime is", newtime.shape)
    newtime = np.array(newtime)

    return modifypitch, newtime


def mypitch_eval(estimate_path, GT_csvpath, Method):
    precisionlist = []
    recalllist = []
    F1scorelist = []
    if Method == 'REAPER':
        estimate_list = readf0.getf0name(estimate_path + '/' + Method)
    else:
        estimate_list = ReadCSV.getcsvname(estimate_path + '/' + Method)

    GT_list = ReadCSV.getcsvname(GT_csvpath)
    for i in range(len(estimate_list)):
        if Method == 'REAPER':
            estimate_pitch, estimate_time = readf0.read_f0_file(estimate_path + '/' + Method + '/' + estimate_list[i])
        # elif Method == 'BNLS':
        #     estimate_pitch, estimate_time = ReadCSV.ReadPitch(estimate_path + '/' + Method + '/' + estimate_list[i])
        #     estimate_pitch = np.array([float(x) for x in estimate_pitch])
        #     print(len(estimate_pitch))
        #     for j in range(len(estimate_pitch)):
        #         if j==0:
        #             k=0
        #         if math.isnan(estimate_pitch[k]):
        #             estimate_pitch = np.delete(estimate_pitch, k)
        #             estimate_time=np.delete(estimate_time, k)
        #             k = k-1
        #         k = k+1
        #     print(len(estimate_pitch))
        else:
            estimate_pitch, estimate_time = ReadCSV.ReadPitch(estimate_path + '/' + Method + '/' + estimate_list[i])
        GT_pitch, GT_time = ReadCSV.ReadPitch(GT_csvpath + '/' + GT_list[i])
        print(max(GT_pitch))
        print(min(GT_pitch))
        print(type(estimate_pitch))

        GT_time = np.array([float(x) for x in GT_time])
        GT_pitch = np.array([float(x) for x in GT_pitch])
        estimate_pitch = np.array([float(x) for x in estimate_pitch])
        estimate_time = np.array([float(x) for x in estimate_time])  # 转变为np数组

        # min_len = min(len(estimate_pitch), len(GT_pitch))
        # GT_time = GT_time[0: min_len]
        # GT_pitch = GT_pitch[0: min_len]
        # estimate_pitch = estimate_pitch[0: min_len]
        # estimate_time = estimate_time[0: min_len]  # 使得二者同长度

        GT_pitch = np.fromstring(GT_pitch)
        GT_time = np.array(GT_time)



        # GT_pitch = [GT_pitch]
        # estimate_pitch = [estimate_pitch]
        # print(GT_pitch[0].shape)
        # print(GT_time.shape)

        (ref_v, ref_c,
         est_v, est_c) = mir_eval.melody.to_cent_voicing(GT_time,
                                                         GT_pitch,
                                                         estimate_time,
                                                         estimate_pitch)
        raw_pitch = mir_eval.melody.raw_chroma_accuracy(ref_v, ref_c,
                                                       est_v, est_c)
        raw_chroma_t50 = mir_eval.melody.raw_pitch_accuracy(ref_v, ref_c,
                                                         est_v, est_c, cent_tolerance=50)
        raw_chroma_t25 = mir_eval.melody.raw_pitch_accuracy(ref_v, ref_c,
                                                         est_v, est_c, cent_tolerance=25)
        raw_chroma_t10 = mir_eval.melody.raw_pitch_accuracy(ref_v, ref_c,
                                                         est_v, est_c, cent_tolerance=10)

        # (precision_no_offset,
        #  recall_no_offset,
        #  f_measure_no_offset, avg_overlap_ratio) = mir_eval.transcription.precision_recall_f1_overlap(GT_time, GT_pitch,
        #                                                                                               estimate_time,
        #
        accrancy_item = [raw_pitch,raw_chroma_t50,raw_chroma_t25,raw_chroma_t10]


        # metris_tuple = (
        #     GT_time, GT_pitch, estimate_time, estimate_pitch)
        # dic = mir_eval.melody.evaluate(GT_time,
        #                                                  GT_pitch,
        #                                                  estimate_time,
        #                                                  estimate_pitch)

        precisionlist.append(accrancy_item)
        # recalllist.append(recall_no_offset)
        # F1scorelist.append(f_measure_no_offset)
        GT_pitch_list = []
        estimate_pitch_list = []
        # print("precision: " + str(precision_no_offset) + ", recall: " + str(recall_no_offset) + ", F1score: " + str(
        #     f_measure_no_offset) + "\n")
        #print(dic.items())
        print("estimate file: "+str(estimate_list[i])+" 's "+Method+" results are:")
        print("raw_chroma_accuracy is: "+str(raw_pitch))

        print("raw_pitch_accurancy with tolerance 50 is: "+str(raw_chroma_t50))
        print("raw_pitch_accurancy with tolerance 25 is: "+str(raw_chroma_t25))
        print("raw_pitch_accurancy with tolerance 10 is: "+str(raw_chroma_t10))


if __name__ == '__main__':
    estimate_csvpath = './resultpitch'
    GT_csvpath = './annotation_stems'
    method = 'BNLS'
    mypitch_eval(estimate_csvpath, GT_csvpath, method)
