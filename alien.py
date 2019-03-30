from random import randint

import pygame

from pygame.sprite import Sprite


class Alien(Sprite):

    def __init__(self, setting, screen):
        super(Alien, self).__init__()
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.setting = setting

        self.image = pygame.image.load("images/alien.bmp")
        self.rect = self.image.get_rect()

        self.rect.x = 0
        self.rect.y = 0

        self.x = float(self.rect.x)

    def blitme(self):
        self.screen.blit(self.image, self.rect)

    def update(self):
        #print(str(self.setting.fleet_direction))
        self.rect.x += self.setting.alien_speed * self.setting.fleet_direction
        #self.rect.y += self.setting.fleet_drop_speed

    def reached_boundary(self):
        screen_rect = self.screen.get_rect()

        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            #print("Reached boundary")
            return True
        else:
            return False

