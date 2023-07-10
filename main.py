import pygame
from pygame.locals import *

import time

import pg
import mswpr

flags = DOUBLEBUF
screen = pygame.display.set_mode((300, 343), flags)

field_x = 9
field_y = 9
total_bombs = 10

def load():
    global a0, a1, a2, a3, a4, a5, a6, a7, a8, s0, s1, s2, s3, s4, s5, s6, s7, s8, s9, hidden, bomb
    a0 = pygame.image.load("assets/0.png").convert()
    a1 = pygame.image.load("assets/1.png").convert()
    a2 = pygame.image.load("assets/2.png").convert()
    a3 = pygame.image.load("assets/3.png").convert()
    a4 = pygame.image.load("assets/4.png").convert()
    a5 = pygame.image.load("assets/5.png").convert()
    a6 = pygame.image.load("assets/6.png").convert()
    a7 = pygame.image.load("assets/7.png").convert()
    a8 = pygame.image.load("assets/8.png").convert()

    s0 = pygame.image.load("assets/s0.png").convert()
    s1 = pygame.image.load("assets/s1.png").convert()
    s2 = pygame.image.load("assets/s2.png").convert()
    s3 = pygame.image.load("assets/s3.png").convert()
    s4 = pygame.image.load("assets/s4.png").convert()
    s5 = pygame.image.load("assets/s5.png").convert()
    s6 = pygame.image.load("assets/s6.png").convert()
    s7 = pygame.image.load("assets/s7.png").convert()
    s8 = pygame.image.load("assets/s8.png").convert()
    s9 = pygame.image.load("assets/s9.png").convert()

    hidden = pygame.image.load("assets/facingDown.png")
    bomb = pygame.image.load("assets/bomb.png")


def fill(arr, x_size, y_size, image, name, can_grow):
    global screen

    x = 6
    y = 48
    while len(arr) != (x_size * y_size):
        arr.append(pg.Image(screen, name, image, x, y, True, can_grow))
        x = x + 32
        if x == 6 + x_size * 32:
            x = 6
            y = y + 32
def get_cord(arr, x_size, y_size):
    i=0
    success = False
    while i < x_size * y_size:
        if arr[i].is_visible and arr[i].is_highlited:
            success = True
            break
        i = i + 1

    if success:
        return i
    else:
        return 2137
        #yes im using the funny pope number as the error handler



if __name__ == '__main__':

    load()
    running = True

    set_up = False

    covered = []
    fill(covered, field_x, field_y, hidden, "covered", True)


    t0 = time.time()
    while running:
        screen.fill((128, 128, 128))

        t1 = (time.time() - t0)
        tint = int(t1)

        mouse_pos = pygame.mouse.get_pos()

        pg.Image.perform_mouse_check()
        pg.Image.perform_bloating()

        if set_up:
            pg.Image.name_draw("uncovered")
        pg.Image.name_draw("covered")

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.WINDOWCLOSE:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:

                    cord = get_cord(covered, field_x, field_y)

                    if set_up == False:
                        field = mswpr.setup(screen, cord, field_x, field_y, total_bombs)
                        set_up = True
                    if 0 <= cord < field_x*field_y:
                        mswpr.uncover(cord, covered, field, field_x, field_y, total_bombs)


        pygame.display.flip()
