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
download_dir = 'C:\Users\leowa\Music'
audio_itag = 140  # streams have a specific identifying tag, 140 is 128kbps audio only


inUse = True

while inUse:
    url = input('Enter the url of the video or playlist: ')
    '''  playlists dont work
    if 'list' in url:
        video = []
        playlist = Playlist(url)
        playlist._video_regex = re.compile(r"\"url\":\"(/watch\?v=[\w-]*)")
        for v in playlist.video_urls:
            video.append(YouTube(v))
    else:
    '''
    video = None
    try:
        video = YouTube(url)
    except:
        print("Couldn't find video at url:", url)

    if video is not None:
        # if its a playlist
        if str(type(video)) == "<class 'list'>":
            for v in video:
                print("Title  : ", v.title)
                print("Length : ", convert_time(int(v.length)))
                print("Channel: ", v.author)
                print()
        # if its just a video
        else:
            print("Title  : ", video.title)
            print("Length : ", convert_time(int(video.length)))
            print("Channel: ", video.author)
            print()

            for s in video.streams.all():
                print(s)

            if input("Download this video (Y or N): ").lower() == 'y':
                dl = input("Download mp4 or mp3: ")
                while dl.lower() != 'mp4' and dl.lower() != 'mp3':
                    dl = input("Enter mp3 or mp4 as download options: ")
                    print()
                if dl.lower() == 'mp4':
                    res = input("Enter desired resolution (or high for highest avaliable): ")
                    if res.lower() == 'high':
                        stream = video.streams.get_highest_resolution()
                    else:
                        stream = video.stream.get_by_resolution(res)

                elif dl.lower() == 'mp3':
                    stream = video.streams.get_by_itag(audio_itag)

                if stream is None:
                    print("Error: Unable to find given stream quality or resolution")
                else:
                    print("Downloading...")
                    stream.download(output_path=download_dir, filename=video.title)
                    print("Download complete at", download_dir)

    if input("Download another? (Y or N): ").lower() == 'n':
        inUse = False
    print()
