from pyomxplayer import OMXPlayer
from pprint import pprint
omx = OMXPlayer('/home/pi/HousePi/Videos/Ariana.mp4')
pprint(omx.__dict__)
omx.toggle_pause()
#omx.position
omx.stop()