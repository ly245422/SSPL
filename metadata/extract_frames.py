## Extract frames using ffmpeg and parallel
import subprocess

dir_video_org = r"/ChaoticWorld/videos" # Specify your own original video path
dir_video_new_save_root = r"/ChaoticWorld/frames_320_180" # Specify your own frame path

print('Extracting videos')

cmd = '''
num_threads=20
src_path=''' + dir_video_org + '''
dst_path=''' + dir_video_new_save_root + '''

mkdir $dst_path

parallel -j $num_threads "mkdir ${dst_path}/{};ffmpeg -i ${src_path}/{}.mp4 -vf scale=320:180 -start_number 1 ${dst_path}/{}/'{}_%06d.png' -loglevel error" ::: `ls ${src_path} | cut -d '.' -f1`
'''

subprocess.check_output(cmd, shell=True) # frames are 1-indexed

print('Extracting videos completed')
