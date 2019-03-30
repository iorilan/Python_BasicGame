import sys
import pygame
from pygame.sprite import Group

from alien import Alien
from settings import GameSettings
from ship import Ship
import game_functions as gf
from GameStats import GameStats
from button import Button
from ScoreBoard import Scoreboard
from LeftShip import LeftShip

def run_game():
    pygame.init()
    # settings
    setting = GameSettings()
    screen = pygame.display.set_mode((setting.screen_width, setting.screen_height))
    pygame.display.set_caption(setting.title)
    play_button = Button(setting, screen, "Play")

    ship = Ship(screen, setting)
    bullets = Group()
    aliens = Group()
    gf.create_fleet(setting, screen, ship, aliens)
    stats = GameStats(setting)
    sb = Scoreboard(setting, screen, stats)
    ls = LeftShip(setting, screen, stats)

    while True:
        # game events
        gf.check_events(ship, bullets, aliens, screen, setting, stats, play_button, sb, ls)

        if stats.game_active:
            ship.updatePosition()
            gf.update_bullets(setting, screen, ship, aliens, bullets, stats, sb)
            gf.update_aliens(setting, stats, screen, ship, aliens, bullets, ls)
        gf.update_screen(setting, stats, screen, ship, bullets, aliens, play_button, sb, ls)


run_game()
