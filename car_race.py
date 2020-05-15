import pygame
import time
from datetime import datetime
import random
import config

pygame.init()

config.init()
config_data = config.load_config()

# Global
gameIntro = True
choosePlayer = False
lives = 3
dodged = 0
fuel_level = 20

# RGB - Read Green Blue
black           =   (0,0,0)
white           =   (255,255,255)
grey_1          =   (184,184,148)
grey_2          =   (122, 122, 82)
red             =   (200,0,0)
green           =   (0,200,0)
blue            =   (0,0,200)
bright_red      =   (255,0,0)
bright_green    =   (0,255,0)
bright_blue     =   (0,0,255)

# Display
display_width   = 800
display_height  = 600
display_color   = grey_2
display_caption = config_data['display_caption']

#Player
#default_player = config_data["players"]["last_player"]
default_player = config.load_score_history()['last_player']
player = default_player

# Intro buttons
bIntro_caption = ('GO!', 'Quit', 'Change player')
""" bIntro_x = (150, 550, 550)
bIntro_y = (450, 450, 130)
bIntro_width = (100, 100, 200) """
bIntro_x = (150, 550, 350)
bIntro_y = (450, 450, 10)
bIntro_width = (100, 100, 180)
bIntro_height = (50, 50, 50)
bIntro_color = ((green, bright_green), (red, bright_red), (green, bright_green))
# game_loop and pause can not be refered before they are defined
# bIntro_action = (game_loop, pause) is moved to game_intro()

#Car
carImg = pygame.image.load('img/racecar.png')
car_width = 73
car_height = 83

# Font
smallfont = pygame.font.SysFont('comicsansms', 25)
medfont = pygame.font.SysFont('comicsansms', 50)
largefont = pygame.font.SysFont('comicsansms', 80)

# Functions
# Display objects: rect, circle and image.
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

# Display the car.
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

def display_button(x, y, width, height, color, caption=None,
action=None, action_param=None, return_smth=False):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    respond = None
    #print(mouse)
    #print(click)
    if y+height > mouse[1] > y and x+width > mouse[0] > x:
        pygame.draw.rect(gameDisplay, color[1], (x, y, width, height))
        if click[0] == 1 and action != None:
            if action_param == None and return_smth == False:
                action()
            elif action_param == None and return_smth == True:
                respond = action()
            elif action_param != None and return_smth == False:
                action(action_param)
            else: # action_param != None and return_smth == True
                respond = action(action_param)
        elif click[0] == 1 and action == None:
            return(True) # button/text fieled has been chosen
    else:
        pygame.draw.rect(gameDisplay, color[0], (x, y, width, height))
        
    display_message(caption, x=x+(width/2), y=y+(height/2))
    if return_smth == True:
        return(respond)

def remove_player(player_x):
    # are you sure
    if pause(msg1='This will remove player ' + player_x, msg2='y or n'):
        config.remove_player(player_x) # remove player
        return(True)
    else:
        return(False) # the player was not removed

def new_player(new_player):
    score_history = config.load_score_history()
    # Check if this name is available.
    createPlayer = True
    for p in score_history['player']:
        if p['name'] == new_player:
            createPlayer = False # This player already exists.
    if createPlayer:
        config.create_new_player(new_player)
        set_player(new_player)
    else:
        display_message('This player already exists!', font=medfont, color=red)
        pygame.display.update()
        time.sleep(2)

def set_player(new_player):
    global choosePlayer, player
    choosePlayer = False
    player = new_player
    global your_last_score, your_best_score, best_score, best_score_player, best_score_date
    your_last_score, your_best_score, best_score, best_score_player, best_score_date = get_score_history()

def choose_player():
    global choosePlayer
    choosePlayer = True
    reload_score_history = True
    
    x_pl = (display_width/2)-200 # x position of buttons with players' names
    # players' buttons properties
    width = 200
    height = 50
    color = (green, bright_green)
    # remove player button properties
    del_but_caption = 'Del'
    del_but_width = 50
    del_but_color = (red, bright_red)
    
    text = 'enter new player'
    entered = False
    textInput = False

    while choosePlayer:
        if reload_score_history:
            score_history = config.load_score_history()
            reload_score_history = False
        y_pl = 30
        gameDisplay.fill(display_color)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pause()
                #gameIntro = False
        
            # Choose/add player.
            entered = display_button(x_pl, y_pl, width, height, color, caption=text)
            if entered:
                text = ''
                textInput = True
            if textInput:
                if event.type == pygame.KEYDOWN:
                    #print(event)
                    if event.key == pygame.K_RETURN:
                        new_player(text)
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    elif event.key == pygame.K_ESCAPE:
                        textInput = False
                    else:
                        #print(event.key)
                        #print(pygame.key.name(event.key))
                        text += pygame.key.name(event.key)
            
            for p in score_history['player']:
                y_pl += height+10
                # remove player button
                if p['name'] != 'Anonymous':
                    if display_button(x_pl-del_but_width-10, y_pl, del_but_width,\
                        height, del_but_color, caption=del_but_caption,\
                        action=remove_player, action_param=p['name'], return_smth=True):
                        reload_score_history = True
                # player button
                display_button(x_pl, y_pl, width, height, color, caption=p['name'],\
                    action=set_player, action_param=p['name'])
                # score data
                display_message('last: '+str(p['last_score'])+', best: '+str(p['best_score']),\
                    center=False, x=x_pl+width+4, y=y_pl)
            
            pygame.display.update()
            clock.tick(30)

def score(dodged):
    display_message('Score: '+str(dodged), color=green, center=False, x=0, y=0)

def refuel(fuel_level):
    display_message('Fuel: '+str(fuel_level), color=red, center=False, x=0, y=30)

def life(lives, color=blue):
    display_message('Lives: '+str(lives), color=color, center=False, x=0, y=60)

def levels(level, color=blue):
    display_message('Level: '+str(level), color=color, center=False, x=0, y=90)

def crash():
    global gameIntro
    global lives
    score_history = {}
    p = {}
    life(lives, color=white)
    lives += -1
    life(lives)
    if lives > 0: # Just a crash. Display the message and return.
        display_message('You Crashed', font=largefont, color=red)
        pygame.display.update()
        time.sleep(2)
    else: # Game Over
        now = datetime.now()
        time_stamp = now.strftime("%Y-%m-%d %T")

        score_history = config.load_score_history()

        score_history['last_player'] = player
        if score_history['best_score'] < dodged:
            score_history['best_score_player'] = player
            score_history['best_score'] = dodged
            score_history['best_score_date'] = time_stamp

        # Find/add player and update it's score.
        for p in score_history['player']:
            if p['name'] == player:
                p['last_score'] = dodged
                p['last_score_date'] = time_stamp
                if p['best_score'] < dodged:
                    p['best_score'] = dodged
                    p['best_score_date'] = time_stamp

        config.edit_score_history(score_history)
        
        pause(msg1='Game Over', msg1_font=largefont, msg1_y_displace=-60)
        gameIntro = True

    # Clean the display to prevent overlapping text
    # in case of pause directly after comming back to game_loop(). 
    gameDisplay.fill(display_color)
    pygame.display.update()

def exit_the_game():
    pygame.quit()
    quit()

def pause(msg1='Paused', msg1_font=medfont, msg1_y_displace=-20,
msg2='Press C to Continue or Q to Quit'):
    paused = True

    if msg1 == 'Game Over':
        your_last_score, your_best_score, best_score, best_score_player, best_score_date = get_score_history()
        display_score_history(your_last_score, your_best_score, best_score, best_score_player, best_score_date)

    if gameIntro: # if pygame.QUIT during game_intro() clean the screen
        gameDisplay.fill(display_color)

    display_message(msg1, font=msg1_font, color=red, y_displace=msg1_y_displace)
    display_message(msg2, font=smallfont, color=blue, y_displace=20)
 
    pygame.display.update()

    while paused:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if msg2 != 'y or n':
                    if event.key == pygame.K_c or event.key == pygame.K_SPACE:
                        paused = False
                    if event.key == pygame.K_q:
                        exit_the_game()
                
                if msg2 == 'y or n' and event.key == pygame.K_y:
                    return(True)
                if msg2 == 'y or n' and event.key == pygame.K_n:
                    return(False)

        display_message(msg1, font=msg1_font, color=red, y_displace=msg1_y_displace)
        display_message(msg2, font=smallfont, color=blue, y_displace=20)

        clock.tick(15)

def get_score_history():
    score_history = config.load_score_history()
    best_score = score_history['best_score']
    best_score_player = score_history['best_score_player']
    best_score_date = score_history['best_score_date']
    # Find/add player and update it's score.
    for p in score_history['player']:
        if p['name'] == player:
            your_last_score = p['last_score']
            your_best_score = p['best_score']

    return(your_last_score, your_best_score, best_score, best_score_player, best_score_date)

def display_score_history(your_last_score, your_best_score, best_score, best_score_player, best_score_date):
    display_message('player: ' + player, color=green, center=False, x=550, y=0)
    display_message('your last score: ' + str(your_last_score), color=green, center=False, x=550, y=30)
    display_message('your best score: ' + str(your_best_score), color=green, center=False, x=550, y=60)
    display_message('_______________', color=red, center=False, x=550, y=62)
    display_message('the best score: ' + str(best_score), color=green, center=False, x=550, y=94)
    display_message('by ' + str(best_score_player) + ' on', color=green, center=False, x=550, y=124)
    display_message(str(best_score_date), color=green, center=False, x=550, y=154)

def game_intro():    
    # game_loop and pause can not be defined in the begining of this file.
    #bIntro_action = (game_loop, pause, choose_player)
    bIntro_action = (game_loop, exit_the_game, choose_player)
    
    #reload_score_history = True
    global your_last_score, your_best_score, best_score, best_score_player, best_score_date
    your_last_score, your_best_score, best_score, best_score_player, best_score_date = get_score_history()
    
    gameIntro = True
    while gameIntro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pause()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_g:
                    gameIntro = False
                if event.key == pygame.K_q:
                    exit_the_game()

        gameDisplay.fill(display_color)
        display_message('A car race', font=medfont, color=red, y_displace=-20)
        display_score_history(your_last_score, your_best_score, best_score, best_score_player, best_score_date)
                
        for i in range(len(bIntro_action)):
            click = display_button(bIntro_x[i], bIntro_y[i], bIntro_width[i],\
                bIntro_height[i], bIntro_color[i], caption=bIntro_caption[i])
            if click:
                if bIntro_action[i] == game_loop:
                    gameIntro = False
                elif bIntro_action[i] == exit_the_game:
                    exit_the_game()
                elif bIntro_action[i] == choose_player:
                    choose_player()

        pygame.display.update()
        clock.tick(15)

def game_loop():
    global gameIntro
    gameIntro = True

    global lives, fuel_level, dodged
    lives = 3
    dodged = 0
    fuel_level = 20

    level = 0

    gameExit = False
    while not gameExit:
        x_change = 0 
        y_change = 0

        lostLife = False
        
        if gameIntro:
            lives = 3
            dodged = 0
            fuel_level = 20
            game_intro()
            gameIntro = False

        # Road line
        rl_speed = 5
        rl_width = 10
        rl_height = 40
        rl_line = 2
        road_line = [
            {'type': 'road_line', 'speed' : rl_speed, 'shape' : 'rect', 'color' : black,\
                'x' : display_width/2, 'y' : 0,\
                    'width' : rl_width, 'height' : rl_height, 'line' : rl_line},
            {'type': 'road_line', 'speed' : rl_speed, 'shape' : 'rect', 'color' : black,\
                'x' : display_width/2, 'y' : 80,\
                    'width' : rl_width, 'height' : rl_height, 'line' : rl_line},
            {'type': 'road_line', 'speed' : rl_speed, 'shape' : 'rect', 'color' : black,\
                'x' : display_width/2, 'y' : 160,\
                    'width' : rl_width, 'height' : rl_height, 'line' : rl_line},
            {'type': 'road_line', 'speed' : rl_speed, 'shape' : 'rect', 'color' : black,\
                'x' : display_width/2, 'y' : 240,\
                    'width' : rl_width, 'height' : rl_height, 'line' : rl_line},
            {'type': 'road_line', 'speed' : rl_speed, 'shape' : 'rect', 'color' : black,\
                'x' : display_width/2, 'y' : 320,\
                    'width' : rl_width, 'height' : rl_height, 'line' : rl_line},
            {'type': 'road_line', 'speed' : rl_speed, 'shape' : 'rect', 'color' : black,\
                'x' : display_width/2, 'y' : 400,\
                    'width' : rl_width, 'height' : rl_height, 'line' : rl_line},
            {'type': 'road_line', 'speed' : rl_speed, 'shape' : 'rect', 'color' : black,\
                'x' : display_width/2, 'y' : 480,\
                    'width' : rl_width, 'height' : rl_height, 'line' : rl_line},
            {'type': 'road_line', 'speed' : rl_speed, 'shape' : 'rect', 'color' : black,\
                'x' : display_width/2, 'y' : 560,\
                    'width' : rl_width, 'height' : rl_height, 'line' : rl_line},
        ]
        # Obstacles
        obstacle = [
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
                    'radius' : 40, 'line' : 10},
            {'type': 'obstacle', 'speed' : 6, 'shape' : 'rect', 'color' : red,\
                'x' : random.randrange(0, display_width), 'y' : -100,\
                    'width' : 30, 'height' : 30, 'line' : 0},
            {'type': 'obstacle', 'speed' : 8, 'shape' : 'rect', 'color' : red,\
                'x' : random.randrange(0, display_width), 'y' : -300,\
                    'width' : 20, 'height' : 20, 'line' : 0},
            {'type': 'obstacle', 'speed' : 6, 'shape' : 'rect', 'color' : green,\
                'x' : random.randrange(0, display_width), 'y' : -250,\
                    'width' : 30, 'height' : 30, 'line' : 0}
        ]     
        # obstacle.extend([ {'type': ... 'height' : 48} ])
        # obstacle.insert(0, {'type': ... height' : 48})
        del obstacle[0]
        obstacle.insert(0, 
            {'type': 'obstacle', 'speed' : 5, 'shape' : 'img', 'file' : 'img/racecar_red_yellow.png',\
                'x' : random.randrange(0, display_width), 'y' : -200,\
                    'width' : 73, 'height' : 83},
        )
        del obstacle[1]
        obstacle.insert(1, 
            {'type': 'obstacle', 'speed' : 4, 'shape' : 'img', 'file' : 'img/racecar_yellow_turquoise.png',\
                'x' : random.randrange(0, display_width), 'y' : -500,\
                    'width' : 73, 'height' : 83},
        )
        del obstacle[4]
        obstacle.insert(4, 
            {'type': 'obstacle', 'speed' : 5, 'shape' : 'img', 'file' : 'img/racecar_blue_red.png', 'slide': 1,\
                'x' : random.randrange(0, display_width), 'y' : -50,\
                    'width' : 73, 'height' : 83},
        )

        # Goodies
        goody = [
            {'type': 'fuel', 'speed' : 5, 'shape' : 'img', 'file' : 'img/hydrogen_station-1.png',\
                'x' : random.randrange(0, display_width), 'y' : -500,\
                    'width' : 40, 'height' : 48},
            {'type': 'fuel', 'speed' : 5, 'shape' : 'img', 'file' : 'img/hydrogen_station-2.png',\
                'x' : random.randrange(0, display_width), 'y' : -200,\
                    'width' : 40, 'height' : 48}
        ]

        x = (display_width * 0.45)
        y = (display_height * 0.8)

        obj_set = [0]*20
        # Versions
        """ obj_set[1] = goody[0:1] + obstacle[0:4]
        obj_set[2] = goody[0:1] + obstacle[0:5]
        obj_set[3] = goody[0:1] + obstacle[0:7]
        obj_set[4] = goody + obstacle """
        obj_set[1] = road_line + goody[0:1] + obstacle[0:4]
        obj_set[2] = road_line + goody[0:1] + obstacle[0:5]
        obj_set[3] = road_line + goody[0:1] + obstacle[0:7]
        obj_set[4] = road_line + goody + obstacle
        """ obj_set[1] = road_line + goody[0:1] + obstacle[0:2] + obstacle[5:6]
        obj_set[2] = road_line + goody[0:1] + obstacle[0:2] + obstacle[5:7]
        obj_set[3] = road_line + goody[0:1] + obstacle[0:2] + obstacle[5:8]
        obj_set[4] = road_line + goody + obstacle """

        objects = obj_set[1]

        while not lostLife:
            if dodged < 20:
                objects = obj_set[1] 
                level = 1
            elif 49 > dodged >= 20: #if 99 > dodged >= 50:
                objects = obj_set[2]
                level = 2
            elif 79 > dodged >= 50: #elif 149 > dodged >= 100: 
                objects = obj_set[3]
                level = 3
            else:
                objects = obj_set[4]
                level = 4

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

            gameDisplay.fill(display_color)

            # Draw the objects
            for ob in objects:
                object(ob)
                ob['y'] += ob['speed']
                #if ob['shape'] == 'circle':
                if 'slide' in ob:
                    ob['x'] += ob['slide']

            # Display the car and update the score.
            car(x,y)
            score(dodged)
            refuel(fuel_level)
            life(lives)
            levels(level)
            
            # Check for colision with the left and right boundary.
            if x > display_width - car_width or x < 0:
                crash()
                lostLife = True
            
            # Check for minimum height for the car and deactivate "free falling" if reached.
            if y > (display_height * 0.8):
                y = (display_height * 0.8)
                y_change = 0
            # Check for maximum height for the car and activate "free falling" if reached.
            if y < 5: #100:
                y_change = 3
            
            for ob in objects:
                # Rectangles and images have the same shape.
                if ob['shape'] == 'rect' or ob['shape'] == 'img':
                    # Colision and fuel refill detection.
                    if (ob['y']+ob['height'] > y+5 > ob['y'] or y+car_height-5 > ob['y'] > y)\
                        and (ob['x']+ob['width'] > x+5 and x+car_width-5 > ob['x']):
                        # Is it obstacle or fuel?
                        if ob['type'] == 'obstacle':
                            crash()
                            lostLife = True
                        # Fuel
                        elif ob['type'] == 'fuel':
                            fuel_level += 10
                            refuel(fuel_level)
                            ob['x'] = random.randrange(0, display_width)
                            ob['y'] = -1 * ob['y'] - 500
                    # End of display - send the object to the top and increase the score if an obstacle.
                    elif ob['y'] > display_height:
                        ob['y'] = 0 - ob['height']
                        if ob['type'] != 'road_line':
                            ob['x'] = random.randrange(0, display_width)
                        # Score is only for obstacles.
                        if ob['type'] == 'obstacle':
                            dodged += 1
                
                elif ob['shape'] == 'circle':
                    # Colision detection.
                    if ob['x']+ob['radius'] > x+15 > ob['x'] or x < ob['x']-ob['radius'] < x+car_width-15:
                        if ob['y']+ob['radius'] > y+15 > ob['y'] or y < ob['y']-ob['radius'] < y+car_height-15:
                            crash()
                            lostLife = True
                    # End of display - send the object to the top and increase the score.
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

                """ elif ob['y'] > display_height:
                    ob['y'] = 0 - ob['height']
                    ob['x'] = random.randrange(0, display_width) """
                
                if 'slide' in ob and ob['shape'] != 'circle':
                    if ob['x'] < 0 or ob['x']+ob['width'] > display_width:
                        ob['slide'] = -1 * ob['slide']

            pygame.display.update()
            clock.tick(60)

gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption(display_caption)
clock = pygame.time.Clock()

game_loop()
