import pygame
import time
import random

pygame.init()

# Global
gameExit = False
gameIntro = True
lives = 3
dodged = 0
fuel_level = 20

# RGB - Read Green Blue
black           =   (0,0,0)
white           =   (255,255,255)
red             =   (200,0,0)
green           =   (0,200,0)
blue            =   (0,0,200)
bright_red      =   (255,0,0)
bright_green    =   (0,255,0)
bright_blue     =   (0,0,255)

# Display
display_width   = 800
display_height  = 600
display_caption = 'A bit Racey'

# Intro buttons
bIntro_x = (150, 550)
bIntro_y = (450, 450)
bIntro_width = 100
bIntro_height = 50
bIntro_color = ((green, bright_green), (red, bright_red))
bIntro_caption = ('GO!', 'Quit')
# game_loop and pause can not be refered before they are defined
# bIntro_action = (game_loop, pause) is moved to game_intro()

#Car
carImg = pygame.image.load('racecar.png')
car_width = 73
car_height = 83

# Font
smallfont = pygame.font.SysFont('comicsansms', 25)
medfont = pygame.font.SysFont('comicsansms', 50)
largefont = pygame.font.SysFont('comicsansms', 80)

# Functions
def object(ob):
    if ob['shape'] == 'rect':
        pygame.draw.rect(gameDisplay, ob['color'],\
            [ob['x'], ob['y'], ob['width'], ob['height']], ob['line'])
    elif ob['shape'] == 'circle':
        pygame.draw.circle(gameDisplay, ob['color'],\
            (ob['x'], ob['y']), ob['radius'], ob['line'])
    elif ob['shape'] == 'img':
        img = pygame.image.load(ob['file'])
        gameDisplay.blit(img, (ob['x'], ob['y']))

def car(x,y):
    gameDisplay.blit(carImg, (x,y))

def text_objects(text, font, color=black):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()

def display_message(text, font=smallfont, color=black,\
    center=True, x=display_width/2, y=display_height/2, x_displace=0, y_displace=0):
    textSurf, textRect = text_objects(text, font, color=color)
    if center:
        textRect.center = (x+x_displace, y+y_displace)
    else:
        textRect = textRect.move(x+x_displace, y+y_displace)
    gameDisplay.blit(textSurf, textRect)

def display_button(x, y, width, height, color, caption=None, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    #print(mouse)
    #print(click)
    if y+height > mouse[1] > y and x+width > mouse[0] > x:
        pygame.draw.rect(gameDisplay, color[1], (x, y, width, height))
        if click[0] == 1 and action != None:
            action()
    else:
        pygame.draw.rect(gameDisplay, color[0], (x, y, width, height))
        
    display_message(caption, x=x+(width/2), y=y+(height/2))

def score(dodged):
    display_message('Score: '+str(dodged), color=green, center=False, x=0, y=0)

def refuel(fuel_level):
    display_message('Fuel: '+str(fuel_level), color=red, center=False, x=0, y=30)

def life(lives, color=blue):
    display_message('Lives: '+str(lives), color=color, center=False, x=0, y=60)

def crash():
    global lives
    global fuel_level
    global dodged
    life(lives, color=white)
    lives += -1
    life(lives)
    if lives > 0:
        display_message('You Crashed', font=largefont, color=red)
        pygame.display.update()
        time.sleep(2)
    else:
        pause(msg1='Game Over', msg1_font=largefont, msg1_y_displace=-60)
        lives = 3
        dodged = 0
        fuel_level = 20

    # Clean the display to prevent overlapping text
    # in case of pause directly after comming back to game_loop(). 
    gameDisplay.fill(white)
    pygame.display.update()
    game_loop()

def exit_the_game():
    pygame.quit()
    quit()

def pause(msg1='Paused', msg1_font=medfont, msg1_y_displace=-20):
    paused = True
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c or event.key == pygame.K_SPACE:
                    paused = False
                if event.key == pygame.K_q:
                    exit_the_game()

        if gameIntro:
            gameDisplay.fill(white)

        display_message(msg1, font=msg1_font, color=red, y_displace=msg1_y_displace)
        display_message('Press C to Continue or Q to Quit', font=smallfont,\
            color=blue, y_displace=20)

        pygame.display.update()
        clock.tick(5)

def game_intro():
    bIntro_action = (game_loop, pause)

    global gameIntro
    while gameIntro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pause()
                gameIntro = False

        gameDisplay.fill(white)
        display_message('A car race', font=medfont, color=red, y_displace=-20)
        
        for i in range(2):
            display_button(bIntro_x[i], bIntro_y[i], bIntro_width, bIntro_height,\
                bIntro_color[i], caption=bIntro_caption[i], action=bIntro_action[i])

        pygame.display.update()
        clock.tick(15)

def game_loop():
    global gameIntro
    gameIntro = False
    global gameExit
    gameExit = False
    global lives
    global fuel_level
    global dodged

    x = (display_width * 0.45)
    y = (display_height * 0.8)
    
    x_change = 0 
    y_change = 0
    
    # Obstacles
    objects = [
        {'type': 'obstacle', 'speed' : 5, 'shape' : 'rect', 'color' : black,\
            'x' : random.randrange(0, display_width), 'y' : -500,\
                'width' : car_width-20, 'height' : 80, 'line' : 0},
        {'type': 'obstacle', 'speed' : 4, 'shape' : 'rect', 'color' : bright_green,\
            'x' : random.randrange(0, display_width), 'y' : -600,\
                'width' : car_width-30, 'height' : 120, 'line' : 4},
        {'type': 'obstacle', 'speed' : 8, 'shape' : 'circle', 'slide': 1, 'color' : bright_blue,\
            'x' : random.randrange(45, display_width-45), 'y' : -800,\
                'radius' : 20, 'line' : 0},
        {'type': 'obstacle', 'speed' : 2, 'shape' : 'circle', 'slide': -2, 'color' : blue,\
            'x' : random.randrange(45, display_width-45), 'y' : -400,\
                'radius' : 30, 'line' : 5},        
        {'type': 'obstacle', 'speed' : 5, 'shape' : 'circle', 'slide': 4, 'color' : bright_red,\
            'x' : random.randrange(45, display_width-45), 'y' : -700,\
                'radius' : 40, 'line' : 10}
    ]
    # Goodies
    objects.extend([
        {'type': 'fuel', 'speed' : 5, 'shape' : 'img', 'file' : 'hydrogen_station-3.png',\
            'x' : random.randrange(0, display_width), 'y' : -500,\
                'width' : 40, 'height' : 48}
    ])

    while not gameExit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pause()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -5
                elif event.key == pygame.K_RIGHT:
                    x_change = 5
                elif event.key == pygame.K_UP and fuel_level > 0.5:
                    y_change = -5
                elif event.key == pygame.K_p or event.key == pygame.K_SPACE:
                    pause()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_change = 0
                elif event.key == pygame.K_UP:
                    y_change = 3

            #print(event)
        
        x += x_change
        y += y_change
        if y_change == -5:
            fuel_level += -0.5
            if fuel_level < 0.5:
                y_change = 3

        gameDisplay.fill(white)

        # Draw the objects
        for ob in objects:
            object(ob)
            ob['y'] += ob['speed']
            if ob['shape'] == 'circle':
                ob['x'] += ob['slide']

        # Display the car and update the score.
        car(x,y)
        score(dodged)
        refuel(fuel_level)
        life(lives)
        
        # Check for colision with the left and right boundary.
        if x > display_width - car_width or x < 0:
            crash()
        
        # Check for minimum height for the car and deactivate "free falling" if reached.
        if y > (display_height * 0.8):
            y = (display_height * 0.8)
            y_change = 0
        # Check for maximum height for the car and activate "free falling" if reached.
        if y < 100:
            y_change = 3
        
        # Colision and fuel refill detection.
        for ob in objects:
            # Rectangles and images have the same shape.
            if ob['shape'] == 'rect' or ob['shape'] == 'img':
                if (ob['y']+ob['height'] > y+5 > ob['y'] or y+car_height-5 > ob['y'] > y)\
                    and (ob['x']+ob['width'] > x+5 and x+car_width-5 > ob['x']):
                    # Is it obstacle or fuel?
                    if ob['type'] == 'obstacle':
                        crash()
                    # Fuel
                    elif ob['type'] == 'fuel':
                        fuel_level += 10
                        refuel(fuel_level)
                        ob['x'] = random.randrange(0, display_width)
                        ob['y'] = -1 * ob['y'] - 500
                elif ob['y'] > display_height:
                    ob['y'] = 0 - ob['height']
                    ob['x'] = random.randrange(0, display_width)
                    # Score is only for obstacles.
                    if ob['type'] == 'obstacle':
                        dodged += 1
            
            elif ob['shape'] == 'circle':
                if ob['x']+ob['radius'] > x+15 > ob['x'] or x < ob['x']-ob['radius'] < x+car_width-15:
                    if ob['y']+ob['radius'] > y+15 > ob['y'] or y < ob['y']-ob['radius'] < y+car_height-15:
                        crash()
                elif ob['y']-ob['radius'] > display_height:
                    ob['y'] = 0 - ob['radius']
                    ob['x'] = random.randrange(45, display_width+45)
                    dodged += 1

                # If a circle hits the side wall it will bounce or it will be
                # teleportated to the other side.
                if ob['line'] == 0 and ob['x']-ob['radius'] > display_width:
                    ob['x'] = 0
                if ob['line'] > 0 and (ob['x']+ob['radius'] > display_width\
                    or ob['x']-ob['radius'] < 0):
                    ob['slide'] = -1 * ob['slide']

            elif ob['y'] > display_height:
                ob['y'] = 0 - ob['height']
                ob['x'] = random.randrange(0, display_width)

        pygame.display.update()
        clock.tick(60)

gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption(display_caption)
clock = pygame.time.Clock()

if not gameExit:
    if gameIntro:
        game_intro()
    game_loop()

# We should never reach this since exit_the_game() is called from pause()
exit_the_game()
