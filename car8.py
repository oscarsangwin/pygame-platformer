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

obstacles = [
    pg.Rect(0, HEIGHT-100, int(WIDTH/2)-30, 30),
    pg.Rect(int(WIDTH/2)+30, HEIGHT-200, int(WIDTH/2)-30, 30),
    pg.Rect(0, HEIGHT-300, int(WIDTH/2)-30, 30),
    pg.Rect(int(WIDTH/2)+30, HEIGHT-400, int(WIDTH/2)-30, 30)
] 

def update_screen():
    screen.fill(WHITE)
    for obstacle in obstacles:
        pg.draw.rect(screen, GREEN, obstacle)
    myPlayer.draw()
    draw_text(f'Fps: {fps}', WIDTH-75, 7)
    pg.display.update()

def draw_text(text, x, y):
    textsurface = myfont.render(text, True, (0, 0, 0))
    screen.blit(textsurface, (x, y))

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
        for obstacle in obstacles:
            if self.rect.colliderect(obstacle):
                return True
        if self.touching_left() or self.touching_right() or self.touching_roof():
            return True

        return False

    def update_location(self):
        self.rect.center = self.x, self.y

    def touching_floor(self):
        if self.y + (self.PLAYER_HEIGHT/2) > HEIGHT:
            return True
        else:
            return False
            
    def touching_left(self):
        if self.x - (self.PLAYER_WIDTH/2) < 0:
            return True
        else:
            return False

    def touching_right(self):
        if self.x + (self.PLAYER_WIDTH/2) > WIDTH:
            return True
        else:
            return False

    def touching_roof(self):
        if self.y - (self.PLAYER_HEIGHT/2) < 0:
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

        # CHECK IF TOUCHING A SURFACE (for debugging)
        if self.check_collision():
            print('this is bad')
        else:
            pass

pg.init()
pg.display.set_caption('Platformer 8')
screen = pg.display.set_mode([WIDTH, HEIGHT])

print('Loading fonts... (this may take a few seconds)')
pg.font.init()
myfont = pg.font.SysFont(None, 30)
print('...Done!')

clock = pg.time.Clock()

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

    # CLOCK EVENTS
    fps = str(int(clock.get_fps())) # Get the frames per second
    clock.tick(62) # Set max fps to 62

    # RENDER SCREEN
    update_screen()
pg.quit()