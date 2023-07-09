import pygame


class Image:
    all = []

    def __init__(self, surface, name, img, blit_cord_x, blit_cord_y, is_visible=True, can_grow=True):

        self.surface = surface
        self.name = name

        self.img = img
        self.img_height = img.get_height()
        self.img_width = img.get_height()

        self.x = blit_cord_x
        self.y = blit_cord_y

        self.is_visible = is_visible

        # constants, DO NOT TOUCH ANYWHERE IN THE CODE:
        self.img_prime = img
        self.prime_x = blit_cord_x
        self.prime_y = blit_cord_y

        self.is_highlited = True
        self.can_grow = can_grow

        self.grow_scaler = 1

        Image.all.append(self)

    def __repr__(self):
        return f"Name: {self.name}, X cord: {self.x}, Y cord: {self.y}, Visible: {self.is_visible}"

    def replace_img(self, new_img):
        self.img = new_img

    def draw(self):
        if self.is_visible:
            self.surface.blit(self.img, (self.x, self.y))

    def bloat(self):
        if self.is_visible:
            if self.is_highlited and self.can_grow and self.grow_scaler < 1.15:
                self.grow_scaler = self.grow_scaler + 0.0025
                self.x = self.x - 0.0004 * self.img_width
                self.y = self.y - 0.0004 * self.img_height
            elif (self.is_highlited == False or self.can_grow == False) and self.grow_scaler > 1:
                self.grow_scaler = self.grow_scaler - 0.0025
                self.x = self.x + 0.0004 * self.img_width
                self.y = self.y + 0.0004 * self.img_height
            self.img = pygame.transform.rotozoom(self.img_prime, 0, self.grow_scaler)

    def mouse_check(self, mouse_pos):
        if (self.prime_x+self.img_width > mouse_pos[0] >= self.prime_x) and (self.prime_y+self.img_height > mouse_pos[1] >= self.prime_y):
            self.is_highlited = True
        else:
            self.is_highlited = False

    @classmethod
    def name_draw(cls, name):
        for img in cls.all:
            if img.name == name:
                img.draw()

    @classmethod
    def perform_mouse_check(cls):
        mouse_pos = pygame.mouse.get_pos()
        for img in cls.all:
            img.mouse_check(mouse_pos)

    @classmethod
    def perform_bloating(cls):
        for img in cls.all:
            img.bloat()

