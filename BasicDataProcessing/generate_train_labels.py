import os
import random

#Lists all the wav files in the format of the voxceleb test dataset.
def list_audios(root_dir):
    audio_list = []
    for root, dirs, files in os.walk(root_dir):
        for filename in files:
            if filename.split(".")[1] == "wav":
                audio_path_list = root.split("/")
                length = len(audio_path_list) 
                audio_path = audio_path_list[length - 2] + "/" + audio_path_list[length - 1] + "/" + filename
                audio_list.append(audio_path)

    return audio_list

#Get the speaker id from a simple path : speaker_id/sub_dir/audio.wav
def get_speaker_id(audio_path):
    return audio_path.split("/")[0]

#It returns a list(speakers) of lists(audios)
def list_speakers_audios(audio_list):
    audio_list.sort()
    speakers = []
    speaker_now = get_speaker_id(audio_list[0])
    speaker_audios = []

    for audio in audio_list:
        if(speaker_now != get_speaker_id(audio)):
            speakers.append(speaker_audios)
            speaker_audios = []
            speaker_now = get_speaker_id(audio)
        speaker_audios.append(audio)
    
    speakers.append(speaker_audios)
    return speakers

#Receives a list(speakers) of lists(audios)
#Returns list of labeled (diff speakers) pairs, represented in lists (label, audio1, audio2)
def make_diff_speakers_pairs(speakers):
    i = 0
    j = 0
    k = 0
    diff_pairs = []
    for i in range(0, len(speakers)):
        k = 0
        for j in range(i+1, len(speakers)):
            diff_pairs.append(["0", speakers[i][k], speakers[j][random.randint(0, len(speakers[j])-1)]])
            k += 1
            if k >= len(speakers[i]):
                k = 0
            diff_pairs.append(["0", speakers[i][k], speakers[j][random.randint(0, len(speakers[j])-1)]])
            k += 1
            if k >= len(speakers[i]):
                k = 0

    return diff_pairs

#Receives a list(speakers) of lists(audios)
#Returns list of labeled (same speakers) pairs, represented in lists (label, audio1, audio2)
def make_same_speakers_pairs(speakers, num_pairs):
    same_pairs = []
    for i in range(0, len(speakers)):
        for j in range(0, num_pairs // len(speakers)):
            same_pairs.append(["1", speakers[i][random.randint(0, len(speakers[i])-1)], speakers[i][random.randint(0, len(speakers[i])-1)]])

    return same_pairs


"""
audio_list = list_audios("../../voxceleb1/dev/")
speakers = list_speakers_audios(audio_list)
diff_pairs = make_diff_speakers_pairs(speakers)
same_pairs = make_same_speakers_pairs(speakers)

#random.shuffle(diff_pairs)
#random.shuffle(same_pairs)

dataset = []
for i in range(len(diff_pairs)):
    dataset.append(diff_pairs[i])
    dataset.append(same_pairs[i])

random.shuffle(dataset)

#print(len(dataset))
for i in dataset:
    print(i[0], i[1], i[2])


"""