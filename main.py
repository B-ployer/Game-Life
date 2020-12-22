"""
Существует поле состоящее из клеток. Изначально все эти клетки имеют значение
0, мы можем задать значение 1 для клетки. Клетка живёт 1 ход, а потом умирает,
если рдом нет 2 или 3 клеток со значением 1. Рождение новой клетки
происходит, если рядом с ней есть хотя бы 3 клетки со значением 1.
"""

import pygame
from random import randint
from copy import deepcopy

RES = WIDTH, HEIGHT = 1200, 600
TILE = 7
W, H = WIDTH // TILE, HEIGHT // TILE
FPS = 30

pygame.init()
surface = pygame.display.set_mode(RES)
clock = pygame.time.Clock()

next_field = [[0 for i in range(W)] for j in range(H)]
current_field = [[0 for i in range(W)] for j in range(H)]


def create_glider(y, x, hor = 0, vert = 0):
    if hor == 0 and vert == 0 :
        gliders_pos = ((y, x), (y - 2, x), (y - 1, x + 1), (y, x + 1), (y, x - 1))
    elif hor == 1 and vert == 0 :
        gliders_pos = ((y, x), (y + 2, x), (y + 1, x + 1), (y, x + 1), (y, x - 1))
    elif hor == 0 and vert == 1 :
        gliders_pos = ((y, x), (y - 2, x), (y - 1, x - 1), (y, x - 1), (y, x + 1))
    elif hor == 1 and vert == 1 :
        gliders_pos = ((y, x), (y + 2, x), (y + 1, x - 1), (y, x - 1), (y, x + 1))

    return gliders_pos


def check_cell(current_field, x, y):
    count = 0
    for j in range(y - 1, y + 2):
        for i in range(x - 1, x + 2):
            if current_field[j][i]:
                count += 1

    if current_field[y][x]:
        count -= 1
        if count == 2 or count == 3:
            return 1
        return 0
    else:
        if count == 3:
            return 1
        return 0


def game_pause(stop=1):
    while stop:

        surface.fill(pygame.Color('black'))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.__dict__['button'] == 1:
                    x, y = event.__dict__['pos']
                    x, y = x // TILE, y // TILE
                    if current_field[y][x]:
                        current_field[y][x] = 0
                    else:
                        current_field[y][x] = 1
                if event.__dict__['button'] == 3:
                    stop = 0

        for x in range(0, WIDTH, TILE):
            pygame.draw.line(surface, pygame.Color('darkslategray'), (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILE):
            pygame.draw.line(surface, pygame.Color('darkslategray'), (0, y), (WIDTH, y))

        for x in range(1, W - 1):
            for y in range(1, H - 1):
                if current_field[y][x]:
                    pygame.draw.rect(surface, pygame.Color('forestgreen'), (x * TILE + 2, y * TILE + 2, TILE - 2, TILE - 2))

        pygame.display.flip()
        clock.tick(FPS)


for g in range(30, 101, 6):
    for i, j in create_glider(30, g):
        current_field[i][j] = 1

#for g in range(30, 101, 6):
#    for i, j in create_glider(57, g, 1):
#        current_field[i][j] = 1

while True:

    surface.fill(pygame.Color('black'))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.__dict__['button'] == 1:
                x, y = event.__dict__['pos']
                x, y = x // TILE, y // TILE
                if current_field[y][x]:
                    current_field[y][x] = 0
                else:
                    current_field[y][x] = 1
            if event.__dict__['button'] == 3:
                game_pause()

    #draw grid
    [pygame.draw.line(surface, pygame.Color('darkslategray'), (x, 0), (x, HEIGHT)) for x in range(0, WIDTH, TILE)]
    [pygame.draw.line(surface, pygame.Color('darkslategray'), (0, y), (WIDTH, y)) for y in range(0, HEIGHT, TILE)]
    #draw life
    for x in range(1, W - 1):
        for y in range(1, H - 1):
            if current_field[y][x]:
                pygame.draw.rect(surface, pygame.Color('forestgreen'), (x * TILE + 2, y * TILE + 2, TILE - 2, TILE - 2))
            next_field[y][x] = check_cell(current_field, x, y)

    current_field = deepcopy(next_field)

    print(int(clock.get_fps()))
    pygame.display.flip()
    clock.tick(FPS)
