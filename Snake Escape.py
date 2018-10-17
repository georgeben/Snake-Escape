#GEORGE BENJAMIN
#SNAKE ESCAPE

import pygame, sys, random
pygame.init()
pygame.mixer.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 30
total_frames = 0
direction = "right"
grass_boundary = 50
play_music = True
play_sfx = True
level = "medium"

powerup_spawn_intervals = [180, 360, 540, 720, 900, 1080, 1260, 1440, 1620, 1800, 1980, 2160, 2340, 2520, 2700, 2880, 3060,
                          3240, 3420, 3600, 3780, 3960, 4140, 4320, 4500, 4680, 4860, 5040, 5220, 5400, 5580, 5760, 5940, 6120,
                          6300, 6480, 6660, 6840, 7020, 7200, 7380, 7560, 7740, 7920, 8100, 8280, 8460, 8640, 8820, 9000]

#MISSION
game_mission = None
mission_score = None
number_of_powerup = None
number_of_rats = None
number_of_hawk = None


#SOUNDS
eagle = pygame.mixer.Sound("sound/eagle.wav")
power_up = pygame.mixer.Sound("sound/power up.ogg")

#COLOURS
WHITE = (255,255,255)
GREEN = (0, 170, 0)
RED = (170,0,0)
BLACK = (0,0,0)
YELLOW = (255,255,0)
BLUE = (0,0,170)
LIGHT_GREEN = (0,255,0)
LIGHT_RED = (255,0,0)
LIGHT_BLUE = (0,0,255)
PURPLE = (170,0,170)
LIGHT_PURPLE = (255,0,255)
GREY = (155,155,155)
#COLOURS

#IMAGES
background = pygame.image.load("assets/ground 2.png")
grass = pygame.image.load("assets/grass.png")
gameOver_sign = pygame.image.load("assets/gameOver sign.png")
snakehead = pygame.image.load("assets/head.png")
snake_tail = pygame.image.load("assets/tail.png")
icon = pygame.image.load("assets/icon.png")
intro_page = pygame.image.load("assets/cover page.png")
paused_screen = pygame.image.load("assets/paused screen.png")
bg = pygame.image.load("assets/background.png")
bg2 = pygame.image.load("assets/about page.png")
score_board = pygame.image.load("assets/score board.png")
mission_complete = pygame.image.load("assets/mission complete.png")

#GAME PROPS
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption("Snake Escape")
pygame.display.set_icon(icon)
clock = pygame.time.Clock()


class Rat(pygame.sprite.Sprite):
    List = pygame.sprite.Group()

    def __init__(self,image_string, SCREEN_HEIGHT,grass_boundry, rat_velx):
        pygame.sprite.Sprite.__init__(self)
        Rat.List.add(self)
        
        self.image = pygame.image.load(image_string)
        self.rect = self.image.get_rect()
        self.SCREEN_HEIGHT = SCREEN_HEIGHT
        self.grass_boundry = grass_boundry

        self.directions = ("right","left")
        self.direction = random.choice(self.directions)

        if self.direction == "right":
            self.rect.x = 0 - self.rect.width
        elif self.direction == "left":
            self.rect.x = SCREEN_WIDTH
        self.rect.y = random.randrange(self.grass_boundry,self.SCREEN_HEIGHT - self.grass_boundry,40)

        self.width = self.rect.width
        self.height = self.rect.height

        self.velx = rat_velx

           
        

    @staticmethod
    def motion(SCREEN_WIDTH):
        for rat in Rat.List:
            if rat.direction == "right":
                rat.image = pygame.image.load("assets/rat flipped.png")
                rat.rect.x += rat.velx
                if rat.rect.x > SCREEN_WIDTH:
                    Rat.List.remove(rat)
                    del rat
            elif rat.direction == "left":
                rat.rect.x -=rat.velx
                if rat.rect.x + rat.rect.width < 0:
                    Rat.List.remove(rat)
                    del rat

class Hawk(pygame.sprite.Sprite):
    List = pygame.sprite.Group()

    def __init__(self, image_string, SCREEN_WIDTH, SCREEN_HEIGHT):
        pygame.sprite.Sprite.__init__(self)
        Hawk.List.add(self)

        self.image = pygame.image.load(image_string)
        self.rect = self.image.get_rect()
        self.SCREEN_WIDTH = SCREEN_WIDTH
        self.SCREEN_HEIGHT = SCREEN_HEIGHT

        self.directions = ("right","left","up","down")
        self.direction = random.choice(self.directions)

        if self.direction == "right":
            self.rect.x = 0 - self.rect.width
            self.rect.y = random.randrange(0,SCREEN_HEIGHT - self.rect.height,70)
        elif self.direction == "left":
            self.rect.x = SCREEN_WIDTH
            self.rect.y = random.randrange(0,SCREEN_HEIGHT - self.rect.height,70)
        elif self.direction == "down":
            self.rect.y = 0
            self.rect.x = random.randrange(0,SCREEN_WIDTH - self.rect.width,70)
        elif self.direction == "up":
            self.rect.y = self.SCREEN_HEIGHT - self.rect.width
            self.rect.x = random.randrange(0,SCREEN_WIDTH - self.rect.width,70)
        

        self.width = self.rect.width
        self.height = self.rect.height

        self.velx = 20

    @staticmethod
    def hawk_motion(SCREEN_WIDTH, SCREEN_HEIGHT):
        for hawk in Hawk.List:
            if hawk.direction == "right":
                hawk.image = pygame.image.load("assets/hawk flipped.png")
                hawk.rect.x += hawk.velx
                if hawk.rect.x > SCREEN_WIDTH:
                    Hawk.List.remove(hawk)
                    del hawk
            elif hawk.direction == "left":
                hawk.rect.x -=hawk.velx
                if hawk.rect.x + hawk.rect.width < 0:
                    Hawk.List.remove(hawk)
                    del hawk
            elif hawk.direction == "up":
                hawk.image = pygame.image.load("assets/hawk up.png")
                hawk.rect.y -=hawk.velx
                if hawk.rect.y < 0:
                    Hawk.List.remove(hawk)
                    del hawk
            elif hawk.direction == "down":
                hawk.image = pygame.image.load("assets/hawk down.png")
                hawk.rect.y +=hawk.velx
                if hawk.rect.y + hawk.rect.height > SCREEN_HEIGHT:
                    Hawk.List.remove(hawk)
                    del hawk

class Sheild(pygame.sprite.Sprite):
    List = pygame.sprite.Group()
    def __init__(self, image_string, SCREEN_WIDTH, SCREEN_HEIGHT):
        pygame.sprite.Sprite.__init__(self)
        Sheild.List.add(self)

        self.image = pygame.image.load(image_string)
        self.rect = self.image.get_rect()

        self.screen_width = SCREEN_WIDTH
        self.screen_height = SCREEN_HEIGHT

        self.rect.x = random.randrange(50,750,40)
        self.rect.y = random.randrange(50,550,40)

        self.timer = 0


class Rat_pp(pygame.sprite.Sprite):
    List = pygame.sprite.Group()
    def __init__(self, image_string, SCREEN_WIDTH, SCREEN_HEIGHT):
        pygame.sprite.Sprite.__init__(self)
        Rat_pp.List.add(self)

        self.image = pygame.image.load(image_string)
        self.rect = self.image.get_rect()

        self.screen_width = SCREEN_WIDTH
        self.screen_height = SCREEN_HEIGHT

        self.rect.x = random.randrange(50,750,40)
        self.rect.y = random.randrange(50,550,40)

        self.timer = 0
        self.timeup = 0

def text_object(text, colour, size):
    message = pygame.font.SysFont("franklingothicmedium", size)
    textSurf = message.render(text, True, colour)
    return textSurf, textSurf.get_rect()

def text_to_button(msg, colour, buttonx, buttony, button_width, button_height, size):
    textSurf, textRect = text_object(msg, colour, size)
    textRect.center = ((buttonx +(button_width/2)), (buttony +(button_height/2)))
    screen.blit(textSurf, textRect)

def message_to_screen(text,y_displace,x = 0, y = 0,colour = BLACK, size = 20,font_type = "Comicsansms", centralized = True):
    font = pygame.font.SysFont(font_type, size)
    textSurf = font.render(text,True,colour)
    textRect = textSurf.get_rect()
    if centralized:
        textRect.center = SCREEN_WIDTH/2, (SCREEN_HEIGHT/2)+y_displace
        screen.blit(textSurf, textRect)
    else:
        screen.blit(textSurf,(x,y))

def intro_button(text, x, y, image, inactive_col, active_col, size, action):
    image = pygame.image.load(image)
    image_rect = image.get_rect()
    screen.blit(image, (x,y))
    width = image_rect.width
    height = image_rect.height
    
    cur = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x + width  > cur[0] > x and y + height > cur[1] > y:
        text_to_button(text,active_col,x,y,width,height,size)
        if click[0] == 1 and action != None:
            if action == "quit":
                pygame.quit()
                quit()
            elif action == "controls":
                game_controls()
            elif action == "about":
                about()
            elif action == "play":
                mission_screen()
            elif action == "gameplay":
                gameLoop()
            elif action == "settings":
                settings()    
    else:
        text_to_button(text,inactive_col,x,y,width,height,size)

def toggle_button(text1, text2, x, y, image, colour, size, action):
    global play_music
    global play_sfx
    global level
    image = pygame.image.load(image)
    image_rect = image.get_rect()
    screen.blit(image, (x,y))
    width = image_rect.width
    height = image_rect.height

    cur = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + width > cur[0] > x and y + height > cur[1] > y:
        if click[0] == 1:
            if action == "music":
                if play_music == False:
                    pygame.mixer.music.play(-1)
                    play_music = True
                elif play_music == True:
                    pygame.mixer.music.stop()
                    play_music = False
            elif action == "sfx":
                if play_sfx == False:
                    play_sfx = True
                elif play_sfx == True:
                    play_sfx = False
            elif action == "level":
                if level == "easy":
                    level = "medium"
                elif level == "medium":
                    level = "hard"
                elif level == "hard":
                    level = "easy"
                    
                    
    if action == "music": 
        if play_music  == True:
            text_to_button(text1, colour, x, y, width, height, size)
        elif play_music == False:
            text_to_button(text2, colour, x, y, width, height, size)
    elif action == "sfx": 
        if play_sfx  == True:
            text_to_button(text1, colour, x, y, width, height, size)
        elif play_sfx == False:
            text_to_button(text2, colour, x, y, width, height, size)
    elif action == "level":
        if level  == "easy":
            text_to_button("EASY", colour, x, y, width, height, size)
        if level  == "medium":
            text_to_button("MEDIUM", colour, x, y, width, height, size)
        if level  == "hard":
            text_to_button("HARD", colour, x, y, width, height, size)
                

def button2(inactive_but, active_but,x,y, action):
    inactive_button = pygame.image.load(inactive_but)
    active_button = pygame.image.load(active_but)
    inactive_but_rect = inactive_button.get_rect()
    active_but_rect = active_button.get_rect()
    screen.blit(inactive_button,(x,y))

    cur = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x+inactive_but_rect.width > cur[0] > x and y+inactive_but_rect.height > cur[1] > y:
        screen.blit(active_button, (x,y))
        if click[0] == 1 and action != None:
            if action == "pause":
                paused()
            if action == "replay":
                gameLoop()
            if action == "main menu":
##                if play_music == True:
##                    pygame.mixer.music.load("track2.ogg")
##                    pygame.mixer.music.play(-1)
                game_intro()
    
def rat_spawn(FPS, total_frames, SCREEN_HEIGHT,rat_velx):
    half_second = FPS/2
    if total_frames % half_second == 0:
        rat = Rat("assets/rat.png",SCREEN_HEIGHT,grass_boundary, rat_velx)
        

def hawk_spawn(FPS, total_frames,SCREEN_WIDTH, SCREEN_HEIGHT):
    three_seconds = FPS * 3
    if total_frames % three_seconds == 0:
        if play_sfx == True:
            eagle.play()
        hawk = Hawk("assets/hawk.png", SCREEN_WIDTH, SCREEN_HEIGHT)

def sheild_spawn(SCREEN_WIDTH, SCREEN_HEIGHT, total_frames, FPS):
##        if play_sfx == True:
##            power_up.play()
    sheild = Sheild("assets/sheild.png", SCREEN_WIDTH, SCREEN_HEIGHT)

def rat_pp_spawn(SCREEN_WIDTH, SCREEN_HEIGHT, total_frames, FPS):
##        if play_sfx == True:
##            power_up.play()
    rat_pp = Rat_pp("assets/rat pp.png", SCREEN_WIDTH, SCREEN_HEIGHT)
        
def power_off():
    for sheild in Sheild.List:
        Sheild.remove(sheild)
        del sheild

def zoom(FPS, total_frames):
    for sheild in Sheild.List:
        if total_frames % (FPS/6) == 0:
            sheild.image  = pygame.image.load("assets/zoom sheild.png")
        else:
            sheild.image = pygame.image.load("assets/sheild.png")

    for rat_pp in Rat_pp.List:
        if total_frames % (FPS/6) == 0:
            rat_pp.image  = pygame.image.load("assets/rat pp zoom.png")
        else:
            rat_pp.image = pygame.image.load("assets/rat pp.png")
    
def rat_collide():
    for rat_1 in Rat.List:
        for rat_2 in Rat.List:
            if rat_1.rect.x + rat_1.rect.width == rat_2.rect.x:
                if rat_1.rect.y == rat_2.rect.y:
                    rat_1.image = pygame.image.load("assets/rat flipped.png")
                    rat_1.velx = -rat_1.velx

                    rat_2.direction = "left"
                    rat_2.image = pygame.image.load("assets/rat.png")
                    
def snake(snake_list, snake_body_size):
    if direction == "right":
        head = pygame.transform.rotate(snakehead, 270)
    if direction == "left":
        head = pygame.transform.rotate(snakehead, 90)
    if direction == "up":
        head = snakehead
    if direction == "down":
        head = pygame.transform.rotate(snakehead, 180)
        
        
    screen.blit(head,(snake_list[-1][0], snake_list[-1][1]))
    for XnY in snake_list[0:-1]:
        pygame.draw.rect(screen, GREEN,[XnY[0],XnY[1],snake_body_size,snake_body_size])
        

def paused():
    play_sfx = False
    if play_music:
        pygame.mixer.music.pause()
        pygame.mixer.music.load("track2.ogg")
        pygame.mixer.music.play(-1)
    else:
        pygame.mixer.music.stop()

    paused = True

    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.mixer.music.unpause()
                    paused = False

        screen.blit(paused_screen,(0,0))

        play_but_x = 330
        play_but_y = 200

        cur = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        inactive_button = pygame.image.load("assets/play button inactive.png")
        active_button = pygame.image.load("assets/play button active.png")
        inactive_but_rect = inactive_button.get_rect()
        active_but_rect = active_button.get_rect()
        screen.blit(inactive_button,(play_but_x,play_but_y))

        if play_but_x+inactive_but_rect.width > cur[0] > play_but_x and play_but_y + inactive_but_rect.height > cur[1] > play_but_y:
            screen.blit(active_button, (play_but_x,play_but_y))
            if click[0] == 1:
                pygame.mixer.music.unpause()
                paused = False

        button2("assets/replay button inactive.png","assets/replay button active.png",230,220,"replay")
        button2("assets/main menu inactive.png","assets/main menu active.png",450,220,"main menu")

        pygame.display.update()
        clock.tick(10)

def game_intro():
    intro = True
    
    while intro:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                    
        screen.blit(intro_page,(0,0))

        intro_button("PLAY", 300, 300,"assets/plaque.png", BLACK, LIGHT_GREEN, 30, "play")
        intro_button("CONTROLS", 300, 360,"assets/plaque.png", BLACK, YELLOW, 30, "controls")
        intro_button("ABOUT", 300, 420,"assets/plaque.png", BLACK, LIGHT_BLUE, 30, "about")
        intro_button("SETTINGS", 300, 480,"assets/plaque.png", BLACK, WHITE, 30, "settings")
        intro_button("QUIT", 300, 540,"assets/plaque.png", BLACK, LIGHT_RED, 30, "quit")

        pygame.display.update()

        clock.tick(10)

def game_controls():
    game_control = True
    while game_control:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                    
        screen.blit(bg2,(0,0))
        button2("assets/back button inactive.png","assets/back button active.png",0,0,"main menu")
        message_to_screen("Controls",-170,0,0, LIGHT_RED, 60,"ravie")

        message_to_screen("Welcome to Snake Escape. Increase your score by eating", -100,0,0, BLACK,29 )
        message_to_screen("as much mice as you can. Watch out for edges and hawks", -50,0,0, BLACK,29)
        message_to_screen("No matter what, do not run into your self. Got it???", 0,0,0, BLACK,29)
        message_to_screen("Lets Play!!!", 50,0,0, BLACK,29)
        message_to_screen("Move up-Up Arrow key      Move Down-Down Arrow key ",  150,0,0,BLUE,29)
        message_to_screen("Move Left-Left Arrow key      Move Right-Right Aroow key", 200,0,0, BLUE,27)
        message_to_screen("Pause-ESC                                                                   ", 250,0,0, BLUE,29)

        pygame.display.update()

        clock.tick(10)

def about():
    about = True

    while about:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                    
        screen.blit(bg2,(0,0))
        button2("assets/back button inactive.png","assets/back button active.png",0,0,"main menu")
        message_to_screen("ABOUT THE GAME",-170,0,0, LIGHT_RED, 40,"ravie")

        message_to_screen("Developed by Maxtech Software Development Company(MSDC)", -120,0,0, BLACK,27 )
        message_to_screen("CREDITS",-50,0,0, LIGHT_RED, 40, "ravie")
        message_to_screen("Special thanks to:", -10,0,0, BLACK,27)
        message_to_screen("George Kurobara Benjamin, Programming and Game Design", 30,0,0, BLACK,27)
        message_to_screen("Dreamstime Graphics, Graphics", 70,0,0, BLACK,27)
        message_to_screen("Also a big thank you to freinds, family", 110,0,0, BLACK,27)
        message_to_screen("and every one who cared", 150,0,0, BLACK,27)
        
        pygame.display.update()

        clock.tick(10)

def settings():
    settings = True

    while settings:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                    
        screen.blit(bg2,(0,0))
        
        button2("assets/back button inactive.png","assets/back button active.png",0,0,"main menu")
        message_to_screen("SETTINGS",-180,0,0, LIGHT_RED, 50,"ravie")

        message_to_screen("MUSIC",0,50,200, BLACK, 40,"ravie", False)
        message_to_screen("SFX",0,50,300, BLACK, 40,"ravie", False)
        message_to_screen("LEVEL",0,50,400, BLACK, 40,"ravie", False)
        toggle_button("ON", "OFF", 550, 200, "plaque.png", BLACK, 30, "music")
        toggle_button("ON", "OFF", 550, 300, "plaque.png", BLACK, 30, "sfx")
        toggle_button("DEFAULT", "EASY", 550, 400, "plaque.png", BLACK, 30, "level")
      
        pygame.display.update()

        clock.tick(10)

def mission_screen():
    global game_mission, mission_score, number_of_powerup, number_of_rats, number_of_hawk
    mission_screen = True

    #MISSIONS
    number_of_powerups_list = (2, 5, 10, 15)
    number_of_powerup = str(random.choice(number_of_powerups_list))

    score_lists = (1000, 1500, 2000, 2500, 3000, 3500, 4000, 5000, 7000)
    mission_score = str(random.choice(score_lists))

    number_of_rats_list = (7, 10, 15, 21, 25)
    number_of_rats = str(random.choice(number_of_rats_list))

    number_of_hawk_list = (5, 7, 12, 15, 20)
    number_of_hawk = str(random.choice(number_of_hawk_list))
    
    mission1 = "Get "+ mission_score+" points."
    mission2 = "Get " + number_of_powerup+" Power ups"
    mission3 = "Eat " + number_of_rats + " mice"
    mission4 = "Escape from "+ number_of_hawk+ " hawks"
    
    MISSIONS = (mission1, mission2, mission3, mission4)
    game_mission = random.choice(MISSIONS)
##    print game_mission
##    print number_of_rats
##    print number_of_powerup
##    print mission_score
##    print number_of_hawk

    while mission_screen:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
##            elif event.type == pygame.KEYDOWN:
##                if event.key == pygame.K_KP_ENTER:
##                    gameLoop()

        screen.blit(bg,(0,0))
        screen.blit(bg2,(0,0))
        
        message_to_screen("MISSION",-100,0,0, LIGHT_RED, 50,"ravie")
        message_to_screen(game_mission,0,0,0, BLACK, 50,"ravie")
        intro_button("START", 550, 500,"assets/plaque.png", BLACK, LIGHT_GREEN, 30, "gameplay")
        button2("assets/back button inactive.png","assets/back button active.png",0,0,"main menu")

        pygame.display.update()

        clock.tick(10)

        
def gameLoop():

    mission_completed = False
    number_of_hawks_passed = 0
    no_of_pp_gotten = 0

    #LEVEL
    if level == "easy":
        rat_velx = 3
        hawk_vel = 2
        score_mul = 10
    elif level == "medium":
        rat_velx = 15
        hawk_vel = 10
        score_mul = 30
    elif level == "hard":
        rat_velx = 20
        hawk_vel = 15
        score_mul = 50


#EMPTYING LISTS
    Hawk.List.empty()
    Sheild.List.empty()
    Rat_pp.List.empty()
    Rat.List.empty

#GLOBAL VARIABLES
    global direction
    direction = "right"

    #MUSIC
    if play_music == True:
        pygame.mixer.music.load("sound/gameplay_song.ogg")
        pygame.mixer.music.play(-1)
    else:
        pygame.mixer.music.stop()
        
    #SNAKE_DATA
    lead_x = SCREEN_WIDTH/2
    lead_y = SCREEN_HEIGHT/2
    snake_body_size = 15
    if level == "easy":
        snake_x_dis = 7
        snake_y_dis = 7
    elif level == "medium":
        snake_x_dis = 13
        snake_y_dis = 13
    elif level == "hard":
        snake_x_dis = 15
        snake_y_dis = 15

    snake_velx = snake_x_dis
    snake_vely = 0
    snake_list = []
    snake_length = 1

    #POWER UP

    sheild_obtained = False
    rat_pp_obtained = False

    powerup_list = ("sheild", "rat_pp")
    turn = random.choice(powerup_list)

    
    sheild_start_point = 0
    sheild_time_up = 0

    rat_pp_start_point = 0
    rat_pp_time_up = 0

    #GAME PROPS
    gameExit = False
    gameOver = False

    global total_frames

    
    while not gameExit:
        
        while gameOver:

##            pygame.mixer.music.load("track2.ogg")
##            pygame.mixer.music.play(-1)
##                        
            screen.blit(bg,(0,0))
            screen.blit(gameOver_sign, (50,0))
            if mission_completed == True:
                screen.blit(mission_complete, (100,50))
##                message_to_screen("BRAVO MISSION COMPLETED",-100,0,0, RED, 40,"ravie")
            button2("assets/replay button inactive.png","assets/replay button active.png",170,290,"replay")
            button2("assets/main menu inactive.png","assets/main menu active.png",510,290,"main menu")
            message_to_screen("YOUR SCORE",0,249,310, BLACK, 40,"stencil", False)
            message_to_screen(score,80,0,0, BLACK, 40,"stencil")
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
            pygame.display.update()
        
        rat_spawn(FPS, total_frames,SCREEN_HEIGHT, rat_velx)
##        rat_collide()
        hawk_spawn(FPS, total_frames, SCREEN_WIDTH, SCREEN_HEIGHT)
        
#POWER UP SPAWN
        #####Change this from total frames and set it to another variable
        for interval in powerup_spawn_intervals:
            if total_frames == interval:
                if turn == "sheild":
                    sheild_spawn(SCREEN_WIDTH, SCREEN_HEIGHT, total_frames, FPS)
                elif turn == "rat_pp":
                    rat_pp_spawn(SCREEN_WIDTH, SCREEN_HEIGHT, total_frames, FPS)
            
##            sheild_spawn(SCREEN_WIDTH, SCREEN_HEIGHT, total_frames, FPS)   
        zoom(FPS, total_frames)

#PROCESSES
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and direction != "right":
                    direction = "left"
                    snake_velx = -snake_x_dis
                    snake_vely = 0
                    
                elif event.key == pygame.K_RIGHT and direction != "left":
                    direction = "right"
                    snake_velx = snake_x_dis
                    snake_vely = 0
                    
                elif event.key == pygame.K_UP and direction != "down":
                    direction = "up"
                    snake_vely = -snake_y_dis
                    snake_velx = 0
                    
                elif event.key == pygame.K_DOWN and direction != "up":
                    direction = "down"
                    snake_vely = snake_y_dis
                    snake_velx = 0

                elif event.key == pygame.K_ESCAPE:
                    paused()

        #LOGIC
        score = (snake_length - 1)*score_mul
        
        if total_frames % (FPS * 3) == 0:
            number_of_hawks_passed+=1
         
        if "points" in game_mission:
            if int(score) >= int(mission_score):
                mission_completed = True
             
        elif "Power ups" in game_mission:
            if int(no_of_pp_gotten) >= int(number_of_powerup):
                mission_completed = True
                
        elif "mice" in game_mission:
            if int(score) / score_mul >= int(number_of_rats):
                mission_completed = True
           
        elif "hawk" in game_mission:
            if number_of_hawks_passed >= int(number_of_hawk):
                mission_completed = True
       
                    
        #CROSSING THE BOUNDARY            
        if lead_x + snake_body_size > ((SCREEN_WIDTH - grass_boundary) + snake_body_size) or lead_x < grass_boundary or lead_y + snake_body_size > ((SCREEN_HEIGHT - grass_boundary) + snake_body_size) or lead_y < grass_boundary:
            gameOver = True
        lead_x+=snake_velx
        lead_y+=snake_vely
        
        Rat.motion(SCREEN_WIDTH)
        Hawk.hawk_motion(SCREEN_WIDTH,SCREEN_HEIGHT)

        #UPDATIGN THE SNAKELENGTH
        snakeHead = []
        snakeHead.append(lead_x)
        snakeHead.append(lead_y)
        snake_list.append(snakeHead)
        if len(snake_list) > snake_length:
            del snake_list[0]

        #EATING THE RAT
        for rat in Rat.List:
            if lead_x > rat.rect.x and lead_x < rat.rect.x + rat.rect.width or lead_x + snake_body_size > rat.rect.x  and lead_x + snake_body_size < rat.rect.x + rat.rect.width:
                if lead_y > rat.rect.y and lead_y < rat.rect.y + rat.rect.width or lead_y + snake_body_size > rat.rect.y and lead_y + snake_body_size < rat.rect.y + rat.rect.height:
                    Rat.List.remove(rat)
                    del rat
                    snake_length +=1

        #SNAKE DEATH - RUNNING INTO YOURSELF
        for eachSegment in snake_list[:-1]:
            if eachSegment == snakeHead:
                gameOver = True

        #CAUGHT BY A HAWK
        for hawk in Hawk. List:
            for snake_pos in snake_list:
                if snake_pos[0] > hawk.rect.x and snake_pos[0] < hawk.rect.x + hawk.rect.width :
                    if snake_pos[1] > hawk.rect.y and snake_pos[1] < hawk.rect.y + hawk.rect.height:
                        if sheild_obtained == False:
                            gameOver = True


#SHEILD COLLECTION
##        #SHEILD TIME UP
##        sheild_items = len(Sheild.List)
##        if sheild_items > 0:
##            sheild_time_up +=1
##            if sheild_time_up > 0 and sheild_time_up % (FPS * 5)== 0:
##                power_off()
##                sheild_time_up = 0

        if turn == "sheild":                    
            for sheild in Sheild.List:
                if lead_x > sheild.rect.x and lead_x < sheild.rect.x + sheild.rect.width or lead_x + snake_body_size > sheild.rect.x  and lead_x + snake_body_size < sheild.rect.x + sheild.rect.width:
                    if lead_y > sheild.rect.y and lead_y < sheild.rect.y + sheild.rect.width or lead_y + snake_body_size > sheild.rect.y and lead_y + snake_body_size < sheild.rect.y + sheild.rect.height:
                        sheild_obtained = True

                if sheild_obtained == True:
                    sheild.rect.center = lead_x, lead_y
                    if sheild_start_point % (FPS * 5) == 0:
                        Sheild.List.remove(sheild)
                        del sheild
                        sheild_start_point = 0
                        sheild_obtained = False
                        no_of_pp_gotten+=1
##                        print no_of_pp_gotten
                sheild_start_point += 1


            for sheild in Sheild.List:
                sheild.timer +=1
    ##            print sheild.timer
                if sheild.timer == 120 and sheild_obtained == False:
                    Sheild.List.remove(sheild)
                    del sheild
##                    power_up_due = 0
            
        

#RAT POWERUP COLLECTION

        #RAT PP TIME UP
        elif turn == "rat_pp":
            for rat_pp in Rat_pp.List:
                if lead_x > rat_pp.rect.x and lead_x < rat_pp.rect.x + rat_pp.rect.width or lead_x + snake_body_size > rat_pp.rect.x  and lead_x + snake_body_size < rat_pp.rect.x + rat_pp.rect.width:
                    if lead_y > rat_pp.rect.y and lead_y < rat_pp.rect.y + rat_pp.rect.width or lead_y + snake_body_size > rat_pp.rect.y and lead_y + snake_body_size < rat_pp.rect.y + rat_pp.rect.height:
                        rat_pp_obtained = True
                        print rat_pp_obtained
                        Rat_pp.List.remove(rat_pp)
                        del rat_pp

                if rat_pp_obtained == True:
                    rat_pp.timeup +=1
                    print rat__p.timeup
                    rat_velx = (rat_velx/2)
##                    rat_pp_start_point += 1
##                    print rat_pp_start_point
                    if rat_pp.timeup == (FPS * 2) == 0:
                        rat_velx = (rat_velx*2)
##                        rat_pp_start_point = 0
                        rat_pp_obtained = False
                        no_of_pp_gotten+=1
##                        print no_of_pp_gotten

            for rat_pp in Rat_pp.List:
                rat_pp.timer +=1
##                print rat_pp.timer
                if rat_pp.timer == 90 and rat_pp_obtained == False:
                    Rat_pp.List.remove(rat_pp)
                    del rat_pp

        #LOGIC
##        start_point +=1
##        print start_point
        total_frames+=1
##        print total_frames

        #DRAWING
        screen.blit(background,(0,0))
        Rat.List.draw(screen)
        snake(snake_list, snake_body_size)
        Sheild.List.draw(screen)
        Rat_pp.List.draw(screen)
        screen.blit(grass,(2,2))
        Hawk.List.draw(screen)
        button2("assets/pause button inactive.png","assets/pause button active.png",0,0,"pause")

        #DISPLAYING SCORE
        screen.blit(score_board,(550,5))
        score = str(score)
        message_to_screen(score, 0,680,5, BLACK,30,"franklingothicmedium",False)
        
        #DRAWING
        pygame.display.update()
    

        clock.tick(FPS)

if play_music == True:
    pygame.mixer.music.load("sound/track2.ogg")
    pygame.mixer.music.play(-1)
else:
    pygame.mixer.music.stop()

     
game_intro()
gameLoop()
pygame.quit()
quit()
