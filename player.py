#!/usr/bin/env python3
import pygame

class Player(object):
    # image_left = 'images/player-left.png'
    # image_right = 'images/player-right.png'

    def __init__(self, name, x=0, y=0):
        self._name = name
        self._x = x
        self._y = y
        self.lenght = 66
        self.height = 92
        self.health = 5
        self.gravity = 5
        self.look_left = False
        self.is_moving = False
        self.is_ground = True
        self.is_jumping = False
        self.is_hurt = False
        self.jump_roof = self._y
        self.hurt_roof = self._y
        self.jump_height = 120
        self.hurt_height = 80
        self.hurt_distance = 60
        self.hurt_distance_limit = 0
        self.hurt_velocity = 10
        self.current_walk_image = 1
        self.walk_image_max = 11
        # Define images
        self.player_idle = 'mygame/assets/Player/p2_front.png'
        self.walk_image = 'mygame/assets/Player/p2_walk/PNG/p2_walk'
        self.player_moving = 'mygame/assets/Player/p2_stand.png'
        self.player_jump = 'mygame/assets/Player/p2_jump.png'
        self.player_hurt = 'mygame/assets/Player/p2_hurt.png'

    def move_x(self, value):
        # Other stuff like checking if you are running into a wall
        self._x += value

    def move_y(self, value):
        # Other stuff like checking if you a stopped by a plateform in you fall.
        self._y += value

    def get_walk_image(self):
        if self.current_walk_image <= 8:
            self.current_walk_image += 1
            current_image = '0' + str(self.current_walk_image)
        elif self.current_walk_image >= 11:
            self.current_walk_image = 1
            current_image = '0' + str(self.current_walk_image)
        elif self.current_walk_image >= 9:
            self.current_walk_image += 1
            current_image = str(self.current_walk_image)

        return self.walk_image + current_image + '.png'

    def jump(self):

        if self._y > self.jump_roof and self.is_jumping == True:
            self.move_y(-self.gravity)
        elif self._y <= self.jump_roof and self.is_jumping == True:
            self.is_jumping = False

    def hurt(self):
        if self.look_left:
            if self._x < self.hurt_distance_limit:
                self.move_x(+self.hurt_velocity)
        else:
            if self._x > self.hurt_distance_limit:
                self.move_x(-self.hurt_velocity)

    def update(self, key):
        if self.is_hurt == False:
            if key[pygame.K_LEFT]:
                self.move_x(-5)
                self.look_left = True
                self.is_moving = True
            elif key[pygame.K_RIGHT]:
                self.move_x(+5)
                self.look_left = False
                self.is_moving = True

            if key[pygame.K_UP] and self.is_jumping == False and self.is_ground == True:
                self.is_jumping = True
                self.is_ground = False
                self.jump_roof = self._y - self.jump_height
