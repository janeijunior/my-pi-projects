#!/usr/bin/python

# The Sound Engine
# Provides helper functions and a playlist class
# Zach Bernal | Summer 2009

import pygame, sys, os
import math, copy, random
if not pygame.mixer: print 'Warning, pygame.mixer did not load. Sound disabled.'

__all__ = ["init", "isenabled", "NoneSound", "load_sound", "load_music", "Playlist"]

__audio_enabled = False

def init():
    """ A wrapper for pygame.mixer.init(). """
	global __audio_enabled
	try:
		if not __audio_enabled:
			pygame.mixer.init(22050, -16, 2, 1024) # in pygame 1.9, third argument is stereo if 2.
			#pygame.mixer.init()
			__audio_enabled = True
			print "Audio Enabled."
	except pygame.error, message :
		__audio_enabled = False
		print "Audio disabled:", message
	return __audio_enabled

def isenabled():
	return __audio_enabled

class NoneSound:
	def play(self): pass
	def stop(self): pass
	def fadeout(self, *args): pass
	def set_volume(self, *args): pass
	def get_volume(self, *args): pass
	def get_num_channels(self, *args): pass
	def get_length(self, *args): pass
	def get_buffer(self, *args): pass


#sound loader
def load_sound(name, dirname = 'sounds', soundcache = {}):

	if not pygame.mixer or not __audio_enabled:
		return NoneSound()
	fullname = os.path.join(dirname, name)

	if fullname in soundcache:
		return soundcache[fullname]

	try:
		sound = pygame.mixer.Sound(fullname)
	except pygame.error, message:
		print "Cannot load sound:", fullname
		raise SystemExit, message

	# Cache sound
	soundcache[fullname] = sound
	return sound

#music loader
def load_music(name, dirname = 'bgm'):
	if not pygame.mixer or not __audio_enabled:
		return False
	fullname = os.path.join(dirname, name)
	try:
		music = pygame.mixer.music.load(fullname)
	except pygame.error, message:
		print "Cannot load music:", fullname
		raise SystemExit, message
	return True




class Playlist():
	""" A Macintosh-style playlist abstraction """
	NORANDOM, RANDOM = range(2)
	NOLOOP, LOOP, LOOPONE  = range(3)
	STOP, PLAY, PAUSE = range(3)
	PASSIVE, SPECIFIC, NEXT, PREV = range(4)

	def __init__(self):

		# initialize mixer
		if not init():
			return None

		# State machine states
		self.randomstate = Playlist.NORANDOM # whether to use random or incrementing tracklist
		self.loopstate = Playlist.NOLOOP # whether to loop at end of list or on single track or to stop at end.
		self.pausestate = Playlist.STOP # whether to play, stop, or pause playback.
		self.prev_pausestate = Playlist.STOP # previous state, for edge cases.
		self.controlstate = Playlist.PASSIVE # overrides loop and random states to switch between tracks

		# list of filenames to play
		self.playlist = []
		self.randomindexes = range(0, len(self.playlist))

		# current track starts at -1, gets incremented to first in list
		self.index = -1
		
		# need a random number generator for random play...
		# using the python native instance
		#random.seed(time.time())

	def update(self):
		""" Update internal state of playlist and pygame music player. Return true if playing or paused, return false if stopped. """
		# Don't allow empty playlists to play.
		if len(self.playlist) == 0:
			pass
			###print "nothing to play!"
		# if playing from stop or play... (will contine to play tracks...)
		elif self.pausestate == Playlist.PLAY and self.prev_pausestate != Playlist.PAUSE:
			# Start the next track, if we're done playing the current one..
			if not pygame.mixer.music.get_busy():

				# what do we do when we run out of random indexes?
				# loop: reset them, otherwise we've finished the playlist.
				if len(self.randomindexes) == 0:
					if self.loopstate == Playlist.LOOP:
						self._resetrandom()
					else:
						print "Done playing random indexes."
						self.restart()
						return False

				#print "random indexes:", self.randomindexes

				# what is the next track?
				# control states and the "loop one" setting override everything else
				if self.controlstate == Playlist.SPECIFIC:
					# keep self.index the same, it was set in self.play()
					if self.index in self.randomindexes: 
						self.randomindexes.remove(self.index)
					self.controlstate = Playlist.PASSIVE # the control expires after execution.
				elif self.controlstate == Playlist.NEXT:
					self.index += 1	
					self.controlstate = Playlist.PASSIVE # the control expires after execution.
				elif self.controlstate == Playlist.PREV:
					self.index -= 1	
					if self.index < 0:
						self.index = len(self.playlist)-1
					self.controlstate = Playlist.PASSIVE # the control expires after execution.

				elif self.loopstate == Playlist.LOOPONE:
					# keep self.index the same
					if self.index in self.randomindexes: 
						self.randomindexes.remove(self.index)
				# either increment in random sequence or increment by one
				elif self.randomstate == Playlist.RANDOM:
					# get a random thing from the remaining items not yet chosen
					#self.index = random.randint(0, len(self.playlist)-1)
					self.index = random.choice(self.randomindexes)
					self.randomindexes.remove(self.index)
				else: # increment
					self.index += 1

				# what do we do when we hit the end?
				# loop: go to 0, otherwise we've finished the playlist.
				if self.index >= len(self.playlist):
					if self.loopstate == Playlist.LOOP:
						self.index = 0
					else:
						print "Done playing the list."
						self.restart()
						return False

				# load & play next track
				load_music(self.playlist[self.index], "")
				print str(self.index) + ":", self.playlist[self.index], "r:", self.randomstate, "l:", self.loopstate
				pygame.mixer.music.play()
			return True

		# if playing from pause...
		elif self.pausestate == Playlist.PLAY and self.prev_pausestate == Playlist.PAUSE:
			pygame.mixer.music.unpause()
			self.prev_pausestate == Playlist.PLAY # forget about the pause so that more tracks will be played
			return True
			
		# if pausing (do this once coming from play, then stop pausing after that)
		elif self.pausestate == Playlist.PAUSE and self.prev_pausestate == Playlist.PLAY:
			pygame.mixer.music.pause()
			self.prev_pausestate = Playlist.PAUSE # forget to keep pausing
			return True
		
		# if stopping from play or pause...
		elif self.pausestate == Playlist.STOP and self.prev_pausestate != Playlist.STOP:
			pygame.mixer.music.stop()
			self.prev_pausestate = Playlist.STOP # forget to keep stopping
			return False


	def _play(self, index = -1):
		if index > -1:
			# force this index to be played.
			self.index = index
			self.controlstate = Playlist.SPECIFIC
		self.prev_pausestate = self.pausestate
		self.pausestate = Playlist.PLAY
	def _pause(self):
		self.prev_pausestate = self.pausestate
		self.pausestate = Playlist.PAUSE
	def _stop(self):
		self.prev_pausestate = self.pausestate
		self.pausestate = Playlist.STOP
	def _next(self):
		self.controlstate = Playlist.NEXT
	def _prev(self):
		self.controlstate = Playlist.PREV

	def _restart(self):
		self._stop()
		self.index = -1
		self._resetrandom()

	def _resetrandom(self):
		#random.seed(time.time())
		self.randomindexes = range(0, len(self.playlist))
		print "reset random indexes"

	def play(self, index = -1):
		self._play(index)
		self.update()

	def next(self):
		self._stop()
		self.update()
		self._next()
		self._play()

	def prev(self):
		self._stop()
		self.update()
		self._prev()
		self._play()

	def pause(self):
		if self.pausestate == Playlist.PAUSE:
			self.play()
		else:
			self._pause()
			self.update()

	def stop(self):
		self._stop()
		self.update()

	def add(self, filename, dirname = "bgm"):
		fullname = os.path.join( dirname, filename)
		self.playlist.append(fullname)
		self._resetrandom()

	def addfolder(self, foldername = "bgm"):
		for filename in os.listdir(foldername):
			if filename.endswith(".mp3") or filename.endswith(".wav"):
				self.add(filename, foldername)

	def setrandom(self):
		self.randomstate = Playlist.RANDOM
	def unsetrandom(self):
		self.randomstate = Playlist.NORANDOM
	def setloop(self):
		self.loopstate = Playlist.LOOP
	def setloopone(self):
		self.loopstate = Playlist.LOOPONE
	def unsetloop(self):
		self.loopstate = Playlist.NOLOOP

	def set_volume(self, vol):
		pygame.mixer.music.set_volume(vol)

	def get_volume(self):
		return pygame.mixer.music.get_volume()
	def __len__(self):
		return len(self.playlist);


if __name__ == "__main__":
	player = Playlist()

	player.addfolder()

	def playloop(player):
		player.play()
		while player.update():
			pass

	# hey look, interactive shell!
	import code
	shell = code.InteractiveConsole(globals())
	shell.interact()


