import pygame

from ants_and_map import *
from config import *
from direction import *

pygame.init()

win = pygame.display.set_mode(WIN_SIZE)
map = Map(0, 0)
home = Home(map.count_blok_y // 2, map.count_blok_y // 2 - 2, map)
ant_test = Ant(home.x_exit, home.y_exit, map, home.x_exit, home.y_exit)
ant = Ant(0, 0, map, home.x_exit, home.y_exit)
moving_sprites = pygame.sprite.Group()
homes = pygame.sprite.Group()
moving_sprites.add(ant_test)
moving_sprites.add(ant)
homes.add(home)
# moving_sprites.add(map)
clock = pygame.time.Clock()
pos = [0, 0]


def redraw():
    map.draw_matrix(win)
    homes.draw(win)
    homes.update()
    moving_sprites.update(win)
    pygame.display.update()


random_move = pygame.USEREVENT
pygame.time.set_timer(random_move, 100)

while True:
    clock.tick(25)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            raise SystemExit('А ты любишь капибар? :)')

        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            map.draw_stone_test(pos)

        if event.type == random_move:
            ant_test.to_patrol()

        if event.type == pygame.MOUSEWHEEL:
            scale += event.y
            if scale < 1:
                scale = 1
            map.size_block = SIZE_BLOCK * scale
            ant.image = pygame.transform.scale(ant.image,
                                               (32 * scale, 32 * scale))
            ant_test.image = pygame.transform.scale(ant.image,
                                                    (32 * scale, 32 * scale))
            home.image = pygame.transform.scale(home.image,
                                                (SIZE_BLOCK * 8 * scale, SIZE_BLOCK * 5 * scale))

    keys = pygame.key.get_pressed()

    if keys[pygame.K_w]:
        ant.move(up)

    if keys[pygame.K_s]:
        ant.move(down)

    if keys[pygame.K_d]:
        ant.move(right)

    if keys[pygame.K_a]:
        ant.move(left)

    if keys[pygame.K_r]:
        ant_test.x = home.x_exit
        ant_test.y = 0
        ant_test.map.matrix[ant_test.x][ant_test.y] += ' ant'
        ant_test.restricted_blocks.clear()

    redraw()
