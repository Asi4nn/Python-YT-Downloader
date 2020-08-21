# Python-YT-Downloader

## How to use

Requires pytube3 to be installed, the program will try and install this for the user on launch

On line 56 you can edit the directory you wish the downloads to go into
Line 57 has the audio i_tag, which controls the quality of the audio only downloads (defaults to 128kbps)
```python
#####################################
# EDIT THESE
#####################################
download_dir = 'C:\\Users\\leowa\\Music'
audio_itag = 140  # streams have a specific identifying tag, 140 is 128kbps audio only
```

If you're using the exe build instead, the program will always download in the folder that it's in

## Disclaimer

- Some videos tend to not load, not at the fault of the program, but because of the module
- From testing, it seems quite random to whether a video will load or not, so try a few times if a video doesn't load
