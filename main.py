# main.py

import subprocess
import sys
import get_pip
import re


def install(package):
    subprocess.call([sys.executable, "-m", "pip", "install", package])

try:
    from pytube import YouTube
    from pytube import Playlist
except:
    print('Import Error: PyTube3 not installed')
    print('Attempting to install PyTube3 using pip')
    try:
        import pip
        install('pytube3')
        print('PyTube3 has been installed')
    except:
        print('Import Error: pip not installed')
        print('Attempting to install pip')
        get_pip.main()
        print('Pip has been installed')
        try:
            print('Attempting to install PyTube3 using pip')
            import pip
            install('pytube3')
            print('PyTube3 has been installed')
        except:
            print('PyTube3 could not be installed')

from pytube import YouTube
from pytube import Playlist
import pytube


def convert_time(seconds: int):
    '''
    Returns a string of the time in the most optimal units
    Form: hours, minutes, seconds
    '''
    if seconds < 60:
        return str(seconds) + ' seconds'
    elif seconds < 3600:
        return str(seconds // 60) + ' minutes ' + str(seconds % 60) + ' seconds'
    else:
        return str(seconds // 3600) + ' hours ' + str(seconds // 60) + ' minutes ' + str(seconds % 60) + ' seconds'


#####################################
# EDIT THESE
#####################################
download_dir = 'C:\\Users\\leowa\\Music'
audio_itag = 140  # streams have a specific identifying tag, 140 is 128kbps audio only

'''
These are the common stream formats:
Only change the itag if you know what you're doing

<Stream: itag="18" mime_type="video/mp4" res="360p" fps="30fps" vcodec="avc1.42001E" acodec="mp4a.40.2" progressive="True" type="video">
<Stream: itag="22" mime_type="video/mp4" res="720p" fps="30fps" vcodec="avc1.64001F" acodec="mp4a.40.2" progressive="True" type="video">
<Stream: itag="137" mime_type="video/mp4" res="1080p" fps="30fps" vcodec="avc1.640028" progressive="False" type="video">
<Stream: itag="248" mime_type="video/webm" res="1080p" fps="30fps" vcodec="vp9" progressive="False" type="video">
<Stream: itag="136" mime_type="video/mp4" res="720p" fps="30fps" vcodec="avc1.64001f" progressive="False" type="video">
<Stream: itag="247" mime_type="video/webm" res="720p" fps="30fps" vcodec="vp9" progressive="False" type="video">
<Stream: itag="135" mime_type="video/mp4" res="480p" fps="30fps" vcodec="avc1.4d401e" progressive="False" type="video">
<Stream: itag="244" mime_type="video/webm" res="480p" fps="30fps" vcodec="vp9" progressive="False" type="video">
<Stream: itag="134" mime_type="video/mp4" res="360p" fps="30fps" vcodec="avc1.4d401e" progressive="False" type="video">
<Stream: itag="243" mime_type="video/webm" res="360p" fps="30fps" vcodec="vp9" progressive="False" type="video">
<Stream: itag="133" mime_type="video/mp4" res="240p" fps="30fps" vcodec="avc1.4d4015" progressive="False" type="video">
<Stream: itag="242" mime_type="video/webm" res="240p" fps="30fps" vcodec="vp9" progressive="False" type="video">
<Stream: itag="160" mime_type="video/mp4" res="144p" fps="30fps" vcodec="avc1.4d400c" progressive="False" type="video">
<Stream: itag="278" mime_type="video/webm" res="144p" fps="30fps" vcodec="vp9" progressive="False" type="video">
<Stream: itag="140" mime_type="audio/mp4" abr="128kbps" acodec="mp4a.40.2" progressive="False" type="audio">
<Stream: itag="249" mime_type="audio/webm" abr="50kbps" acodec="opus" progressive="False" type="audio">
<Stream: itag="250" mime_type="audio/webm" abr="70kbps" acodec="opus" progressive="False" type="audio">
<Stream: itag="251" mime_type="audio/webm" abr="160kbps" acodec="opus" progressive="False" type="audio">
'''

while True:
    url = input('Enter the url of the video or playlist: ').rstrip()
    print()
    video = None

    if 'list' in url:
        video = []
        playlist = Playlist(url)
        playlist._video_regex = re.compile(r"\"url\":\"(/watch\?v=[\w-]*)")
        # print(playlist.video_urls)
        for v in playlist.video_urls:
            try:
                yt = YouTube(v)
                video.append(yt)
                print("Title  :", yt.title)
                print("Length :", convert_time(int(yt.length)))
                print("Channel:", yt.author)
                print()
            except:
                print("Error: Failed to load video at:", v)
                print()
    else:
        try:
            video = YouTube(url)
        except:
            print("Couldn't find video at url:", url)

    if video is not None:
        # if its a playlist
        if str(type(video)) == "<class 'list'>":
            print("Videos :", len(video))
            print()

            if input("Download this playlist (Y or N): ").lower() == 'y':
                print()
                dl = input("Download video or audio: ")
                print()
                while dl.lower() != 'video' and dl.lower() != 'audio':
                    dl = input("Enter video or audio as download options: ")
                    print()
                if dl.lower() == 'video':
                    res = input("Enter desired resolution (or high for highest avaliable): ")
                    if res.lower() == 'high':
                        for v in video:
                            stream = v.streams.get_highest_resolution()
                            if stream is None:
                                print("Failed to get stream for", v.title)
                            else:
                                print("Downloading:", v.title)
                                stream.download(output_path=download_dir, filename=v.title)
                    else:
                        for v in video:
                            stream = v.streams.get_by_resolution(res)
                            if stream is None:
                                print("Failed to get stream for", v.title)
                            else:
                                print("Downloading:", v.title)
                                stream.download(output_path=download_dir, filename=v.title)

                elif dl.lower() == 'audio':
                    for v in video:
                        stream = v.streams.get_by_itag(audio_itag)
                        if stream is None:
                            print("Failed to get stream for", v.title)
                        else:
                            print("Downloading:", v.title)
                            stream.download(output_path=download_dir, filename=v.title)
                print("Download complete at", download_dir)

        # if its just a video
        else:
            print("Title  : ", video.title)
            print("Length : ", convert_time(int(video.length)))
            print("Channel: ", video.author)
            print()

            # Uncomment this to see all stream types for a given video
            '''
            for s in video.streams:
                print(s)
            '''

            if input("Download this video (Y or N): ").lower() == 'y':
                dl = input("Download video or audio: ")
                while dl.lower() != 'video' and dl.lower() != 'audio':
                    dl = input("Enter video or audio as download options: ")
                    print()
                if dl.lower() == 'video':
                    res = input("Enter desired resolution (or high for highest avaliable): ")
                    if res.lower() == 'high':
                        stream = video.streams.get_highest_resolution()
                    else:
                        stream = video.streams.get_by_resolution(res)

                elif dl.lower() == 'audio':
                    stream = video.streams.get_by_itag(audio_itag)

                if stream is None:
                    print("Error: Unable to find given stream quality or resolution (make sure resolution is in the form xxxxp, example 1080p)")
                else:
                    print("Downloading...")
                    stream.download(output_path=download_dir, filename=video.title)
                    print("Download complete at", download_dir)

    print()
