import pygame


class LeftShip:
    def __init__(self, settings, screen, stats):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.settings = settings
        self.stats = stats

        self.text_color = (30,30,30)
        self.font = pygame.font.SysFont(None, 48)
        self.image = pygame.image.load("images/ship.bmp")
        self.rect = self.image.get_rect()
        self.rect.width = 20
        self.rect.height = 20
        self.rect.left = self.screen_rect.left
        self.rect.top = self.settings.screen_height - 80

        font_str = str(self.stats.ships_left)
        self.font_image = self.font.render(font_str, True, self.text_color, self.settings.bg_color)

        self.font_rect = self.font_image.get_rect()
        self.font_rect.left = self.screen_rect.left + 75
        self.font_rect.top = self.settings.screen_height - 50

    def updateStats(self, stats):
        self.stats = stats
        font_str = str(self.stats.ships_left)
        self.font_image = self.font.render(font_str, True, self.text_color, self.settings.bg_color)

    def draw(self):
        self.screen.blit(self.font_image, self.font_rect)
        self.screen.blit(self.image, self.rect)