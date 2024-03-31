## Extract frames using ffmpeg and parallel
import subprocess

dir_video_new_save_root = r"/data/wenjj/ChaoticWorld/videos_320_180"


print('Extracting videos')

cmd = '''
num_threads=20
src_path=''' + dir_video_new_save_root + '''
dst_path=''' + dir_video_new_save_root.replace('videos', 'frames') + '''

mkdir $dst_path

parallel -j $num_threads "mkdir ${dst_path}/{};ffmpeg -i ${src_path}/{}.mp4 -start_number 1 ${dst_path}/{}/'{}_%06d.png' -loglevel error" ::: `ls ${src_path} |cut -d '.' -f1`
'''
subprocess.check_output(cmd, shell=True) # frames are 1-indexed

print('Extracting videos completed')