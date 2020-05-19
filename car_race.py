import pygame
import time
from datetime import datetime
import random
import config

pygame.init()

config.init()
config_data = config.load_config()

# Demo and debug
NO_CRASH = False

# RGB - Read Green Blue
black           =   (0,0,0)
white           =   (255,255,255)
grey            =   (128, 128, 128)
red             =   (200,0,0)
green           =   (0,200,0)
blue            =   (0,0,200)
bright_red      =   (255,0,0)
bright_green    =   (0,255,0)
bright_blue     =   (0,0,255)

# Display
DSP_WIDTH   = config_data['display']['width']
DSP_HEIGHT  = config_data['display']['height']
DSP_COLOR   = locals()[config_data['display']['color']]
DSP_CAPTION = config_data['display']['caption']

# Levels
LIVES       = config_data['levels']['lives']
FUEL_LEVEL  = config_data['levels']['fuel_level']
L1_SPEED    = config_data['levels']['l1']['speed']
L2_SPEED    = config_data['levels']['l2']['speed']
L3_SPEED    = config_data['levels']['l3']['speed']
L4_SPEED    = config_data['levels']['l4']['speed']
SPEED = [0, L1_SPEED, L2_SPEED, L3_SPEED, L4_SPEED]

# Global
gameIntro = True
choosePlayer = False
lives = LIVES
fuel_level = FUEL_LEVEL
speed = SPEED[1]
dodged = 0
level = 1

# Road line
RL_LINE     = config_data['road_line']['line']
RL_COLOR    = locals()[config_data['road_line']['color']]
#RL_SPEED    = config_data['road_line']['speed']
#RL_SPEED    = speed
RL_WIDTH    = config_data['road_line']['width']
RL_HEIGHT   = config_data['road_line']['height']

#Player
default_player = config.load_score_history()['last_player']
player = default_player

# Intro buttons
bIntro_caption = ('GO!', 'Quit', 'Change player')
bIntro_x = (DSP_WIDTH/2-200, DSP_WIDTH/2+100, DSP_WIDTH-450) #(150, 550, 350)
bIntro_y = (DSP_HEIGHT*0.75, DSP_HEIGHT*0.75, 10) #(450, 450, 10)
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
    center=True, x=DSP_WIDTH/2, y=DSP_HEIGHT/2, x_displace=0, y_displace=0):
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
    
    x_pl = (DSP_WIDTH/2)-200 # x position of buttons with players' names
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
        gameDisplay.fill(DSP_COLOR)
        
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

def random_x(x1=0, x2=DSP_WIDTH):
    return random.randrange(x1, x2)

def score(dodged):
    display_message('Score: '+str(dodged), color=green, center=False, x=0, y=0)

def refuel(fuel_level):
    display_message('Fuel: '+str(fuel_level), color=red, center=False, x=0, y=30)

def life(lives, color=blue):
    display_message('Lives: '+str(lives), color=color, center=False, x=0, y=60)

def levels(level, color=blue):
    display_message('Level: '+str(level), color=color, center=False, x=0, y=90)

def collision_detection(ob, other_ob):
    """ print(ob)
    print(other_ob) """
    if (ob['y']+ob['height'] > other_ob['y']+5 > ob['y'] or other_ob['y']+other_ob['height']-5 > ob['y'] > other_ob['y'])\
        and (ob['x']+ob['width'] > other_ob['x']+5 and other_ob['x']+other_ob['width']-5 > ob['x']):
        return True #print('COLLISION')

def crash():
    global gameIntro
    global lives
    score_history = {}
    p = {}
    life(lives, color=DSP_COLOR) # Just overwrite lives and keep the rest as it is.
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
    gameDisplay.fill(DSP_COLOR)
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
        gameDisplay.fill(DSP_COLOR)

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
    display_message('player: ' + player, color=green, center=False, x=DSP_WIDTH-250, y=0)
    display_message('your last score: ' + str(your_last_score), color=green, center=False, x=DSP_WIDTH-250, y=30)
    display_message('your best score: ' + str(your_best_score), color=green, center=False, x=DSP_WIDTH-250, y=60)
    display_message('_______________', color=red, center=False, x=DSP_WIDTH-250, y=62)
    display_message('the best score: ' + str(best_score), color=green, center=False, x=DSP_WIDTH-250, y=94)
    display_message('by ' + str(best_score_player) + ' on', color=green, center=False, x=DSP_WIDTH-250, y=124)
    display_message(str(best_score_date), color=green, center=False, x=DSP_WIDTH-250, y=154)

def set_level1():
    global lives, fuel_level, speed, dodged, level
    lives = 3
    fuel_level = 20
    speed = L1_SPEED
    dodged = 0
    level = 1

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

        gameDisplay.fill(DSP_COLOR)
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

    global lives, fuel_level, speed, dodged, level
    set_level1()

    gameExit = False
    while not gameExit:
        x_change = 0 
        y_change = 0

        lostLife = False
        
        if gameIntro:
            set_level1()
            game_intro()
            gameIntro = False

        # Road line
        road_line = []
        for rl in range(0, DSP_HEIGHT, 2*RL_HEIGHT):
            road_line2 = {'type':'road_line', 'shape':'rect', 'color':RL_COLOR,
                'width':RL_WIDTH, 'height':RL_HEIGHT, 'line':RL_LINE, 'speed':0,
                'x':DSP_WIDTH/2, 'y':rl}
            road_line.append(road_line2)

        # Obstacles
        obstacle = [
            {'type': 'obstacle', 'speed':0, 'shape' : 'rect', 'color' : black,\
                'x' : random_x(), 'y' : -500,\
                    'width' : car_width-20, 'height' : 80, 'line' : 0},
            {'type': 'obstacle', 'speed':-1, 'shape' : 'rect', 'color' : bright_green,\
                'x' : random_x(), 'y' : -600,\
                    'width' : car_width-30, 'height' : 120, 'line' : 4},
            {'type': 'obstacle', 'speed':3, 'shape' : 'circle', 'slide': 1, 'color' : bright_blue,\
                'x' : random.randrange(45, DSP_WIDTH-45), 'y' : -800,\
                    'radius' : 20, 'line' : 0},
            {'type': 'obstacle', 'speed':-2, 'shape' : 'circle', 'slide': -2, 'color' : blue,\
                'x' : random.randrange(45, DSP_WIDTH-45), 'y' : -400,\
                    'radius' : 30, 'line' : 5}, 
            {'type': 'obstacle', 'speed':0, 'shape' : 'circle', 'slide': 4, 'color' : bright_red,\
                'x' : random.randrange(45, DSP_WIDTH-45), 'y' : -700,\
                    'radius' : 40, 'line' : 10},
            {'type': 'obstacle', 'speed':1, 'shape' : 'rect', 'color' : red,\
                'x' : random_x(), 'y' : -100,\
                    'width' : 30, 'height' : 30, 'line' : 0},
            {'type': 'obstacle', 'speed':3, 'shape' : 'rect', 'color' : red,\
                'x' : random_x(), 'y' : -300,\
                    'width' : 20, 'height' : 20, 'line' : 0},
            {'type': 'obstacle', 'speed':1, 'shape' : 'rect', 'color' : green,\
                'x' : random_x(), 'y' : -250,\
                    'width' : 30, 'height' : 30, 'line' : 0}
        ]     
        # obstacle.extend([ {'type': ... 'height' : 48} ])
        # obstacle.insert(0, {'type': ... height' : 48})
        del obstacle[0]
        obstacle.insert(0, 
            {'type':'obstacle', 'shape':'img', 'file':'img/racecar_red_yellow.png',
            'width':73, 'height':83, 'speed':0,
            'x':random_x(), 'y':-200},
        )
        del obstacle[1]
        obstacle.insert(1, 
            {'type':'obstacle', 'shape':'img', 'file':'img/racecar_yellow_turquoise.png',
            'width':73, 'height':83, 'speed':-1,
            'x':random_x(), 'y':-500},
        )
        del obstacle[2]
        obstacle.insert(2, 
            {'type':'obstacle', 'shape':'img', 'file':'img/motorbike.png',
            'width':47, 'height':69, 'speed':+3, 'slide':1, 'coll_resp':'bounce',
            'x':random_x(), 'y':-800},
        )
        del obstacle[4]
        obstacle.insert(4, 
            {'type':'obstacle', 'shape':'img', 'file':'img/racecar_blue_red.png',
            'width':73, 'height':83, 'speed':0, 'slide':1, 'coll_resp':'bounce',
            'x':random_x(), 'y':-50},
        )

        # Goodies
        goody = [
            {'type':'fuel', 'shape':'img', 'file':'img/hydrogen_station-1.png',
            'width':40, 'height':48, 'speed':0,
            'x':random_x(), 'y':-500},
            {'type':'fuel', 'shape':'img', 'file':'img/hydrogen_station-2.png',
            'width':40, 'height':48, 'speed':0,
            'x':random_x(), 'y':-200}
        ]

        x = (DSP_WIDTH * 0.45)
        y = (DSP_HEIGHT * 0.8)

        obj_set = [0]*20
        # Versions
        """ obj_set[1] = goody[0:1] + obstacle[0:4]
        obj_set[2] = goody[0:1] + obstacle[0:5]
        obj_set[3] = goody[0:1] + obstacle[0:7]
        obj_set[4] = goody + obstacle """
        obj_set[1] = road_line + goody[0:1] + obstacle[0:3]
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
                level = 1
            elif 49 > dodged >= 20: #if 99 > dodged >= 50:
                level = 2
            elif 79 > dodged >= 50: #elif 149 > dodged >= 100: 
                level = 3
            else:
                level = 4

            objects = obj_set[level]
            speed = SPEED[level]

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

            gameDisplay.fill(DSP_COLOR)

            # Draw the objects
            for ob in objects:
                object(ob)
                ob['y'] += ob['speed'] + speed
                if 'slide' in ob:
                    ob['x'] += ob['slide']

            # Display the car and update the score.
            car(x,y)
            score(dodged)
            refuel(fuel_level)
            life(lives)
            levels(level)
            
            # Check for colision with the left and right boundary.
            if x > DSP_WIDTH - car_width or x < 0:
                crash()
                lostLife = True
            
            # Check for minimum height for the car and deactivate "free falling" if reached.
            if y > (DSP_HEIGHT * 0.8):
                y = (DSP_HEIGHT * 0.8)
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
                        if ob['type'] == 'obstacle' and not NO_CRASH:
                            crash()
                            lostLife = True
                        # Fuel
                        elif ob['type'] == 'fuel':
                            fuel_level += 10
                            refuel(fuel_level)
                            ob['x'] = random_x()
                            ob['y'] = -1 * ob['y'] - 500
                    # End of display - send the object to the top and increase the score if an obstacle.
                    elif ob['y'] > DSP_HEIGHT:
                        ob['y'] = 0 - ob['height']
                        if ob['type'] != 'road_line':
                            ob['x'] = random_x()
                        # Score is only for obstacles.
                        if ob['type'] == 'obstacle':
                            dodged += 1
                
                elif ob['shape'] == 'circle':
                    # Colision detection.
                    if ob['x']+ob['radius'] > x+15 > ob['x'] or x < ob['x']-ob['radius'] < x+car_width-15:
                        if ob['y']+ob['radius'] > y+15 > ob['y'] or y < ob['y']-ob['radius'] < y+car_height-15:
                            if not NO_CRASH:
                                crash()
                                lostLife = True
                    # End of display - send the object to the top and increase the score.
                    elif ob['y']-ob['radius'] > DSP_HEIGHT:
                        ob['y'] = 0 - ob['radius']
                        ob['x'] = random.randrange(45, DSP_WIDTH+45)
                        dodged += 1

                    # If a circle hits the side wall it will bounce or it will be
                    # teleportated to the other side.
                    if ob['line'] == 0 and ob['x']-ob['radius'] > DSP_WIDTH:
                        ob['x'] = 0
                    if ob['line'] > 0 and (ob['x']+ob['radius'] > DSP_WIDTH\
                        or ob['x']-ob['radius'] < 0):
                        ob['slide'] = -1 * ob['slide']

                """ elif ob['y'] > DSP_HEIGHT:
                    ob['y'] = 0 - ob['height']
                    ob['x'] = random_x() """
                
                if 'coll_resp' in ob:
                    for other_ob in objects:
                        if other_ob['type'] != 'road_line' and other_ob['type'] != 'fuel' and\
                            other_ob['shape'] != 'circle' and\
                                objects.index(ob) != objects.index(other_ob):
                            if collision_detection(ob, other_ob):
                                ob['slide'] = -1 * ob['slide']


                if 'slide' in ob and ob['shape'] != 'circle':
                    if ob['x'] < 0 or ob['x']+ob['width'] > DSP_WIDTH:
                        ob['slide'] = -1 * ob['slide']

            pygame.display.update()
            clock.tick(60)

gameDisplay = pygame.display.set_mode((DSP_WIDTH,DSP_HEIGHT))
pygame.display.set_caption(DSP_CAPTION)
clock = pygame.time.Clock()

game_loop()
