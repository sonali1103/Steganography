import base64
import shutil
from flask import Blueprint, redirect, render_template, url_for
import os

home = Blueprint('home', __name__)

 # directory which has all embedded files
EMBEDED_FOLDER = './Steganography/static/embededfiles/'

@home.route('/')
def homeview():
    # Get list of files in the folder
    files = os.listdir(EMBEDED_FOLDER)

    # Filter images, videos, and audios
    image_files = [EMBEDED_FOLDER + file for file in files if file.lower().endswith(('.png','.heic', '.jpg', '.jpeg', '.gif'))]
    image_binary = []
    
    # to display image file on UI
    for img_file in image_files:
        with open(img_file, 'rb') as file:
            file_content = file.read()
        encoded_content = base64.b64encode(file_content).decode('utf-8')
        image_binary.append(encoded_content)
    
    
    video_files = [EMBEDED_FOLDER + file for file in files if file.lower().endswith(('.mp4', '.avi', '.mkv'))]    
    video_binary = []
    for video_file in video_files:
        with open(video_file, 'rb') as file:
            v_file_content = file.read()
        encoded_video = base64.b64encode(v_file_content).decode('utf-8')
        video_binary.append(encoded_video)
    
     
    audio_files = [EMBEDED_FOLDER + file for file in files if file.lower().endswith(('.mp3', '.wav', '.ogg'))]   
    audio_binary = []
    for audio_file in audio_files:
        with open(audio_file, 'rb') as file:
            v_file_content = file.read()
        encoded_audio = base64.b64encode(v_file_content).decode('utf-8')
        audio_binary.append(encoded_audio)       

    return render_template('home.html', image_files=image_binary, video_files=video_binary, audio_files=audio_binary)


@home.route('/delete', methods=['POST'])
def delete_files():
    shutil.rmtree(EMBEDED_FOLDER)
    os.makedirs(EMBEDED_FOLDER)
    return redirect(url_for('home.homeview'))  