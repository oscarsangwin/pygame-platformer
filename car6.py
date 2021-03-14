import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame as pg
import time

WIDTH = 700
HEIGHT = 500

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 220, 0)
BLUE = (0, 0, 255)

up_key = False
down_key = False
left_key = False
right_key = False

obstacle = pg.Rect(int(WIDTH/4), HEIGHT-100, int(WIDTH/2), 30) # height was 30, 

def update_screen():
    screen.fill(WHITE)
    pg.draw.rect(screen, GREEN, obstacle)
    myPlayer.draw()
    pg.display.update()

class Player():
    def __init__(self, color=BLUE):
        self.PLAYER_WIDTH = 30
        self.PLAYER_HEIGHT = 30

        self.color = color

        self.x_vel = 0
        self.y_vel = 0

        self.max_vel = 12

        self.friction = 0.85
        self.power = 8

        self.jump_power = 27
        self.gravity = -0.95

        self.rect = pg.Rect(0, 0, self.PLAYER_WIDTH, self.PLAYER_HEIGHT)

        self.x = int(WIDTH / 2)
        self.y = int(self.PLAYER_HEIGHT + 10)

        self.update_location()

    def draw(self):
            pg.draw.rect(screen, self.color, self.rect)
    
    def check_collision(self): # Returns True if touching obstacle
        if self.rect.colliderect(obstacle):
            return True
        else:
            return False

    def update_location(self):
        self.rect.center = self.x, self.y

    def touching_floor(self):
        if self.y + (self.PLAYER_HEIGHT/2) > HEIGHT:
            return True
        else:
            return False

    def step(self, change_x, change_y):
        if change_y > 0:
            for _ in range(change_y):
                self.y += 1
                self.update_location()
                if self.check_collision():
                    self.y -= 1
                    self.update_location()
                    # print('reached a wall, stepped back one and still touching') if self.check_collision() else print('reached a wall, stepped back one and not touching any more')
                    break
        elif change_y < 0:
            for _ in range(-change_y):
                self.y -= 1
                self.update_location()
                if self.check_collision():
                    self.y += 1
                    self.update_location()
                    # print('reached a wall, stepped back one and still touching') if self.check_collision() else print('reached a wall, stepped back one and not touching any more')
                    self.y_vel = 0
                    break

        if change_x > 0:
            for _ in range(change_x):
                self.x += 1
                self.update_location()
                if self.check_collision():
                    self.x -= 1
                    self.update_location()
                    # print('reached a wall, stepped back one and still touching') if self.check_collision() else print('reached a wall, stepped back one and not touching any more')
                    break
        elif change_x < 0:
            for _ in range(-change_x):
                self.x -= 1
                self.update_location()
                if self.check_collision():
                    self.x += 1
                    self.update_location()
                    # print('reached a wall, stepped back one and still touching') if self.check_collision() else print('reached a wall, stepped back one and not touching any more')
                    break

    def next_move(self, up, down, left, right):

        # GRAVITY
        self.y_vel -= self.gravity
        if self.y_vel > self.max_vel:
            self.y_vel = self.max_vel

        # JUMPING
        self.y += 1
        self.update_location()
        if up and (self.check_collision() or self.touching_floor()):
            self.y_vel -= self.jump_power
        self.y -= 1

        # X AXIS FRICTION
        self.x_vel = self.x_vel * self.friction

        # LEFT AND RIGHT KEYS
        if left and not right:
            self.x_vel = -self.power
        elif right and not left:
            self.x_vel = self.power

        # MOVE BY PLAYER VELOCITIES
        myPlayer.step(int(self.x_vel), int(self.y_vel))

        # ADD A FLOOR (temporary)
        if self.touching_floor():
            self.y = int(HEIGHT - (self.PLAYER_HEIGHT/2))
            self.update_location()

        # CHECK IF TOUCHING A SURFACE (for debuggings)
        if self.check_collision():
            print('this is bad')
        else:
            pass

pg.init()
pg.display.set_caption('Platformer 6')
screen = pg.display.set_mode([WIDTH, HEIGHT])

myPlayer = Player()

running = True
while running:

    # PROCESS INPUTS
    for e in pg.event.get():
        if e.type == pg.QUIT:
            running = False

        elif e.type == pg.KEYDOWN:
            if e.key == pg.K_LEFT:
                left_key = True
            elif e.key == pg.K_RIGHT:
                right_key = True
            elif e.key == pg.K_DOWN:
                down_key = True
            elif e.key == pg.K_UP:
                up_key = True

        elif e.type == pg.KEYUP:
            if e.key == pg.K_LEFT:
                left_key = False
            elif e.key == pg.K_RIGHT:
                right_key = False
            elif e.key == pg.K_DOWN:
                down_key = False
            elif e.key == pg.K_UP:
                up_key = False

    # HANDLE EVENTS
    myPlayer.next_move(up_key, down_key, left_key, right_key)

    # RENDER SCREEN
    update_screen()
pg.quit()