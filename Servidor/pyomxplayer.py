import pexpect
import re
import os

from threading import Thread
from time import sleep

class OMXPlayer(object):

    _FILEPROP_REXP = re.compile(r".*audio streams (\d+) video streams (\d+) chapters (\d+) subtitles (\d+).*")
    _VIDEOPROP_REXP = re.compile(r".*Video codec ([\w-]+) width (\d+) height (\d+) profile (\d+) fps ([\d.]+).*")
    _AUDIOPROP_REXP = re.compile(r"Audio codec (\w+) channels (\d+) samplerate (\d+) bitspersample (\d+).*")
    _STATUS_REXP = re.compile(r"V :\s*([\d.]+).*")
    _DONE_REXP = re.compile(r"have a nice day.*")

    _LAUNCH_CMD = 'omxplayer -r -s %s %s'
    _PAUSE_CMD = 'p'
    _TOGGLE_SUB_CMD = 's'
    _QUIT_CMD = 'q'
    _BACKWARD = '\x5b\x44'
    _FORWARD = '\x5b\x43'


    paused = False
    subtitles_visible = True

    def __init__(self, mediafile, args=None, start_playback=False):
        if not args:
            args = ""
        cmd = self._LAUNCH_CMD % (mediafile, args)
        self._process = pexpect.spawn(cmd)
        
        self.video = dict()
        self.audio = dict()
        
        self._position_thread = Thread(target=self._get_position)
        self._position_thread.start()

        if not start_playback:
            self.toggle_pause()
        self.toggle_subtitles()


    def _get_position(self):
        while True:
            index = self._process.expect([self._STATUS_REXP,
                                            pexpect.TIMEOUT,
                                            pexpect.EOF,
                                            self._DONE_REXP])
            if index == 1: continue
            elif index in (2, 3): break
            else:
                self.position = float(self._process.match.group(1))
            sleep(0.05)

    def toggle_pause(self):
        if self._process.send(self._PAUSE_CMD):
            self.paused = not self.paused

    def toggle_subtitles(self):
        if self._process.send(self._TOGGLE_SUB_CMD):
            self.subtitles_visible = not self.subtitles_visible
    def stop(self):
        self._process.send(self._QUIT_CMD)
        self._process.terminate(force=True)
        os.system("omxplayer -r housepi")

    def set_speed(self):
        raise NotImplementedError

    def set_audiochannel(self, channel_idx):
        raise NotImplementedError

    def set_subtitles(self, sub_idx):
        raise NotImplementedError

    def set_chapter(self, chapter_idx):
        raise NotImplementedError

    def set_volume(self, volume):
        raise NotImplementedError

    def seek(self, minutes):
        raise NotImplementedError

    def backward(self):
        self._process.send(self._BACKWARD)
    
    def forward(self):
        self._process.send(self._FORWARD)    