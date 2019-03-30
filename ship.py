import pygame


class Ship:
    def __init__(self, screen, setting):
        self.screen = screen

        self.image = pygame.image.load("images/ship.bmp")
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        self.moving_left = False
        self.moving_right = False

        self.speed = setting.ship_speed

    def blitme(self):
        self.screen.blit(self.image, self.rect)

    def updatePosition(self):
        if self.rect.right >= self.screen_rect.right and self.moving_right:
            return
        if self.rect.left <= 0 and self.moving_left:
            return

        if self.moving_right:
            self.rect.centerx += self.speed
        if self.moving_left:
            self.rect.centerx -= self.speed

    def center_ship(self):
        self.center = self.screen_rect.centerx