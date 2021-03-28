import pygame as pg

WIDTH = 700
HEIGHT = 500

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255,0)
BLUE = (0, 0, 255)

up_key = False
down_key = False
left_key = False
right_key = False

CAR_WIDTH = 30
CAR_HEIGHT = 30

car_x = WIDTH / 2
car_y = HEIGHT / 2

car_x_vel = 0
car_y_vel = 0

max_vel = 10

friction = 0.9
power = 4

pg.init()
pg.display.set_caption('Platformer 1')
screen = pg.display.set_mode([WIDTH, HEIGHT])

running = True
while running == True:

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

        # print(up_key, '\t', down_key, '\t', left_key, '\t', right_key)

    # After processing events:

    # Handle x velocity
    if left_key and not right_key:
        car_x_vel -= power
    elif not left_key and right_key:
        car_x_vel += power
    else:
        car_x_vel = car_x_vel * friction
    
    # Limit x velocity
    if car_x_vel > max_vel:
        car_x_vel = max_vel
    elif car_x_vel < -max_vel:
        car_x_vel = -max_vel

    # Handle y velocity
    if up_key and not down_key:
        car_y_vel -= power
    elif not up_key and down_key:
        car_y_vel += power
    else:
        car_y_vel = car_y_vel * friction

    # Limit y velocity
    if car_y_vel > max_vel:
        car_y_vel = max_vel
    elif car_y_vel < -max_vel:
        car_y_vel = -max_vel

    # Change position by velocity
    car_x += car_x_vel
    car_y += car_y_vel

    # Warp car over x axis
    if car_x + (CAR_WIDTH/2) < 0:
        car_x = WIDTH - car_x
    elif car_x - (CAR_WIDTH/2) > WIDTH:
        car_x = car_x - WIDTH - CAR_WIDTH

    # Warp car over y axis
    if car_y + (CAR_HEIGHT/2) < 0:
        car_y = HEIGHT - car_y
    elif car_y - (CAR_HEIGHT/2) > HEIGHT:
        car_y = car_y - HEIGHT - CAR_HEIGHT

    # Render car
    screen.fill(WHITE)
    pg.draw.rect(screen, BLUE, (int(car_x-(CAR_WIDTH/2)), int(car_y-(CAR_HEIGHT/2)), CAR_WIDTH, CAR_HEIGHT))
    pg.display.update()

pg.quit()
            
