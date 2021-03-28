# PYGAME PLATFOMER v10
# by Oscar Sangwin, 2021

# Import modules
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame as pg
import time
import json
import sys

# Define platfomer dimensions
WIDTH = 700
HEIGHT = 500

# Define colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 220, 0)
BLUE = (0, 0, 255)
YELLOW = (252, 187, 64)
PURPLE = (252, 40, 252)

# Key values are set to false (off)
up_key = False
down_key = False
left_key = False
right_key = False

reset_key = False
back_key = False
skip_key = False

# Level can be pre-set to an alternate value, but 0 is standard
level = 0
tot_levels = 0

# Fetch obstacles from JSON DATA
def load_obstacles(json_level=0, json_path='./Levels/simple-test.json'):
    # Get data from file
    try:
        with open(json_path, 'r') as f:
            game_data = json.load(f)
    except json.decoder.JSONDecodeError as e:
        print(f'Something may have gone wrong: {e}')
        return

    global tot_levels
    tot_levels = len(game_data['levels'])

    global obstacles, goals, kills, texts, bounces, collision_group
    obstacles = []
    collision_group = []
    goals = []
    kills = []
    texts = []
    bounces = []

    try:
        # Load collision group
        for json_obstacle in game_data['levels'][json_level]['obstacles']:
            if json_obstacle['type'] == 'block':
                try:
                    if json_obstacle['collide'] == False:
                        continue
                except:
                    pass

                collision_group.append(pg.Rect(
                    int(json_obstacle['x']),
                    int(json_obstacle['y']),
                    int(json_obstacle['width']),
                    int(json_obstacle['height'])
                ))
            elif json_obstacle['type'] in ['bounce', 'goal', 'kill']:
                try:
                    if json_obstacle['collide'] == True:
                        collision_group.append(pg.Rect(
                            int(json_obstacle['x']),
                            int(json_obstacle['y']),
                            int(json_obstacle['width']),
                            int(json_obstacle['height'])
                        ))
                except:
                    pass

        # Load individual obstacle groups
        for json_obstacle in game_data['levels'][json_level]['obstacles']:
            if json_obstacle['type'] == 'block':
                obstacle = pg.Rect(int(json_obstacle['x']),
                                int(json_obstacle['y']),
                                int(json_obstacle['width']),
                                int(json_obstacle['height'])
                )
                obstacles.append(obstacle)
            elif json_obstacle['type'] == 'goal':
                goal = pg.Rect(int(json_obstacle['x']),
                                int(json_obstacle['y']),
                                int(json_obstacle['width']),
                                int(json_obstacle['height'])
                )
                goals.append(goal)
            elif json_obstacle['type'] == 'kill':
                kill = pg.Rect(int(json_obstacle['x']),
                                int(json_obstacle['y']),
                                int(json_obstacle['width']),
                                int(json_obstacle['height'])
                )
                kills.append(kill)
            elif json_obstacle['type'] == 'bounce':
                bounce = pg.Rect(int(json_obstacle['x']),
                                int(json_obstacle['y']),
                                int(json_obstacle['width']),
                                int(json_obstacle['height'])
                )
                bounces.append(bounce)
            elif json_obstacle['type'] == 'text':
                
                try:
                    if json_obstacle['size'] == 'large':
                        large = True
                    else:
                        large = False
                except KeyError:
                    large = False
                
                text = (
                    int(json_obstacle['x']),
                    int(json_obstacle['y']),
                    json_obstacle['value'],
                    large
                )
                texts.append(text)

        # Get spawn coords
        global spawn
        try:
            spawn = game_data['levels'][json_level]['options']['spawn']
        except KeyError:
            spawn = None

    except KeyError as e:
        print('There was an error parsing the JSON level. The file may be invalid.')
        print(f'KeyError message: {e}')
        sys.exit()

# Load the initial level
load_obstacles(json_level=level)

# Render the obstacles, player, etc on pygame window
def update_screen():

    # First, background fill
    screen.fill(WHITE)

    # Background 'geometry dash' image
    screen.blit(background_img, (0, 0))
    for text in texts:
        if text[3]:
            draw_title(text[2], text[0], text[1])
        else:
            draw_text(text[2], text[0], text[1])
        
    # Red
    for kill in kills:
        pg.draw.rect(screen, RED, kill)
    
    # Purple
    for bounce in bounces:
        pg.draw.rect(screen, PURPLE, bounce)

    # Green
    for obstacle in obstacles:
        pg.draw.rect(screen, GREEN, obstacle)

    # Yellow
    for goal in goals:
        pg.draw.rect(screen, YELLOW, goal)
    
    # Draw player
    myPlayer.draw()

    # Level info and FPS
    draw_text(f'Level: {level+1} of {tot_levels}', 7, 7)
    draw_text(f'Fps: {fps}', WIDTH-75, 7)

    # Update screen
    pg.display.update()

# Draws standard sized text on screen
def draw_text(text, x, y):
    textsurface = myfont.render(text, True, WHITE)
    screen.blit(textsurface, (x, y))

# Draws large text on screen
def draw_title(text, x, y):
    textsurface = mylargefont.render(text, True, WHITE)
    screen.blit(textsurface, (x, y))

# Player class, kept throught the whole game
class Player():

    # Load initial variables and set positions
    def __init__(self, spawn=None, color=BLUE):
        self.PLAYER_WIDTH = 30
        self.PLAYER_HEIGHT = 30

        self.color = color

        self.x_vel = 0
        self.y_vel = 0

        self.max_vel = 12

        self.friction = 0.85
        self.power = 8

        self.jump_power = 15
        self.gravity = -0.95

        self.rect = pg.Rect(0, 0, self.PLAYER_WIDTH, self.PLAYER_HEIGHT)

        if spawn:
            self.x, self.y = spawn
        else:
            self.x = int(WIDTH / 2)
            self.y = int(self.PLAYER_HEIGHT + 10)

        self.spawn = self.x, self.y

        self.update_location()

        self.on_new_level = False

    # Draws player on screen
    def draw(self):
            pg.draw.rect(screen, self.color, self.rect)
    
    # Checks if colliding with an object group
    # Default group is the collision group
    def check_collision(self, obj_group=None): # Returns True if touching obstacle

        if obj_group == None:
            obj_group = collision_group

        for obstacle in obj_group:
            if self.rect.colliderect(obstacle):
                return True
        if self.touching_left() or self.touching_right() or self.touching_roof():
            return True

        return False

    # Move the character square position to the player coords
    def update_location(self):
        self.rect.center = self.x, self.y

    # Check if touching bottom side
    def touching_floor(self):
        if self.y + (self.PLAYER_HEIGHT/2) > HEIGHT:
            return True
        else:
            return False

    # Check if touching left side    
    def touching_left(self):
        if self.x - (self.PLAYER_WIDTH/2) < 0:
            return True
        else:
            return False

    # Check if touching right side
    def touching_right(self):
        if self.x + (self.PLAYER_WIDTH/2) > WIDTH:
            return True
        else:
            return False

    # Check if touching top side
    def touching_roof(self):
        if self.y - (self.PLAYER_HEIGHT/2) < 0:
            return True
        else:
            return False

    # Move player to desired coords, but stop
    # if about to hit a collision object. Will
    # travel along the Y axis, then X.
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

    # Set player position to spawn coords
    def respawn(self):
        self.x, self.y = self.spawn

    # Change the spawn coords to new location
    def update_spawn(self, new_spawn):
        self.spawn = new_spawn

    # Call once per game cycle, moves player to next
    # position, fed by user input parameters
    def next_move(self, up, down, left, right, reset, back, skip):
        global level

        # Respawn character if it is a new loop on a new level
        if self.on_new_level:
            self.respawn()
            self.on_new_level = False

        # Gravity
        self.y_vel -= self.gravity

        if self.y_vel > self.max_vel:
            self.y_vel = self.max_vel

        # Jumping
        self.y += 1
        self.update_location()
        if up and (self.check_collision() or self.touching_floor()):
            self.y_vel = -self.jump_power
        self.y -= 1

        # X axis friction
        self.x_vel = self.x_vel * self.friction

        # Left and right keys
        if left and not right:
            self.x_vel = -self.power
        elif right and not left:
            self.x_vel = self.power

        if reset:
            self.respawn()
        
        if back:
            if level > 0:
                level -= 1
                self.on_new_level = True
                self.respawn()
        
        if skip:
            if level+1 < tot_levels:
                level += 1
                self.on_new_level = True
                self.respawn()

        # Move by player velocitites
        myPlayer.step(int(self.x_vel), int(self.y_vel))

        # Add a level floor
        if self.touching_floor():
            self.y = int(HEIGHT - (self.PLAYER_HEIGHT/2))
            self.update_location()

        # Check if touching surface 
        # (for debugging only, as this should never run)
        if self.check_collision():
            print('this is bad')

        # Check if on red
        if self.check_collision(obj_group=kills):
            self.respawn()

        # Check if on purple
        if self.check_collision(obj_group=bounces):
            self.y_vel = -self.jump_power*1.5

        # Check if on yellow
        if self.check_collision(obj_group=goals):
            level += 1
            if level >= tot_levels:
                print('GAME COMPLETE')
                print(f'You completed level: {level} of {tot_levels}!!! Yay!')
                sys.exit()
            else:
                self.on_new_level = True


# Load screen
print('Loading screen...')
pg.init()
pg.display.set_caption('Platformer v11')
screen = pg.display.set_mode([WIDTH, HEIGHT])
print('...Done!')

# Load music
print('Loading music...')
music_file = './Sounds/starlight.wav'
pg.mixer.music.load(music_file)
print('...Done!')

# Load fonts
print('Loading fonts... (this may take a few seconds)')
pg.font.init()
myfont = pg.font.SysFont('microsoftsansserifttf', 20)
mylargefont = pg.font.SysFont('microsoftsansserifttf', 30)
print('...Done!')

# Load images
print('Loading images...')
background_img = pg.image.load('./Images/geometric.jpeg')
background_img = pg.transform.scale(background_img, (WIDTH, HEIGHT))
print('...Done!')

# Create pygame clock, for FPS management
clock = pg.time.Clock()

# Create instance of Player object
myPlayer = Player(color=WHITE, spawn=spawn)

# Start music
pg.mixer.music.play(-1)

# GAME LOOP
running = True
while running:

    # Get the level obstacles and update player spawn
    load_obstacles(json_level=level)
    myPlayer.update_spawn(spawn)

    # Process inputs:
        # Arrow keys:
            # Up
            # Down
            # Left
            # Right 
        # Window 'x' button 
        # 'r' for reset / respawn,
        # 'g' for get mouse coords
        # 'b' to go back a level
        # 's' to skip a level
    reset_key = False
    back_key = False
    skip_key = False
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
            elif e.key == pg.K_r:
                reset_key = True
            elif e.key == pg.K_g:
                print(pg.mouse.get_pos())
            elif e.key == pg.K_b:
                back_key = True
            elif e.key == pg.K_s:
                skip_key = True

        elif e.type == pg.KEYUP:
            if e.key == pg.K_LEFT:
                left_key = False
            elif e.key == pg.K_RIGHT:
                right_key = False
            elif e.key == pg.K_DOWN:
                down_key = False
            elif e.key == pg.K_UP:
                up_key = False

    # Handle events: update the player
    myPlayer.next_move(up_key, down_key, left_key, right_key, reset_key, back_key, skip_key)

    # Clock events
    fps = str(int(clock.get_fps())) # Get the frames per second
    clock.tick(60) # Set max fps to 60

    # Update screen
    update_screen()

# Quit pygame
pg.quit()