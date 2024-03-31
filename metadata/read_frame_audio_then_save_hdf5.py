"""
Read frame and audio data using given video ids, and then save as hdf5, respectively.
"""


import os
import cv2
import h5py
import glob
import csv
import pandas as pd
import numpy as np
import librosa
from pydub import AudioSegment
from utils import normalize_audio
from models.torchvggish.torchvggish import vggish_input


# -----------------------------------------------
# raw training data paths and hyper-parameters
# -----------------------------------------------
root_data = "Path to metadata" ## e.g., /SSPL/metadata

mode = "test" ## train/test
if mode == "train":
    path_video_all = root_data + '/ssl/train_list.csv'
    csv_path = root_data + '/ChaoticWorld/all_unlabeled'
elif mode == "test":
    path_video_all = root_data + '/ssl/test_list.csv'
    csv_path = root_data + '/ChaoticWorld/labeled'
os.makedirs(csv_path, exist_ok=True)

video_train_frames_all_paths = pd.read_csv(path_video_all, header=None, sep=',')  
sample_size = video_train_frames_all_paths.shape[0]   
audio_sample_rate = 16000
audio_duration = 3
audio_length = audio_sample_rate * audio_duration


# -----------------------------------------------
# extract paths and data
# -----------------------------------------------
sample_frames = np.zeros((sample_size, 256, 256, 3), dtype='float32')
sample_audios = np.zeros((sample_size, audio_length), dtype='float32')
sample_spects = np.zeros((sample_size, audio_duration, 96, 64), dtype='float32')   # (sample_size, audio_duration, 96, 64) for VGGish
cnt_saved_data = 0

if mode == "train":
    csv_path = csv_path + "/ChaoticWorld_train.csv"
elif mode == "test":
    csv_path = csv_path + "/ChaoticWorld_test.csv"
if os.path.isfile(csv_path):
    os.remove(csv_path)

for i in range(sample_size):

    path = video_train_frames_all_paths.iat[i, 0]   ## path: e.g., 'ADCCAWWD_004157'
    print(f"Processing {path}")
    
    # frame (jpg)
    if mode == "train":
        frame_path = root_data + '/ssl/ssl_train_frames_320x180/' + path + '.png' ## e.g., /SSPL/metadata/ssl/ssl_test_frames_320x180/ADCCAWWD_004157.png
    elif mode == "test":
        frame_path = root_data + '/ssl/ssl_test_frames_320x180/' + path + '.png'
    if not os.path.exists(frame_path):
        print('Path does not exist, or there is no frame: ', frame_path)
        continue

    # audio (mp3)
    if mode == "train":
        audio_path = root_data + '/ssl/ssl_train_wavs/' + path + '.wav' ## e.g., /SSPL/metadata/ssl/ssl_test_wavs/ADCCAWWD_004157.wav
    elif mode == "test":
        audio_path = root_data + '/ssl/ssl_test_wavs/' + path + '.wav'
    if not os.path.exists(audio_path):   # skip empty folder
        print('Path does not exist, or there is no audio: ', audio_path)
        continue

    # record one frame image for one video
    try:
        frame = cv2.imread(frame_path)
    except:
        print("Error png", frame_path)
        continue
    frame = cv2.resize(frame, (256, 256), interpolation=cv2.INTER_CUBIC)
    sample_frames[cnt_saved_data, :, :, :] = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # record 3s sound spectrogram for one video
    # convert mp3 to wav
    try:
        sound = AudioSegment.from_wav(audio_path)
        with open(csv_path, 'a') as csv_file:
            csv_file.write(path + '\n')
    except:
        print("Error wav", audio_path)
        continue
    sound.export(audio_path, format='wav')
    # read wav with given duration
    audio_np, rate = librosa.load(audio_path, sr=audio_sample_rate, mono=True)
    curr_audio_length = audio_np.shape[0]
    if curr_audio_length < audio_length:
        n = int(audio_length / curr_audio_length) + 1
        audio_np = np.tile(audio_np, n)
        curr_audio_length = audio_np.shape[0]
    start_sample = int(curr_audio_length / 2) - int(audio_length / 2)
    sample_audios[cnt_saved_data, :] = normalize_audio(audio_np[start_sample:start_sample + audio_length])
    # log-mel spectrogram
    sample_spects[cnt_saved_data, :, :, :] = vggish_input.waveform_to_examples(sample_audios[cnt_saved_data, :],
                                                                               sample_rate=audio_sample_rate,
                                                                               return_tensor=False)

    cnt_saved_data += 1
    if cnt_saved_data % 1000 == 0:
        print('{} sample data have been extracted.'.format(cnt_saved_data))
    if cnt_saved_data == sample_size:
        print('All {} sample data have been extracted.'.format(cnt_saved_data))
        break
# -----------------------------------------------
# Remove the trailing zero rows
# -----------------------------------------------
last_nonzero_index = np.where(np.any(sample_frames != 0, axis=(1, 2, 3)))[0][-1]
sample_frames = sample_frames[:last_nonzero_index + 1]
sample_audios = sample_audios[:last_nonzero_index + 1]
sample_spects = sample_spects[:last_nonzero_index + 1]

# -----------------------------------------------
# save paths and data
# -----------------------------------------------
if mode == "train":
    h5py_path_frames = root_data + '/ChaoticWorld/all_unlabeled/h5py_train_frames.h5'
    h5py_path_audios = root_data + '/ChaoticWorld/all_unlabeled/h5py_train_audios.h5'
    h5py_path_spects = root_data + '/ChaoticWorld/all_unlabeled/h5py_train_spects.h5'
    # frame
    with h5py.File(h5py_path_frames, 'w') as hf:
        hf.create_dataset('train_frames', data=sample_frames)    
    # audio
    with h5py.File(h5py_path_audios, 'w') as hf:
        hf.create_dataset('train_audios', data=sample_audios)
    # spectrogram
    with h5py.File(h5py_path_spects, 'w') as hf:
        hf.create_dataset('train_spects', data=sample_spects)
elif mode == "test":
    os.makedirs(root_data + '/ChaoticWorld/labeled/Data/', exist_ok=True)
    h5py_path_frames = root_data + '/ChaoticWorld/labeled/Data/h5py_test_frames.h5'
    h5py_path_audios = root_data + '/ChaoticWorld/labeled/Data/h5py_test_audios.h5'
    h5py_path_spects = root_data + '/ChaoticWorld/labeled/Data/h5py_test_spects.h5'
    # frame
    with h5py.File(h5py_path_frames, 'w') as hf:
        hf.create_dataset('test_frames', data=sample_frames)    
    # audio
    with h5py.File(h5py_path_audios, 'w') as hf:
        hf.create_dataset('test_audios', data=sample_audios)
    # spectrogram
    with h5py.File(h5py_path_spects, 'w') as hf:
        hf.create_dataset('test_spects', data=sample_spects)

