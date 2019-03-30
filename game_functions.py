import sys
from random import randint
from time import sleep

import pygame

from alien import Alien
from bullet import Bullet


# keyboard events
def check_keydown(e, ship, bullets, screen, setting):
    if e.key in [pygame.K_RIGHT, pygame.K_d]:
        ship.moving_right = True
    elif e.key in [pygame.K_LEFT, pygame.K_a]:
        ship.moving_left = True
    elif e.key == pygame.K_SPACE:
        fire_bullet(setting, screen, ship, bullets)
    elif e.key in [pygame.K_q, pygame.K_ESCAPE]:
        sys.exit()


def check_keyup(e, ship, bullets, screen, setting):
    ship.moving_right = False
    ship.moving_left = False


def check_play_button(stats, play_button, mouse_x, mouse_y, settings, screen, ship, aliens, bullets, sb, ls):
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        pygame.mouse.set_visible(False)
        stats.reset()
        stats.game_active = True
        sb.updateStats(stats)
        ls.updateStats(stats)

        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()

        aliens.empty()
        bullets.empty()

        create_fleet(settings, screen, ship, aliens)
        ship.center_ship()


def check_events(ship, bullets, aliens, screen, setting, stats, play_button, sb, ls):
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            sys.exit()
        elif e.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(stats, play_button, mouse_x, mouse_y, setting, screen, ship, aliens, bullets, sb, ls)
        elif e.type == pygame.KEYDOWN:
            check_keydown(e, ship, bullets, screen, setting)
        elif e.type == pygame.KEYUP:
            check_keyup(e, ship, bullets, screen, setting)


def update_screen(setting, stats, screen, ship, bullets, aliens, play_button, sb, ls):
    screen.fill(setting.bg_color)
    for b in bullets:
        b.draw()

    ship.blitme()
    aliens.draw(screen)

    sb.show_score()
    ls.draw()

    if not stats.game_active:
        play_button.draw_button()

    pygame.display.flip()


def ship_hit(settings, stats, screen, ship, aliens, bullets, ls):
    if stats.ships_left > 0:
        stats.ships_left -= 1
        ls.updateStats(stats)
        aliens.empty()
        bullets.empty()
        create_fleet(settings, screen, ship, aliens)
        ship.center_ship()

        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)


# ship
def fire_bullet(setting, screen, ship, bullets):
    if len(bullets) < setting.bullet_max:
        b = Bullet(setting, screen, ship)
        bullets.add(b)


def update_bullets(settings, screen, ship, aliens, bullets, stats, sb):
    bullets.update()
    for b in bullets.copy():
        if b.rect.bottom <= 0:
            bullets.remove(b)
    check_bullet_alien_collisions(settings, screen, ship, aliens, bullets,stats, sb)


# alien
def check_bullet_alien_collisions(settings, screen, ship, aliens, bullets, stats, sb):
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if len(aliens) == 0:
        bullets.empty()
        settings.increaseSpeed()
        stats.level+=1
        sb.prep_level()
        create_fleet(settings, screen, ship, aliens)

    if collisions:
        for aliens in collisions.values():
            stats.score += settings.point * len(aliens)
        sb.prep_score()
        check_high_score(stats, sb)


def create_alien(settings, screen, aliens, alien_number, row_number):
    alien = Alien(settings, screen)
    alien_width = alien.rect.width
    alien.rect.x = alien_width + 2 * alien_width * alien_number
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)


def update_aliens(settings, stats, screen, ship, aliens, bullets, ls):
    fleet_reached_boundary(settings, aliens)
    aliens.update()
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(settings, stats, screen, ship, aliens, bullets, ls)
    check_alien_bottom(settings, stats, screen, ship, aliens, bullets,ls)


def get_number_aliens_x(settings, alien_width):
    available_space_x = settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x


def get_number_rows(settings, ship_height, alien_height):
    available_space_y = (settings.screen_height - (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (3 * alien_height))
    return number_rows


def check_alien_bottom(settings, stats, screen, ship, aliens, bullets,ls):
    screen_rect = screen.get_rect()
    for alien in aliens:
        if alien.rect.bottom >= screen_rect.bottom:
            ship_hit(settings, stats, screen, ship, aliens, bullets,ls)
            break


# group of aliens

def create_fleet(settings, screen, ship, aliens):
    alien = Alien(settings, screen)
    alien_width = alien.rect.width
    number_aliens_x = get_number_aliens_x(settings, alien_width)
    number_rows = get_number_rows(settings, ship.rect.height, alien.rect.height)
    for row_num in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(settings, screen, aliens, alien_number, row_num)


def drop_fleet(settings, aliens):
    for alien in aliens.sprites():
        alien.rect.y += settings.fleet_drop_speed


def fleet_reached_boundary(settings, aliens):
    for alien in aliens.sprites():
        if alien.reached_boundary():
            drop_fleet(settings, aliens)
            settings.fleet_direction = -settings.fleet_direction
            return

def check_high_score(stats,sb):
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()