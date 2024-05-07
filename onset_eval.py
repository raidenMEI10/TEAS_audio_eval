import mir_eval
import numpy as np

from Utils.ReadOnsetCSV import readonset, getonsetname

if __name__ == '__main__':
    choice = "ourmethod"  #1是SpecFlux 2是SuperFlux， 3是log energy
    onsetlist = getonsetname("./resultonset/"+choice)
    GTlist = getonsetname("./annotation_onset/")
    for i in range(len(GTlist)):
        onset_env, offset_env = readonset('./resultonset/'+choice+"/"+onsetlist[i])
        onset_gt, offset_gt = readonset('./annotation_onset/'+GTlist[i])
        onset_env = np.delete(np.array([float(x) for x in onset_env]),-1)
        offset_env = np.delete(np.array([float(x) for x in offset_env]),-1)
        onset_gt = np.delete(np.array([float(x) for x in onset_gt]),-1)
        offset_gt = np.delete(np.array([float(x) for x in offset_gt]),-1)

        # interval_eval = np.dstack((onset_env, offset_env)).squeeze()
        # interval_gt = np.dstack((onset_env,offset_env)).squeeze()
        # print(interval_eval)
        # matchings = mir_eval.transcription.match_note_offsets(interval_gt, interval_eval)
        # avg_overlap_ratio = mir_eval.transcription.average_overlap_ratio(interval_gt, interval_eval, matchings)

        F, P, R = mir_eval.onset.f_measure(onset_gt, onset_env)
        print(GTlist[i]+"'s precision: " + str(P) + ", recall: " + str(R) + ", F1score: " + str(F) + "\n")
        #print("avg_overlap_ratio "+ avg_overlap_ratio)