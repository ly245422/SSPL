# Self-Supervised Predictive Learning (SSPL)
We use this model in Track #4 Sound Source Localization of [2024 ICME Grand Challenge] Multi-Modal Video Reasoning and Analyzing Competition (MMVRAC). Our results are cIoU 47.70 AUC 44.14 (sspl_w_pcm) and cIoU 41.12 AUC 42.60 (sspl_wo_pcm). 

## How to reproduce
### Requirements
We have tested the code on the following environment:<br>
```
Python  3.8.0 | torch  1.10.0+cu113 | torchaudio  0.10.0+cu113 | torchvision  0.11.1+cu113 | CUDA  11.4
```
### Parameter setting
```
[sspl_w_pcm]: epoch: 350 | devices: RTX 3070 * 1 | batch_size_per_gpu: 64 | img_size: 224
[sspl_wo_pcm]: epoch: 40 | devices: RTX 3070 * 1 | batch_size_per_gpu: 128 | img_size: 224
```
### Download & pre-process videos
Please refer to the SSPL/metadata/Pre-data.md file.

### Training
We utilize [VGG16] and [VGGish] as backbones 
to extract visual and audio features, respectively. Before training, you need to place pre-trained VGGish weights, 
i.e., [vggish-10086976.pth](https://github.com/harritaylor/torchvggish/releases/download/v0.1/vggish-10086976.pth), 
in ```models/torchvggish/torchvggish/vggish_pretrained/```. <br>To train SSPL on SoundNet-Flickr10k with default setting, simply run:
```
python main.py
```
Remember to specify your own MASTER_ADDR and MASTER_PORT in main.py and path to metadata in arguments_train.py

**Note:** We found that learning rates have vital influence on SSPL's performance. So we suggest that using the early stopping strategy 
to select hyper-parameters and avoid overfitting.

### Test
After training, ```frame_best.pth```, ```sound_best.pth```, ```ssl_head_best.pth``` (and ```pcm_best.pth``` for SSPL (w/ PCM)) 
can be obtained. <br>To test SSPL on Chaotic World 
with default setting, simply run:
```
python test.py
```
Remember to specify your own MASTER_ADDR and MASTER_PORT in test.py and path to metadata in arguments_test.py

### Weight
You can download our checkpoint and best weights.<br>
[sspl_w_pcm_ChaoticWorld.zip](https://drive.google.com/file/d/1XeTe41_5e-_nTR7vSLDr9a51ZsfBFDKP/view?usp=drive_link)<br>
[sspl_wo_pcm_ChaoticWorld.zip](https://drive.google.com/file/d/1_-V1vhqo92fAvmIyGyizkDfWggutwRyy/view?usp=drive_link) 


