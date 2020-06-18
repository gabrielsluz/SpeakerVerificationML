import os
os.environ['KMP_DUPLICATE_LIB_OK']='True'

from resemblyzer import VoiceEncoder, preprocess_wav
from pathlib import Path
import numpy as np

test_list_audios_x = []
test_list_y = []
with open("../voxceleb1/veri_test.txt") as test_labels_file:
    for line in test_labels_file:
        splitted = line.split()
        test_list_y.append(splitted[0])
        test_list_audios_x.append([splitted[1],splitted[2]])

sampling_rate = 16000
max_index = sampling_rate*5

similarity_results = {'1':[], '0':[]}

out_put = open("resemblyser_sim_test.txt", "w")

encoder = VoiceEncoder()
for i in range(len(test_list_audios_x)):
    wav1 = preprocess_wav(Path("../voxceleb1/test/" + test_list_audios_x[i][0]))
    wav2 = preprocess_wav(Path("../voxceleb1/test/" + test_list_audios_x[i][1]))

    embed1 =  encoder.embed_utterance(wav1[:max_index])
    embed2 = encoder.embed_utterance(wav2[:max_index])

    similarity_results[test_list_y[i]].append(embed1 @ embed2)
    out_put.write(str(test_list_y[i]) + " " + str(embed1 @ embed2) + "\n") 
    if i % 1000 == 0:
        print(i)

#print(similarity_results)



os.environ['KMP_DUPLICATE_LIB_OK']='False'