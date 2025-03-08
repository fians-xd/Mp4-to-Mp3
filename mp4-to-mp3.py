import subprocess
import datetime
import os
import re
from tqdm import tqdm
import random

def extract_image(input_file, output_image):
    try:
        result = subprocess.run(['ffmpeg', '-i', input_file, '-frames:v', '1'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        frame_match = re.search(r'frame=\s*(\d+)', result.stdout)
        if frame_match:
            total_frames = int(frame_match.group(1))
        else:
            total_frames = 1
        
        command = [
            'ffmpeg',
            '-i', input_file,
            '-ss', '00:00:01.000',
            '-vframes', '1', 
            output_image
        ]
        
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        with tqdm(total=total_frames, unit='frame', desc='Extracting', ncols=100, bar_format="{l_bar}{bar:30}{r_bar}", colour=random.choice(bright_colors)) as pbar:
            for line in process.stdout:
                frame_match = re.search(r'frame=\s*(\d+)', line)
                if frame_match:
                    current_frame = int(frame_match.group(1))
                    pbar.update(current_frame - pbar.n)
        
        process.wait()
        if process.returncode != 0:
            print('Nasib jomblo yoo error: Image extraction failed.')
    except FileNotFoundError:
        print('Instal dulu goblog Ffmpeg nya.!!')

def convert_mp4_to_mp3(input_file, output_file, cover_image):
    try:
        result = subprocess.run(['ffmpeg', '-i', input_file], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        duration_match = re.search(r'Duration: (\d+):(\d+):(\d+)\.(\d+)', result.stdout)
        if duration_match:
            hours, minutes, seconds, _ = map(int, duration_match.groups())
            total_duration = hours * 3600 + minutes * 60 + seconds
        else:
            total_duration = 0
        
        command = [
            'ffmpeg',
            '-i', input_file,
            '-i', cover_image,
            '-map', '0:a',
            '-map', '1',
            '-c:a', 'libmp3lame',
            '-q:a', '0',
            '-id3v2_version', '3',
            '-metadata:s:v', 'title="Cover"',
            '-metadata:s:v', 'comment="Cover (front)"',
            output_file
        ]
        
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        with tqdm(total=total_duration, unit='s', desc='Converting', ncols=100, bar_format="{l_bar}{bar:30}{r_bar}", colour=random.choice(bright_colors)) as pbar:
            for line in process.stdout:
                time_match = re.search(r'time=(\d+):(\d+):(\d+)\.(\d+)', line)
                if time_match:
                    hours, minutes, seconds, _ = map(int, time_match.groups())
                    elapsed_time = hours * 3600 + minutes * 60 + seconds
                    pbar.update(elapsed_time - pbar.n)
        
        process.wait()
        if process.returncode == 0:
            print(f'\nDadi anjir:=> {output_file}\n')
        else:
            print('Nasib jomblo yoo error: Conversion failed.')
    except FileNotFoundError:
        print('Instal dulu goblog Ffmpeg nya.!!')

bright_colors = ['blue']

random.shuffle(bright_colors)

input_file = input("Masukkan path video (MP4): ")

file_base_name = os.path.splitext(os.path.basename(input_file))[0]
timestamp = datetime.datetime.now().strftime("%S")
cover_image = f"{file_base_name}_cover_{timestamp}.jpg"
output_file = f"{file_base_name}_{timestamp}.mp3"

extract_image(input_file, cover_image)

convert_mp4_to_mp3(input_file, output_file, cover_image)

os.remove(cover_image)
