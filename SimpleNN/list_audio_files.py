import sys
import os

root_dir = sys.argv[1]

audio_list = []

for root, dirs, files in os.walk(root_dir):
    for filename in files:
        if filename.split(".")[1] == "wav":
            audio_path_list = root.split("/")
            audio_path_list = root.split("/")
            length = len(audio_path_list) 
            audio_path = audio_path_list[length - 2] + "/" + audio_path_list[length - 1] + "/" + filename
            audio_list.append(audio_path)

print(len(audio_list))
print(audio_list[0:6])