#!/usr/bin/env python3
import pygame

class Platform(object):

    def __init__(self, x = 0, y = 0):
        self.x_pos = x
        self.y_pos = y
        self.length = 70
        self.height = 90
        self.image = 'mygame/assets/Tiles/grassHalf.png'
        self.x_end = self.x_pos + self.length