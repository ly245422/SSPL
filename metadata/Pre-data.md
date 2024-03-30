# Data Preparation
## Chaotic World dataset
### Download the official annotations
Organize the SSL_ssl_format file in the SSPL/metadata folder in the following format.
[SSL_ssl_format.zip](https://drive.google.com/file/d/1nE_17zGhEx4aIKv_8WVltyUWydEO2-d6/view?usp=drive_link)
```
metadata
|
└───SSL_ssl_format
    |
    └───annotation
    |   |
    |   └───frame
    |   |   |   ADCCAWWD.csv
    |   |   |   ...
    |   |   |   ZXVHGAQL.csv
    |   |   |
    |   └───group
    |   |   |   ADCCAWWD.csv
    |   |   |   ...
    |   |   |   ZXVHGAQL.csv
    |   |   |   
    |   └───train_ssl.txt
    │   |
    |   └───test_ssl.txt
    │
    └───generating_ssl_dataset.py
    │
    └───read_frame_audio_then_save_hdf5.py
```

### Generate the ssl
Run the SSPL/metadata/generating_ssl_dataset.py file to generate the ssl<br>
Initialize the dataset root (metadata), annotation root, frame root, video root, and the type of produced dataset (train/test) in the generating_ssl_dataset.<br>
Run the generating_ssl_dataset.py file to generate the ssl folder structure as follows,
```
ssl
|
└───ssl_test_frames_320x180
|   |   ADCCAWWD_004157.png
|   |   ...
|   |   XLCJZXCK_002655.png
|   |   
└───ssl_test_wavs
|   |   ADCCAWWD_004157.wav
|   |   ...
|   |   XLCJZXCK_002655.wav
|   |   
└───ssl_train_frames_320x180
|   |   AIFFRWMA_000127.png
|   |   ...
|   |   ZXVHGAQL_002058.png
|   |   
└───ssl_train_wavs
|   |   AIFFRWMA_000127.wav
|   |   ...
|   |   ZXVHGAQL_002058.wav
|   |   
```

### Generate the h5 file
Run the SSPL/metadata/read_frame_audio_then_save_hdf5.py file to generate the h5 file.<br>
Move the read_frame_audio_then_save_hdf5.py file to the sspl_w_pcm folder.<br>
Initialize root_data = "/data/SSPL/metadata" and mode (train/test)<br>
The final format of the dataset is as follows
```
metadata
|
└───ChaoticWorld
    │
    └───all_unlabeled
    |   |   h5py_test_frames.h5
    |   |   h5py_test_audios.h5
    |   |   h5py_test_spects.h5
    |   |
    |
    └───labeled
        |
        └───Annotations
        |   |   ChaoticWorld_test.json
        |   |
        └───Data
        |   |   h5py_test_frames.h5
        |   |   h5py_test_audios.h5
        |   |   h5py_test_spects.h5
        |   |   ChaoticWorld_test.csv
        └───ChaoticWorld_test.csv
```
You can also use the preprocessed dataset and placed it in the SSPL/metadata.<br>
(https://drive.google.com/file/d/13NUg7ai0JCrq7iXoaDZD1ZL8bDphPVb4/view?usp=drive_link)
