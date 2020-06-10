import librosa
import librosa.display
import numpy as np
import matplotlib.pyplot as plt
from sklearn import preprocessing

"""
Inputs:
    audio_list: list of audio paths
    audio_length_ms: duration of the audio in milliseconds (ms)
    sampling_rate: sampling rate of the audio in Hz
    n_mels: number of frequencies in mel scale spectogram
    windows_ms: length in ms of the window
    stride_ms: length in ms of the stride
"""
def mel_spectrograms(audio_list, audio_length_ms, sampling_rate, n_mels, window_ms, stride_ms):
    spectrograms = {}
    stride_size = int(0.001 * sampling_rate * stride_ms)
    window_size = int(0.001 * sampling_rate * window_ms)
    max_size = int(0.001 * sampling_rate * audio_length_ms) 

    for audio_path in audio_list:
        try:
            audio, sampling_rate = librosa.load(audio_path, sr = None, mono = True, offset = 0.0, duration = None)
            S = librosa.feature.melspectrogram(audio[:max_size], sr=sampling_rate, n_fft=window_size, hop_length=stride_size, n_mels=n_mels)
            S_DB = librosa.power_to_db(S, ref=np.max)
            spectrograms[audio_path] = S_DB
        except:
            print(audio_path)
    
    return spectrograms


#Same as mel_spectrograms but sets the mean to 0 and variance to 1
def mel_spectrogramsNormalized(audio_list, audio_length_ms, sampling_rate, n_mels, window_ms, stride_ms):
    spectrograms = {}
    stride_size = int(0.001 * sampling_rate * stride_ms)
    window_size = int(0.001 * sampling_rate * window_ms)
    max_size = int(0.001 * sampling_rate * audio_length_ms)

    audio, sampling_rate = librosa.load(audio_list[0], sr = None, mono = True, offset = 0.0, duration = None)
    n_windows = librosa.feature.melspectrogram(audio[:max_size], sr=sampling_rate, n_fft=window_size, hop_length=stride_size, n_mels=n_mels).shape[1]
    spec_array = np.zeros((len(audio_list), n_mels, n_windows))

    index = 0
    for audio_path in audio_list:
        try:
            audio, sampling_rate = librosa.load(audio_path, sr = None, mono = True, offset = 0.0, duration = None)
            S = librosa.feature.melspectrogram(audio[:max_size], sr=sampling_rate, n_fft=window_size, hop_length=stride_size, n_mels=n_mels)
            S_DB = librosa.power_to_db(S, ref=np.max)
            spec_array[index] = S_DB
            index += 1
        except:
            print(audio_path)

    spec_array = spec_array.reshape((len(audio_list), n_mels * n_windows))
    scaler = preprocessing.StandardScaler().fit(spec_array)
    spec_array = scaler.transform(spec_array)
    spec_array = spec_array.reshape((len(audio_list), n_mels, n_windows))

    index = 0
    for audio_path in audio_list:
        spectrograms[audio_path] = spec_array[index]
        index += 1
    
    return spectrograms, scaler

def display_spectrogram(spectrogram, sampling_rate, stride_size):
    librosa.display.specshow(spectrogram, sr=sampling_rate, hop_length=stride_size, x_axis='time', y_axis='mel')
    plt.colorbar(format='%+2.0f dB')
    #plt.savefig('foo.png')


'''
stride_size = int(0.001 * 16000 * 10)
spectrograms = mel_spectrograms(["TesteAudio.wav"], 3000, 16000, 110, 20, 10)
print(spectrograms)
display_spectrogram(spectrograms["TesteAudio.wav"], 16000, stride_size)
'''
spectrograms = mel_spectrograms(["TesteAudio.wav", "TesteAudio1.wav"], 3000, 16000, 64, 20, 10)
print(spectrograms)
spectrograms = mel_spectrogramsNormalized(["TesteAudio.wav", "TesteAudio1.wav"], 3000, 16000, 64, 20, 10)
print(spectrograms)