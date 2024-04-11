import mir_eval

from Utils.ReadOnsetCSV import readonset

if __name__ == '__main__':
    choice = 1  #1是SpecFlux 2是SuperFlux， 3是log energy

    if choice == 1:
        onset_env, csv_list = readonset('./resultonset/Specflux')
    elif choice == 2:
        onset_env, csv_list = readonset('./resultonset/superflux')
    else:
        onset_env, csv_list = readonset('./resultonset/superflux')

    onset_GT, _ = readonset('./annotation_onset')
    for i in range(len(onset_GT)):
        F, P, R = mir_eval.onset.f_measure(onset_GT[i], onset_env[i])
        print(csv_list[i]+"'s precision: " + str(P) + ", recall: " + str(R) + ", F1score: " + str(F) + "\n")