#!/usr/bin/env python3
import pygame

class Enemy(object):
    # image_left = 'images/player-left.png'
    # image_right = 'images/player-right.png'

    def __init__(self, x=0, y=0):
        self._x = x
        self._y = y
        self.look_left = True
        self.lenght = 54
        self.height = 31
        self.image = 'mygame/assets/Enemies/snailWalk1.png'

    def move_x(self, value):
        # Other stuff like checking if you are running into a wall
        self._x += value

    def update(self):
        pass
