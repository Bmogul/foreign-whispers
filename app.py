import os
import subprocess

if __name__ == '__main__':
    videos_path = os.path.join('data', 'videos')
    captions_path = os.path.join('data', 'captions')

    videos = os.listdir(videos_path)
    captions = os.listdir(captions_path)

    if len(videos) != 10 and len(captions) != 10:
        subprocess.run(['python3', 'youtubeAPI.py'])
