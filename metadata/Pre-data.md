# Data Preparation
## Chaotic World dataset
### Frame the video
You need to download the original video yourself.<br>
Specify your own dir_video_org and dir_video_new_save_root in the SSPL/metadata/extract_frames.py.<br>
To generate all frames 320x180, simply run:
```
python extract_frames.py
```
the frames_320_180 folder structure as follows,
```
frames_320_180
|
└───ADCCAWWD
|   |   ADCCAWWD_000001.png
|   |   ...
|   |   ADCCAWWD_005103.png
|   |   
└───AGRUUMUL
|   |   AGRUUMUL_000001.png
|   |   ...
|   |   AGRUUMUL_001220.png
|   |   
|   |   ...
|   |   ...
|   |   ...
|   |   
└───AGRUUMUL
|   |   ZYLIXFXD_000001.png
|   |   ...
|   |   ZYLIXFXD_002499.png
```
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
Specify the dataset root (metadata), frame root, video root, and the type of produced dataset (train/test) in the SSPL/metadata/generating_ssl_dataset.py.<br>
To generate the ssl folder, simply run:
```
python generating_ssl_dataset.py
```
the ssl folder structure as follows,
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
Move the SSPL/metadata/read_frame_audio_then_save_hdf5.py file to the SSPL/sspl_w_pcm folder.<br>
Specify root_data and mode (train/test)<br>
To generate the h5 files, simply run:
```
python read_frame_audio_then_save_hdf5.py
```
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
[ChaoticWorld.zip](https://drive.google.com/file/d/12cDq-_KjnAsCJZXJF5DZb72zVY4hi0nW/view?usp=drive_link)
