import pygame
from pygame.constants import QUIT, K_DOWN, K_UP, K_LEFT, K_RIGHT
import random

pygame.init()

FPS = pygame.time.Clock()

HEIGHT = 700
WIDTH = 1200

FONT = pygame.font.SysFont("Verdana", 20)

COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_BLUE = (0, 0, 255)
COLOR_RED = (255, 0, 0)

main_display = pygame.display.set_mode((WIDTH, HEIGHT))

bg = pygame.transform.scale(pygame.image.load("background.png"), (WIDTH, HEIGHT))
bg_X1 = 0
bg_X2 = bg.get_width()
bg_move = 3

player_size = (20, 20)
# pygame.Surface(player_size)
player = pygame.transform.scale(pygame.image.load("player.png"), (140, 50))
# player.fill(COLOR_BLACK)
# player_rect = player.get_rect()
player_rect = player.get_rect(topleft=(10, 300))
# player_speed = [1, 1]
player_move_down = [0, 7]
player_move_right = [7, 0]
player_move_top = [-0, -7]
player_move_left = [-7, -0]


def create_enemy():
    enemy_size = (30, 30)
    enemy = pygame.transform.scale(pygame.image.load("enemy.png"), (100, 50))
    # enemy = pygame.Surface(enemy_size)
    # enemy.fill(COLOR_BLUE)
    # enemy_rect = pygame.Rect(WIDTH, random.randint(0, HEIGHT), *enemy_size)
    enemy_rect = pygame.Rect(
        WIDTH,
        random.randint(enemy.get_height(), HEIGHT - enemy.get_height()),
        *enemy.get_size()
    )
    enemy_move = [random.randint(-8, -4), 0]
    return [enemy, enemy_rect, enemy_move]


def create_bonus():
    bonus_size = (50, 50)
    bonus = pygame.transform.scale(pygame.image.load("bonus.png"), (100, 150))
    # bonus = pygame.Surface(bonus_size)
    # bonus.fill(COLOR_RED)
    # bonus_rect = pygame.Rect(random.randint(0, WIDTH), 0, *bonus_size)
    bonus_width = bonus.get_width()
    bonus_rect = pygame.Rect(
        random.randint(bonus_width, WIDTH - bonus_width),
        -bonus.get_height(),
        *bonus.get_size()
    )
    bonus_move = [0, random.randint(4, 8)]
    return [bonus, bonus_rect, bonus_move]


CREATE_ENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(CREATE_ENEMY, 1500)

CREATE_BONUS = pygame.USEREVENT + 2
pygame.time.set_timer(CREATE_BONUS, 1500)

enemies = []

bonuses = []

score = 0

playing = True

while playing:
    FPS.tick(200)
    for event in pygame.event.get():
        if event.type == QUIT:
            playing = False
        if event.type == CREATE_ENEMY:
            enemies.append(create_enemy())
        if event.type == CREATE_BONUS:
            bonuses.append(create_bonus())

    #    main_display.fill(COLOR_BLACK)

    bg_X1 -= bg_move
    bg_X2 -= bg_move

    if bg_X1 < -bg.get_width():
        bg_X1 = bg.get_width()

    if bg_X2 < -bg.get_width():
        bg_X2 = bg.get_width()

    main_display.blit(bg, (bg_X1, 0))
    main_display.blit(bg, (bg_X2, 0))

    keys = pygame.key.get_pressed()

    if keys[K_DOWN] and player_rect.bottom < HEIGHT:
        player_rect = player_rect.move(player_move_down)

    if keys[K_RIGHT] and player_rect.right < WIDTH:
        player_rect = player_rect.move(player_move_right)

    if keys[K_UP] and player_rect.top < HEIGHT:
        player_rect = player_rect.move(player_move_top)

    if keys[K_LEFT] and player_rect.left < WIDTH:
        player_rect = player_rect.move(player_move_left)

    for enemy in enemies:
        enemy[1] = enemy[1].move(enemy[2])
        main_display.blit(enemy[0], enemy[1])

        if player_rect.colliderect(enemy[1]):
            playing = False

    for bonus in bonuses:
        bonus[1] = bonus[1].move(bonus[2])
        main_display.blit(bonus[0], bonus[1])

        if player_rect.colliderect(bonus[1]):
            score += 1
            bonuses.pop(bonuses.index(bonus))

    #    enemy_rect = enemy_rect.move(enemy_move)

    #    if player_rect.bottom >= HEIGHT:
    #        player_speed = random.choice(([1, -1], [-1, -1]))

    #    if player_rect.right >= WIDTH:
    #        player_speed = random.choice(([-1, -1], [-1, 1]))

    #    if player_rect.top <= 0:
    #        player_speed = random.choice(([-1, 1], [1, 1]))

    #    if player_rect.left <= 0:
    #        player_speed = random.choice(([1, 1], [1, -1]))

    main_display.blit(FONT.render(str(score), True, COLOR_BLACK), (WIDTH - 50, 20))
    main_display.blit(player, player_rect)

    #   main_display.blit(enemy, enemy_rect)

    print(len(enemies))

    print(len(bonuses))

    #    player_rect = player_rect.move(player_speed)

    pygame.display.flip()

    for enemy in enemies:
        if enemy[1].left < 0:
            enemies.pop(enemies.index(enemy))

    for bonus in bonuses:
        if bonus[1].bottom < 1:
            bonuses.pop(bonuses.index(bonus))
