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


inUse = True

while inUse:
    url = input('Enter the url of the video or playlist: ')
    if 'list' in url:
        video = []
        playlist = Playlist(url)
        playlist._video_regex = re.compile(r"\"url\":\"(/watch\?v=[\w-]*)")
        for v in playlist.video_urls:
            video.append(YouTube(v))
    else:
        video = YouTube(url)

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
