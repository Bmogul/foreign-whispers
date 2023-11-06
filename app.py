import os
import subprocess
from whisperAI import generate_transcript


print('hello')
videos_path = os.path.join('data', 'videos')
transcripts_path = os.path.join('data', 'transcripts')

os.makedirs(transcripts_path, exist_ok=True)

videos = os.listdir(videos_path)

if len(videos) != 10:
    subprocess.run(['python3', 'youtubeAPI.py'])


for video_file in videos:
    if video_file.endswith(".mp4"):
        video_path = os.path.join(videos_path, video_file)
        video_name = os.path.splitext(video_file)[0]
        transcript = generate_transcript(video_path)

        # Save the transcript as an SRT file
        transcript_file = os.path.join(transcripts_path, f"{video_name}.srt")
        with open(transcript_file, "w", encoding="utf-8") as file_handle:
            file_handle.write(transcript)

print("Transcripts generated and saved to the transcripts folder.")
