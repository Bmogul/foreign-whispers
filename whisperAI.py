import whisper

def generate_transcript(mp4_file_path):
    print('mp4_file_path')
    model = whisper.load_model("base")
    result = model.transcribe(mp4_file_path)
    print('result')
    return generate_srt_from_segments(result['segments'])

def generate_srt_from_segments(segments):
    srt_lines = []
    sequence_number = 1
    for segment in segments:
        start_time = int(segment['start'] * 1000)
        end_time = int(segment['end'] * 1000)
        text = segment['text']
        
        srt_line = f"{sequence_number}\n{milliseconds_to_srt_time_format(start_time)} --> {milliseconds_to_srt_time_format(end_time)}\n{text}\n"
        srt_lines.append(srt_line)
        
        sequence_number += 1

    return "\n".join(srt_lines)

def milliseconds_to_srt_time_format(milliseconds):
    seconds, milliseconds = divmod(milliseconds, 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d},{milliseconds:03d}"

# Example usage:
# mp4_file = "./data/videos/V0Vice President Kamala Harris The 2023 60 Minutes Interview.mp4"
# transcript = generate_transcript(mp4_file)
# print(transcript)
