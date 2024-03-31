## Specify save file path
dir_dataset_root = 'Path to metadata' ## e.g. SSPL/metadata/
dir_annotation_root = dir_dataset_root  + '/SSL_ssl_format/annotation/group'
dir_frame_root = '/ChaoticWorld/frames_320_180' ## Specify your frame root
dir_video_root = '/ChaoticWorld/videos_320_180' ## Specify your video root
mode = "test" ## Specify your mode

## Import libraries
import pandas as pd
from glob import glob
import os
import torchaudio
import shutil
import csv
import json
import numpy as np

## Create directories
if mode == "train":
    dir_ssl_frames = os.path.join(dir_dataset_root, 'ssl/ssl_train_frames_320x180')
    dir_ssl_wavs = os.path.join(dir_dataset_root, 'ssl/ssl_train_wavs')
    dir_csv = os.path.join(dir_dataset_root, 'ssl/train_list.csv')
elif mode == "test":
    dir_ssl_frames = os.path.join(dir_dataset_root, 'ssl/ssl_test_frames_320x180')
    dir_ssl_wavs = os.path.join(dir_dataset_root, 'ssl/ssl_test_wavs')
    dir_csv = os.path.join(dir_dataset_root, 'ssl/test_list.csv')
    json_file_path = os.path.join(dir_dataset_root, "ChaoticWorld/labeled/Annotations/ChaoticWorld_test.json")

if os.path.exists(dir_csv):
    os.remove(dir_csv)
os.makedirs(dir_ssl_frames, exist_ok=True)
os.makedirs(dir_ssl_wavs, exist_ok=True)

## Load annotations
train_txt = '/data/liujinfu/ChaoticWorld/annotations/SSL_ssl_format/train_ssl.txt'
test_txt = '/data/liujinfu/ChaoticWorld/annotations/SSL_ssl_format/test_ssl.txt'

train_txt = open(train_txt, 'r')
test_txt = open(test_txt, 'r')

ssl_train = [item.strip() for item in train_txt]
ssl_test = [item.strip() for item in test_txt]
if mode == "train":
    ssl_list = ssl_train
elif mode == "test":
    ssl_list = ssl_test

def write_frame_name_to_csv(frame_name, csv_file_path):
    if not os.path.exists(dir_csv):
        with open(dir_csv, 'w'): 
            pass  
   
    with open(csv_file_path, 'r') as csvfile:
        existing_frames = csvfile.readlines()
        if frame_name.split('.')[0] + '\n' in existing_frames:
            print(f"Frame {frame_name} already exists in the CSV file. Skipping...")
            return
   
    with open(csv_file_path, "a") as csvfile:
        csvfile.write(frame_name.split('.')[0] + '\n')

def extract_sound():
    
    frames_info = []
    for item in ssl_list:
        ## Read annotations
        annotation = pd.read_csv(dir_annotation_root + '/' + item + '.csv')
        
        print('Process:', item)
        ## Load video and audio
        dir_video = os.path.join(dir_video_root, item + '.mp4')
        waveform, sample_rate = torchaudio.load(dir_video)
        waveform_len = waveform.shape[1]
        
        
        for row, data in annotation.iterrows():
            frame_name = '{}_{:0>6d}.png'.format(item, int(data['start_fid']))
            write_frame_name_to_csv(frame_name, dir_csv)
            dir_frame_src = os.path.join(dir_frame_root, item, frame_name)
            dir_wav = os.path.join(dir_ssl_wavs, frame_name[:-4] + '.wav')
            
            ## Load bbox for corresponding timing
            time_current = data['start_time']
            bbox = eval(data['bbox'])[0]
            
            frame_offset = int((time_current - 1.5) * sample_rate)
            num_frames = int(3 * sample_rate)

            frames_info.append({
            "file": f"{item}_{int(data['start_fid']):06d}",
            "class": data['ssl'],
            "bbox": bbox  
            })
            
            ## Extract waveform
            waveform_temp = waveform[:, frame_offset:frame_offset + num_frames]

            if time_current >= 1.5 and frame_offset + num_frames <= waveform_len:
                if waveform_temp.shape[1] == num_frames:
                    pass
                else:
                    print('index {} len: {}'.format(row, waveform_temp.shape[1]))
                
                ## Save audio
                shutil.copy(dir_frame_src, dir_ssl_frames)
                torchaudio.save(dir_wav, 
                                waveform[:, frame_offset:frame_offset + num_frames], 
                                sample_rate, 
                                format="wav")
    if mode == "test":
        ## Write frame information list to JSON file
        json_dir = os.path.dirname(json_file_path)
        os.makedirs(json_dir, exist_ok=True)
        if not os.path.isfile(json_file_path):
            open(json_file_path, 'a').close()  
        with open(json_file_path, 'w') as json_file:
            json.dump(frames_info, json_file, indent=4)


extract_sound()

def extract_images():
    images = sorted(os.listdir(dir_ssl_frames))
    value_train = []
    value_test = []

    for item in images:
        video = item.split('_')[0]
        item = item.split('.')[0]

        if video in ssl_train:
            value_train.append(item)
        else:
            value_test.append(item)
    
extract_images()

