import math
import pygame
import random
from config import *
from prettytable import PrettyTable
from direction import *

pygame.init()
ant_im = pygame.transform.scale(pygame.image.load('ant.png'),
                                (SIZE_BLOCK * scale, SIZE_BLOCK * scale))
home_1_im = pygame.transform.scale(pygame.image.load('home1.png'),
                                   (SIZE_BLOCK * 9 * scale, SIZE_BLOCK * 5 * scale))


class Home(pygame.sprite.Sprite):
    def __init__(self, x, y, map):
        super().__init__()
        self.x = x
        self.y = y
        self.image = home_1_im
        self.rect = self.image.get_rect()
        self.rect.topleft = [x, y]
        self.map = map
        self.width_block = self.rect.width // SIZE_BLOCK
        self.height_block = self.rect.height // SIZE_BLOCK
        self.x_exit = self.x + self.width_block // 2
        self.y_exit = self.y + self.height_block // 2
        self.to_place(self.width_block, self.height_block)
        self.map.matrix[self.x_exit][self.y_exit] = 'exit'

    def update(self):
        self.rect.topleft = [self.x * self.map.size_block, self.y *
                             self.map.size_block]

    # размещение
    def to_place(self, width, height):
        for x in range(self.x, self.x + width):
            for y in range(self.y, self.y + height):
                self.map.matrix[x][y] = 'home'


class Map(pygame.sprite.Sprite):
    GREEN = (63, 191, 76)
    GREEN_DARK = (90, 163, 85)
    BLACK = (0, 0, 0)

    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.speed = 1
        self.size_block = SIZE_BLOCK
        self.count_blok_x = int(WIN_X / self.size_block)
        self.count_blok_y = int(WIN_Y / self.size_block)
        self.matrix = []
        for j in range(self.count_blok_x):
            self.matrix.append([])
            for k in range(self.count_blok_y):
                self.matrix[j].append('0')

    def draw_blok(self, color, column, row, win):
        # win.blit(color, (10 + column * self.size_block * (column + 1), 100 + row * self.size_block * (row + 1)))
        pygame.draw.rect(win, color, pygame.Rect(column * self.size_block,
                                                 row * self.size_block, self.size_block, self.size_block))

    def draw_stone_test(self, pos):
        self.matrix[pos[0] // SIZE_BLOCK][pos[1] // SIZE_BLOCK] = 'stone'

    def draw_matrix(self, win):
        for row in range(self.count_blok_y):
            for column in range(self.count_blok_x):
                if (row + column) % 2 == 0:
                    color = Map.GREEN
                else:
                    color = Map.GREEN_DARK
                self.draw_blok(color, column, row, win)
                if self.matrix[column][row] == 'stone':
                    color = Map.BLACK
                    self.draw_blok(color, column, row, win)

    def update(self, win):
        pass


class Ant(pygame.sprite.Sprite):
    def __init__(self, x, y, map, x_exit, y_exit):
        super().__init__()
        self.x = x
        self.y = y
        self.x_exit = x_exit
        self.y_exit = y_exit
        self.speed = 1
        self.run = True
        self.image = ant_im
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.map = map
        self.barriers = ['stone']
        self.map.matrix[self.x][self.y] += ' ant'
        self.restricted_blocks = []
        self.radius_to_patrol = 5
        self.amount_of_blocks_to_patrol = 0
        self.direction_to_patrol = up

    def draw_ant(self, column, row, win):
        win.blit(self.image, (column * self.map.size_block, row * self.map.size_block))

    def find_distance_to_home(self, coordinate):
        return math.sqrt((coordinate[0] - self.x_exit) ** 2 + (coordinate[1] - self.y_exit) ** 2)

    def save_to_restricted_blocks(self):
        if len(self.restricted_blocks) <= 10:
            self.restricted_blocks.append([self.x, self.y])
        else:
            self.restricted_blocks.pop(0)

    def to_patrol(self):

        if self.amount_of_blocks_to_patrol == 0:
            temp_direction_to_patrol = right
            if not (temp_direction_to_patrol[0] == self.direction_to_patrol[0] * -1 and temp_direction_to_patrol[1] ==
                    self.direction_to_patrol[1] * -1):
                self.direction_to_patrol = temp_direction_to_patrol.copy()

            self.amount_of_blocks_to_patrol = random.randint(3, 7)
        if ((self.x_exit + self.radius_to_patrol) > self.x + self.direction_to_patrol[0] > (
                self.x_exit - self.radius_to_patrol)) \
                and ((self.y_exit + self.radius_to_patrol) > self.y + self.direction_to_patrol[1] > (
                self.y_exit - self.radius_to_patrol)):
            self.move(self.direction_to_patrol)
        else:
            list_direction_to_patrol = [right, right_up, right_down,
                                        left, left_up, left_down, up, down]

            if self.direction_to_patrol == right:
                list_direction_to_patrol = list(filter(filter_by_right, list_direction_to_patrol))
                self.direction_to_patrol = random.choice(list_direction_to_patrol)

            elif self.direction_to_patrol == left:
                list_direction_to_patrol = list(filter(filter_by_left, list_direction_to_patrol))
                self.direction_to_patrol = random.choice(list_direction_to_patrol)

            elif self.direction_to_patrol == up:
                list_direction_to_patrol = list(filter(filter_by_up, list_direction_to_patrol))
                self.direction_to_patrol = random.choice(list_direction_to_patrol)

            elif self.direction_to_patrol == down:
                list_direction_to_patrol = list(filter(filter_by_down, list_direction_to_patrol))
                self.direction_to_patrol = random.choice(list_direction_to_patrol)

        self.amount_of_blocks_to_patrol -= 1

    def find_home(self):
        # distance_to_home = self.find_distance_to_home([self.x, self.y])
        distances = {}
        directions = {}
        to_left = [self.x - 1, self.y]
        to_right = [self.x + 1, self.y]
        to_up = [self.x, self.y - 1]
        to_down = [self.x, self.y + 1]
        to_left_up = [self.x - 1, self.y - 1]
        to_left_down = [self.x - 1, self.y + 1]
        to_right_up = [self.x + 1, self.y - 1]
        to_right_down = [self.x + 1, self.y + 1]
        if to_left not in self.restricted_blocks:
            directions.update({'to_left': to_left})
        if to_left_up not in self.restricted_blocks:
            directions.update({'to_left_up': to_left_up})
        if to_left_down not in self.restricted_blocks:
            directions.update({'to_left_down': to_left_down})
        if to_right not in self.restricted_blocks:
            directions.update({'to_right': to_right})
        if to_right_up not in self.restricted_blocks:
            directions.update({'to_right_up': to_right_up})
        if to_right_down not in self.restricted_blocks:
            directions.update({'to_right_down': to_right_down})
        if to_up not in self.restricted_blocks:
            directions.update({'to_up': to_up})
        if to_down not in self.restricted_blocks:
            directions.update({'to_down': to_down})

        for direction in directions:
            if self.map.matrix[directions[direction][0]][directions[direction][1]] in self.barriers:
                direction = None
            else:
                distance = self.find_distance_to_home(directions[direction])
                distances.update({direction: distance})

        try:
            min_distance = min(distances, key=distances.get)
        except ValueError:
            self.restricted_blocks.clear()
            min_distance = ''

        self.save_to_restricted_blocks()
        print(self.restricted_blocks)

        if self.map.matrix[self.x][self.y].find('exit') != -1:
            pass
        elif min_distance == 'to_left':
            self.move(left)
        elif min_distance == 'to_left_up':
            self.move(left_up)
        elif min_distance == 'to_left_down':
            self.move(left_down)
        elif min_distance == 'to_right_up':
            self.move(right_up)
        elif min_distance == 'to_right':
            self.move(right)
        elif min_distance == 'to_right_down':
            self.move(right_down)
        elif min_distance == 'to_up':
            self.move(up)
        elif min_distance == 'to_down':
            self.move(down)

    def move(self, direction):
        self.run = True

        if direction[0] == 1 and self.x >= self.map.count_blok_x - 2:
            self.run = False

        if direction[0] == -1 and self.x <= 0:
            self.run = False

        if direction[1] == -1 and self.y <= 0:
            self.run = False

        if direction[1] == 1 and self.y >= self.map.count_blok_y - 2:
            self.run = False

        if self.map.matrix[self.x + direction[0]][self.y + direction[1]] in self.barriers:
            self.run = False
        elif self.run:
            self.map.matrix[self.x + direction[0]][self.y + direction[1]] += ' ant'
            lis = self.map.matrix[self.x][self.y].split()
            lis.remove('ant')
            self.map.matrix[self.x][self.y] = ' '.join(lis)

        if self.run:
            self.x += direction[0] * self.speed
            self.y += direction[1] * self.speed

    def update(self, win):
        table = PrettyTable()
        self.draw_ant(self.x, self.y, win)
        table.add_column('||', range(len(self.map.matrix[0])))
        for x in range(len(self.map.matrix)):
            table.add_column(str(x), self.map.matrix[x])
        # print(table)


class Ant_ranger(Ant):
    pass


class Ant_labor(Ant):
    pass


class Ant_defender(Ant):
    pass


class Ant_loader(Ant):
    pass
