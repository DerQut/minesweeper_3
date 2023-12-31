import pg

import random
import pygame
import time


def load_local():

    global a0, a1, a2, a3, a4, a5, a6, a7, a8, bomb

    a0 = pygame.image.load("assets/0.png").convert()
    a1 = pygame.image.load("assets/1.png").convert()
    a2 = pygame.image.load("assets/2.png").convert()
    a3 = pygame.image.load("assets/3.png").convert()
    a4 = pygame.image.load("assets/4.png").convert()
    a5 = pygame.image.load("assets/5.png").convert()
    a6 = pygame.image.load("assets/6.png").convert()
    a7 = pygame.image.load("assets/7.png").convert()
    a8 = pygame.image.load("assets/8.png").convert()

    bomb = pygame.image.load("assets/bomb.png")


def setup(surface, cord, size_x, size_y, bombs, covered):

    load_local()

    i = 0
    arr = []
    field = []

    images = [a0, a1, a2, a3, a4, a5, a6, a7, a8, bomb]

    while i < size_x*size_y:
        arr.append(0)
        i = i + 1

    i = 0
    while i < bombs:
        a = random.randint(0, size_x*size_y-1)
        if arr[a] != 9 and a != cord:
            arr[a] = 9

            #up
            if a >= size_x:
                if arr[a-size_x] != 9:
                    arr[a-size_x] = arr[a-size_x] + 1

            #down
            if a < size_x*(size_y-1):
                if arr[a+size_x] != 9:
                    arr[a+size_x] = arr[a+size_x] + 1

            #left
            if a % size_x != 0:
                if arr[a-1] != 9:
                    arr[a-1] = arr[a-1] + 1

            #right
            if (a+1) % size_x != 0:
                if arr[a+1] != 9:
                    arr[a+1] = arr[a+1] + 1

            #up right
            if a >= size_x and (a+1) % size_x != 0:
                if arr[a-size_x+1] != 9:
                    arr[a-size_x+1] = arr[a-size_x+1]+1

            #up left
            if a >= size_x and a%size_x != 0:
                if arr[a-size_x-1] != 9:
                    arr[a-size_x-1] = arr[a-size_x-1]+1

            #down right
            if a < size_x*(size_y-1) and (a+1) % size_x != 0:
                if arr[a+size_x+1] != 9:
                    arr[a+size_x+1] = arr[a+size_x+1]+1

            #down left
            if a < size_x*(size_y-1) and a % size_x != 0:
                if arr[a+size_x-1] != 9:
                    arr[a+size_x-1] = arr[a+size_x-1]+1
            i = i + 1


    x = 6
    y = 44
    i = 0
    while i < size_x*size_y:
        field.append(pg.Image(surface, "uncovered", images[arr[i]], x, y, True, False))

        field[i].value = arr[i]

        field[i].is_right_edge = True
        field[i].is_left_edge = True
        field[i].is_upper_edge = True
        field[i].is_lower_edge = True

        field[i].flags_around = 0

        covered[i].is_flagged = False

        if i >= size_x:
            field[i].is_upper_edge = False
        if i < size_x*(size_y-1):
            field[i].is_lower_edge = False
        if i % size_x != 0:
            field[i].is_left_edge = False
        if (i+1) % size_x != 0:
            field[i].is_right_edge = False

        i = i + 1

        x = x + 32
        if x == 6 + size_x * 32:
            x = 6
            y = y + 32

    return field


def uncover(cord, covered, field, size_x):

    if cord != 2137 and not covered[cord].is_flagged:

        covered[cord].is_visible = False

        if field[cord].value == 0:

            #up
            if not field[cord].is_upper_edge:
                if covered[cord - size_x].is_visible and not covered[cord-size_x].is_flagged:
                    uncover(cord - size_x, covered, field, size_x)

            #down
            if not field[cord].is_lower_edge:
                if covered[cord + size_x].is_visible and not covered[cord + size_x].is_flagged:
                    uncover(cord + size_x, covered, field, size_x)

            #left
            if not field[cord].is_left_edge:
                if covered[cord - 1].is_visible and not covered[cord - 1].is_flagged:
                    uncover(cord - 1, covered, field, size_x)

            #right
            if not field[cord].is_right_edge:
                if covered[cord + 1].is_visible and not covered[cord + 1].is_flagged:
                    uncover(cord + 1, covered, field, size_x)

            #up right
            if (not field[cord].is_right_edge) and (not field[cord].is_upper_edge):
                if covered[cord - size_x + 1].is_visible and not covered[cord - size_x + 1].is_flagged:
                    uncover(cord - size_x + 1, covered, field, size_x)

            #up left
            if (not field[cord].is_left_edge) and (not field[cord].is_upper_edge):
                if covered[cord - size_x - 1].is_visible and not covered[cord - size_x - 1].is_flagged:
                    uncover(cord - size_x - 1, covered, field, size_x)

            #down right
            if (not field[cord].is_right_edge) and (not field[cord].is_lower_edge):
                if covered[cord + size_x + 1].is_visible and not covered[cord + size_x + 1].is_flagged:
                    uncover(cord + size_x + 1, covered, field, size_x)

            #down left
            if (not field[cord].is_left_edge) and (not field[cord].is_lower_edge):
                if covered[cord + size_x - 1].is_visible and not covered[cord + size_x - 1].is_flagged:
                    uncover(cord + size_x - 1, covered, field, size_x)



        elif field[cord].value == 9:
            print("ODKRYŁEM BOMBE")

def flag(cord, covered, flags, field, size_x):
    if cord != 2137:
        if not covered[cord].is_flagged and covered[cord].is_visible:
            covered[cord].is_flagged = True
            covered[cord].can_grow = False
            flags[cord].is_visible = True

            if not field[cord].is_left_edge:
                field[cord-1].flags_around = field[cord-1].flags_around + 1
            if not field[cord].is_right_edge:
                field[cord+1].flags_around = field[cord+1].flags_around + 1
            if not field[cord].is_lower_edge:
                field[cord+size_x].flags_around = field[cord+size_x].flags_around + 1
            if not field[cord].is_upper_edge:
                field[cord-size_x].flags_around = field[cord-size_x].flags_around + 1

            if (not field[cord].is_left_edge) and (not field[cord].is_upper_edge):
                field[cord-1-size_x].flags_around = field[cord-1-size_x].flags_around + 1
            if (not field[cord].is_left_edge) and (not field[cord].is_lower_edge):
                field[cord-1+size_x].flags_around = field[cord-1+size_x].flags_around + 1
            if (not field[cord].is_right_edge) and (not field[cord].is_upper_edge):
                field[cord+1-size_x].flags_around = field[cord+1-size_x].flags_around + 1
            if (not field[cord].is_right_edge) and (not field[cord].is_lower_edge):
                field[cord+1+size_x].flags_around = field[cord+1+size_x].flags_around + 1

        else:
            covered[cord].is_flagged = False
            covered[cord].can_grow = True
            flags[cord].is_visible = False

            if not field[cord].is_left_edge:
                field[cord - 1].flags_around = field[cord - 1].flags_around - 1
            if not field[cord].is_right_edge:
                field[cord + 1].flags_around = field[cord + 1].flags_around - 1
            if not field[cord].is_lower_edge:
                field[cord + size_x].flags_around = field[cord + size_x].flags_around - 1
            if not field[cord].is_upper_edge:
                field[cord - size_x].flags_around = field[cord - size_x].flags_around - 1

            if (not field[cord].is_left_edge) and (not field[cord].is_upper_edge):
                field[cord - 1 - size_x].flags_around = field[cord - 1 - size_x].flags_around - 1
            if (not field[cord].is_left_edge) and (not field[cord].is_lower_edge):
                field[cord - 1 + size_x].flags_around = field[cord - 1 + size_x].flags_around - 1
            if (not field[cord].is_right_edge) and (not field[cord].is_upper_edge):
                field[cord + 1 - size_x].flags_around = field[cord + 1 - size_x].flags_around - 1
            if (not field[cord].is_right_edge) and (not field[cord].is_lower_edge):
                field[cord + 1 + size_x].flags_around = field[cord + 1 + size_x].flags_around - 1

def advanced_uncover(cord, field, covered, size_x):
    if cord < 2137 and field[cord].value != 0:
        if field[cord].value == field[cord].flags_around:
            if not field[cord].is_left_edge:
                uncover(cord-1, covered, field, size_x)
            if not field[cord].is_right_edge:
                uncover(cord+1, covered, field, size_x)
            if not field[cord].is_lower_edge:
                uncover(cord+size_x, covered, field, size_x)
            if not field[cord].is_upper_edge:
                uncover(cord-size_x, covered, field, size_x)

            if (not field[cord].is_left_edge) and (not field[cord].is_upper_edge):
                uncover(cord-1-size_x, covered, field, size_x)
            if (not field[cord].is_left_edge) and (not field[cord].is_lower_edge):
                uncover(cord-1+size_x, covered, field, size_x)
            if (not field[cord].is_right_edge) and (not field[cord].is_upper_edge):
                uncover(cord+1-size_x, covered, field, size_x)
            if (not field[cord].is_right_edge) and (not field[cord].is_lower_edge):
                uncover(cord+1+size_x, covered, field, size_x)

