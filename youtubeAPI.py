from xml.sax.saxutils import unescape
from pytube import Playlist, exceptions
import xml.etree.ElementTree as ElementTree
import math
import time
import os

def float_to_srt_time_format(d: float) -> str:

        fraction, whole = math.modf(d/1000)
        time_fmt = time.strftime("%H:%M:%S,", time.gmtime(whole))
        ms = f"{fraction:.3f}".replace("0.", "")
        return time_fmt + ms

def xml_to_srt(xml_captions: str) -> str:
    segments = []
    root = ElementTree.fromstring(xml_captions)
    count_line = 0
    for i, child in enumerate(list(root.findall('body/p'))):
        
            text = ''.join(child.itertext()).strip()
            if not text:
                continue
            count_line += 1
            caption = unescape(text.replace("\n", " ").replace("  ", " "),)
            try:
                duration = float(child.attrib["d"])
            except KeyError:
                duration = 0.0
            start = float(child.attrib["t"])
            end = start + duration
            try:
                end2 = float(root.findall('body/p')[i+2].attrib['t'])
            except:
                end2 = float(root.findall('body/p')[i].attrib['t']) + duration
            sequence_number = i + 1  # convert from 0-indexed to 1.
            line = "{seq}\n{start} --> {end}\n{text}\n".format(
                seq=count_line,
                start=float_to_srt_time_format(start),
                end=float_to_srt_time_format(end2),
                text=caption,
            )
            segments.append(line)
    return "\n".join(segments).strip()

max_videos_to_download = 10
videos_downloaded = 0

playlist = Playlist("https://www.youtube.com/playlist?list=PLI1yx5Z0Lrv77D_g1tvF9u3FVqnrNbCRL")

if not os.path.exists('./data/videos'):
    os.makedirs('./data/videos')

if not os.path.exists('./data/captions'):
    os.makedirs('./data/captions')

for video in playlist.videos:
    if videos_downloaded >= max_videos_to_download:
        break  # Stop downloading more videos once you've reached the limit
    try:
        title = f"V{videos_downloaded}"
        len(video.streams)
        if not video.captions:
            print(f"No captions available for video: {video.title}")
            continue
        video.streams.get_highest_resolution().download(output_path='./data/videos', filename_prefix=title)
        # print(video)
        captions = xml_to_srt(video.captions['a.en'].xml_captions)
        # print(captions)
        with open(f"./data/captions/{title}.srt", "w", encoding="utf-8") as file_handle:
             file_handle.write(captions)
        videos_downloaded += 1
    except exceptions.AgeRestrictedError as e:
        continue