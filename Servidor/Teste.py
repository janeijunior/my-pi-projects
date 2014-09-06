import sys, os

    url=os.system('youtube-dl -g https://www.youtube.com/watch?v=BkbU1VWsOKM')
    os.system('omxplayer -o hdmi '+url)