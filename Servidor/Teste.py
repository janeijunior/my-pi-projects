#!/usr/bin/python

import pygame, sys, os


if __name__ == "__main__":
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load('/home/pi/HousePi/Musicas/01.\ John\ Legend\ -\ John\ Legend\ -\ All\ Of\ Me.mp3')
    pygame.mixer.music.play(0)