# Data Preparation
## Chaotic World dataset
### Download the official annotations
Organize the SSL_ssl_format file in the SSPL/metadata folder in the following format.
[SSL_ssl_format.zip](https://drive.google.com/file/d/1nE_17zGhEx4aIKv_8WVltyUWydEO2-d6/view?usp=drive_link)<br>
'''
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
'''
### Generate the ssl
Run the SSPL/metadata/generating_ssl_dataset.py file to generate the ssl<br>
Initialize the dataset root (metadata), annotation root, frame root, video root, and the type of produced dataset (train/test) in the generating_ssl_dataset.<br>
Run the generating_ssl_dataset.py file to generate the ssl folder structure as follows,<br>
ssl<br>
|<br>
└───ssl_test_frames_320x180<br>
|   |   ADCCAWWD_004157.png<br>
|   |   ...<br>
|   |   XLCJZXCK_002655.png<br>
|   |   <br>
└───ssl_test_wavs<br>
|   |   ADCCAWWD_004157.wav<br>
|   |   ...<br>
|   |   XLCJZXCK_002655.wav<br>
|   |   <br>
└───ssl_train_frames_320x180<br>
|   |   AIFFRWMA_000127.png<br>
|   |   ...<br>
|   |   ZXVHGAQL_002058.png<br>
|   |   <br>
└───ssl_train_wavs<br>
|   |   AIFFRWMA_000127.wav<br>
|   |   ...<br>
|   |   ZXVHGAQL_002058.wav<br>
|   |   <br>

### Generate the h5 file<br>
Run the SSPL/metadata/read_frame_audio_then_save_hdf5.py file to generate the h5 file<br>
Move the read_frame_audio_then_save_hdf5.py file to the sspl_w_pcm folder.<br>
Initialize root_data = "/data/SSPL/metadata" and mode(train/test)<br>
The final format of the dataset is as follows<br>
metadata<br>
|<br>
└───ChaoticWorld<br>
    │<br>
    └───all_unlabeled<br>
    |   |   h5py_test_frames.h5<br>
    |   |   h5py_test_audios.h5<br>
    |   |   h5py_test_spects.h5<br>
    |   |<br>
    |<br>
    └───labeled<br>
        |<br>
        └───Annotations<br>
        |   |   ChaoticWorld_test.json<br>
        |   |<br>
        └───Data<br>
        |   |   h5py_test_frames.h5<br>
        |   |   h5py_test_audios.h5<br>
        |   |   h5py_test_spects.h5<br>
        |   |   ChaoticWorld_test.csv<br>
        └───ChaoticWorld_test.csv<br>

You can also use the preprocessed dataset and placed it in the SSPL/metadata.<br>
