import subprocess
import datetime
import os
import re
from tqdm import tqdm
import random

def extract_image(input_file, output_image):
    try:
        # Mendapatkan jumlah frame dalam video untuk memperkirakan progres ekstraksi gambar
        result = subprocess.run(['ffmpeg', '-i', input_file, '-frames:v', '1'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        frame_match = re.search(r'frame=\s*(\d+)', result.stdout)
        if frame_match:
            total_frames = int(frame_match.group(1))
        else:
            total_frames = 1
        
        # Perintah FFmpeg untuk mengekstrak gambar pertama dari video
        command = [
            'ffmpeg',
            '-i', input_file,
            '-ss', '00:00:01.000', # Ambil frame dari detik pertama
            '-vframes', '1', 
            output_image
        ]
        
        # Menjalankan perintah FFmpeg dengan progress bar
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
        # Mendapatkan durasi video untuk progress bar
        result = subprocess.run(['ffmpeg', '-i', input_file], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        duration_match = re.search(r'Duration: (\d+):(\d+):(\d+)\.(\d+)', result.stdout)
        if duration_match:
            hours, minutes, seconds, _ = map(int, duration_match.groups())
            total_duration = hours * 3600 + minutes * 60 + seconds
        else:
            total_duration = 0
        
        # Perintah FFmpeg untuk mengonversi MP4 ke MP3 dengan cover art
        command = [
            'ffmpeg',
            '-i', input_file,
            '-i', cover_image,
            '-map', '0:a', # Gunakan audio dari file input pertama
            '-map', '1', # Gunakan gambar dari file input kedua
            '-c:a', 'libmp3lame', # Encode audio ke MP3
            '-q:a', '0', # Kualitas audio terbaik
            '-id3v2_version', '3',
            '-metadata:s:v', 'title="Cover"',
            '-metadata:s:v', 'comment="Cover (front)"',
            output_file
        ]
        
        # Menjalankan perintah FFmpeg dengan progress bar
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

# Warna-warna yang akan digunakan untuk loading bar secara acak
bright_colors = ['blue'] # warna loading bar, bisa anda tambahkan warnanya lebih dari 1 agar setiap running berbeda warna

# Mengacak urutan warna
random.shuffle(bright_colors)

# Mendapatkan input file path dari pengguna
input_file = input("Masukkan path video (MP4): ")

# Membuat nama file output yang unik berdasarkan nama file input dan timestamp
file_base_name = os.path.splitext(os.path.basename(input_file))[0]
timestamp = datetime.datetime.now().strftime("%S")
cover_image = f"{file_base_name}_cover_{timestamp}.jpg"
output_file = f"{file_base_name}_{timestamp}.mp3"

# Ekstrak gambar dari video
extract_image(input_file, cover_image)

# Melakukan konversi MP4 ke MP3 dengan cover art
convert_mp4_to_mp3(input_file, output_file, cover_image)

# Hapus gambar cover setelah digunakan
os.remove(cover_image)
