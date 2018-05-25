#!/usr/bin/env python3
import pygame

from mygame.player import Player
from mygame.platform import Platform
from mygame.enemy import Enemy


class Window(object):

    def __init__(self, width=800, height=600):
        self._width = width
        self._height = height
        self.cycle = 20
        self.current_cycle = 0

        pygame.init()
        pygame.display.set_caption("My Py Game")
        self.ground = 440
        self.player = Player('PlayerOne', 0, self.ground)
        self.platforms = [Platform(200,self.ground), Platform(350,self.ground-80)]
        self.enemies = [Enemy(720,self.ground+60)]

    def run(self):
        running = True
        while running:
            self.refresh()
            self.player.is_moving = False
            # Detect pressed keys
            key = pygame.key.get_pressed()
            # Move Player
            if key[pygame.K_LEFT] or key[pygame.K_RIGHT]:
                self.player.update(key)
                # Define player limits
                if (self.player._x + self.player.lenght) > self._width:
                    self.player._x = self._width - self.player.lenght
                elif self.player._x < 0:
                    self.player._x = 0
            # Start jump
            if key[pygame.K_UP] and self.player.is_ground == True:
                self.player.update(key)
            # Quit game
            if key[pygame.K_ESCAPE]:
                running = False

            # If player is on the ground
            self.player.is_ground = False
            for platform in self.platforms:
                player_x_pos = self.player._x + 33
                if self.player._y <= (platform.y_pos - platform.height+10) and self.player._y >= (platform.y_pos - platform.height)\
                and player_x_pos >= platform.x_pos and player_x_pos <= platform.x_end:
                    self.player._y = platform.y_pos - platform.height
                    self.player.is_ground = True

                if self.player._y == self.ground:
                    self.player.is_ground = True

            # If player is jumping
            if self.player.is_jumping:
                self.player.jump()

            if self.player.is_ground == False and self.player.is_jumping == False:
                # Falling
                self.player.move_y(+self.player.gravity)

            # if Player is hurt, he can't be hit again while the cycle is not finish
            if self.player.is_hurt == True:
                self.player.hurt()
                if self.current_cycle <= self.cycle:
                    self.current_cycle += 1
                elif self.current_cycle >= self.cycle:
                    self.player.is_hurt = False
                    self.current_cycle = 0

            for enemy in self.enemies:
                # Enemy deplacement
                if enemy.look_left:
                    enemy.move_x(-1)
                else:
                    enemy.move_x(+1)
                # Define direction
                if (enemy._x + enemy.lenght) > self._width:
                    enemy.look_left = True
                elif enemy._x < 0:
                    enemy.look_left = False

                if self.player.is_hurt == False:
                    # if enemy touch player
                    enemy_rect = pygame.Rect(enemy._x, enemy._y, enemy.lenght, enemy.height)
                    player_rect = pygame.Rect(self.player._x, self.player._y, self.player.lenght, self.player.height)
                    if player_rect.colliderect(enemy_rect):
                        self.player.health -= 1
                        self.player.is_hurt = True
                        self.player.hurt_roof = self.player._y + self.player.hurt_height
                        if self.player.look_left:
                            self.player.hurt_distance_limit = self.player._x + self.player.hurt_distance
                        else:
                            self.player.hurt_distance_limit = self.player._x - self.player.hurt_distance

                        # Don't get out the screen !
                        if self.player.hurt_distance_limit > self._width:
                            self.player.look_left = False
                            self.player.hurt_distance_limit = self._width
                        elif self.player.hurt_distance_limit < 0:
                            self.player.look_left = True
                            self.player.hurt_distance_limit = 0

                        if self.player.health > 0:
                            print('touched, player life = ', self.player.health)
                        elif self.player.health <= 0:
                            print('Player is dead !')
                            running = False


    def refresh(self):
        self._window = pygame.display.set_mode((800,600))

        # Set images
        player_image = pygame.image.load(self.player.player_idle).convert_alpha()

        if self.player.is_hurt == True:
            player_image = pygame.image.load(self.player.player_hurt).convert_alpha()
        elif self.player.is_jumping == True:
            player_image = pygame.image.load(self.player.player_jump).convert_alpha()
        elif self.player.is_moving == True:
            walk_image = self.player.get_walk_image()
            player_image = pygame.image.load(walk_image).convert_alpha()

        # Where player is looking
        if self.player.look_left:
            player_image = pygame.transform.flip(player_image, True, False)

        font = pygame.image.load('mygame/assets/bg.png')
        ground = pygame.image.load('mygame/assets/Tiles/grassMid.png')

        # Set the font background
        for y in range(0, 600, 256):
            for x in range(0, 800, 256):
                self._window.blit(font, (x, y))
        # Set the ground
        for x in range(0, 800, 70):
            self._window.blit(ground, (x, 530))

        # Display platforms
        for platform in self.platforms:
            block = pygame.image.load(platform.image)
            self._window.blit(block, (platform.x_pos, platform.y_pos))

        # Enemies
        for enemy in self.enemies:
            enemy_image = pygame.image.load(enemy.image).convert_alpha()
            # Where enemy is looking
            if enemy.look_left == False:
                enemy_image = pygame.transform.flip(enemy_image, True, False)
            self._window.blit(enemy_image, (enemy._x, enemy._y))

        # Set player position
        self._window.blit(player_image, (self.player._x, self.player._y))

        pygame.display.flip()
