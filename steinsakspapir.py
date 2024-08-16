import pygame
# import time
import os

pygame.init()


# COLOUR
BLACK = (0, 0, 0)
WHITE = (250, 250, 250)
RED = (250, 0, 0)
GREEN = (255, 255, 0)
BLUE = (0, 0, 250)


W = 1200
H = 800
run = True
clock = pygame.time.Clock()
time = clock.get_time()
event = pygame.event.get()
screen = pygame.display.set_mode((W,H))
player_list = []
nr_players = 2
i = 0


BASE = 'Brukere\Erling\Skrivebord\Programming\lek og moro'

# def get_image(path):
    # return pygame.image.load( os.path.join(BASE, path) ).convert_alpha()

# saks = get_image('saks.png').convert()
# rock = get_image('rock.png').convert()
# hand = get_image('hand.png').convert()

# pos = pygame.mouse.get_pos()

# spisetid_1 = time.time()+1

score = 0
game_win = False

img_size = (W/4,H/4)

left = (100, H/3)
right = (W-W/3, H/3)



hand = pygame.image.load("hand.png").convert()
rock = pygame.image.load("rock.png").convert()
saks = pygame.image.load("saks.png").convert()
player1 = pygame.image.load("PLAYER1.png").convert()
player2 = pygame.image.load("PLAYER2.png").convert()

                
def draw_text(text, x, y):
    text_col = WHITE
    font = pygame.font.SysFont("None", 50)
    img = font.render(text, True, text_col)
    screen.blit(img, (x,y))

def draw_text_cent(text):
    text_col = WHITE
    font = pygame.font.SysFont("None", 100)
    img = font.render(text, True, text_col)
    text_rect = img.get_rect(center=(W/2, 100))
    screen.blit(img,text_rect)    
    
def draw_controls():
    draw_text('Z = STEIN', 100, H-250) 
    draw_text('X = SAKS', 100, H-200)
    draw_text('C = PAPIR', 100, H-150)
    draw_text('1 = STEIN', 900, H-250)
    draw_text('2 = SAKS', 900, H-200)
    draw_text('3 = PAPIR', 900, H-150)
    
    for player_score in player_list:
            player_score.show_score(player_score.side)
    
def image_size_left(image):
    return pygame.transform.scale(image, img_size)
    # return pygame.transform.flip(image,True, False)

def image_size_right(image):
    return pygame.transform.scale(image, img_size)

def player_win(spiller, spiller2):
    if spiller.game_win == True and spiller2.game_win == False:
        if spiller.side == left:
            pygame.draw.rect(screen, BLACK, (0,0,W,H))
            draw_controls()
            draw_text_cent(' LEFT IS SIGMA, RIGHT U SOY >:)')
            pygame.display.flip()
            pygame.time.delay(3000)
            reset_score(player_list[0],player_list[1])
            player_list[0].choice_ready = False
            player_list[1].choice_ready = False      
        else:
            pygame.draw.rect(screen, BLACK, (0,0,W,H))
            draw_controls()
            draw_text_cent('LEFT IS SIGMA, LEFT U SOY >:)')  
            pygame.display.flip()
            pygame.time.delay(3000)
            reset_score(player_list[0],player_list[1])
            player_list[0].choice_ready = False
            player_list[1].choice_ready = False    
                 

def reset_score(spiller, spiller2):
    spiller.score = 0
    spiller.weapon = player1
    spiller2.score = 0
    spiller2.weapon = player2
            
def blip_player_screen():
    screen.blit(image_size_left(player_list[0].weapon), player_list[0].side)
    screen.blit(image_size_right(player_list[1].weapon), player_list[1].side)     
    draw_controls()

def blip_weapon():
    if player_list[0].weapon == player1 and player_list[1].weapon == player2:
        screen.blit(image_size_left(player_list[0].weapon), player_list[0].side)
        screen.blit(image_size_right(player_list[1].weapon), player_list[1].side)     
        draw_controls() 
        
    if player_list[0].choice_ready == True  and player_list[1].choice_ready == True:
        screen.blit(image_size_left(player_list[0].weapon), player_list[0].side)
        screen.blit(image_size_right(player_list[1].weapon), player_list[1].side)
        draw_controls()
        pygame.display.flip()
        pygame.time.delay(3000)
        player_list[0].choice_ready = False
        player_list[1].choice_ready = False        
        player_list[0].weapon = player1
        player_list[1].weapon = player2
        
    if player_list[0].choice_ready == True or player_list[1].choice_ready == True:
        draw_controls()
        for player in player_list:
            if player.choice_ready == True:
                draw_text('Player ' + str(player.number) + ' READY', W/3, H/2)  
                
def battle_comp():
    for play in player_list:
        for play2 in player_list:
            if play == play2:
                continue
            if play.choice_ready == True and play2.choice_ready == True:
                play.battle(play2)
                # play.show_score(play.side)
                 
                # player_win(play, play2)
                play.winner()

class spiller:
    def __init__(self, score, game_win, side, weapon, number):
        self.score = score
        self.game_win = game_win
        self.side = side
        self.weapon = weapon
        self.number = number
        # self.memory_list = [1]
        # self.key_memory = 0
        # self.key_inputs = 0
        # self.key_pressed_up = False
        self.choice_ready = False
        
    def side_spawn(self):
        if self.side == right:
            self.weapon.get_rect(center=(right))
        else:
            self.weapon.get_rect(center=(left))
            
    def battle(self, comp):
        if self.choice_ready == True and comp.choice_ready == True:
            if self.weapon == rock and comp.weapon == saks:
                self.win()
            if self.weapon == saks and comp.weapon == hand:
                self.win()
            if self.weapon == hand and comp.weapon == rock:
                self.win()

    
    def win(self):
            self.score += 1
            self.lost_game()
        
    def weapon_choice(self, weapon):
        self.weapon = weapon
        # if self.weapon != self.memory_list[0]:
        #     self.memory_list.pop()
        # if self.weapon != player1 or player2 and len(self.memory_list) < 1:
        #     self.memory_list.append(weapon)
        
        
    def winner(self):
        if self.score == 3:
            self.game_win = True
            if self.side == left:
                pygame.draw.rect(screen, BLACK, (0,0,W,H))
                draw_controls()
                draw_text_cent('LEFT IS SIGMA, RIGHT U SOY >:)')
                screen.blit(image_size_left(player_list[0].weapon), player_list[0].side)
                screen.blit(image_size_right(player_list[1].weapon), player_list[1].side)   
                pygame.display.flip()
                pygame.time.delay(5000)
                reset_score(player_list[0],player_list[1])
                player_list[0].choice_ready = False
                player_list[1].choice_ready = False
                   
            else:
                pygame.draw.rect(screen, BLACK, (0,0,W,H))
                draw_controls()
                draw_text_cent('RIGHT IS SIGMA, LEFT U SOY >:)')
                screen.blit(image_size_left(player_list[0].weapon), player_list[0].side)
                screen.blit(image_size_right(player_list[1].weapon), player_list[1].side)    
                pygame.display.flip()
                pygame.time.delay(5000)
                reset_score(player_list[0],player_list[1])
                player_list[0].choice_ready = False
                player_list[1].choice_ready = False   
        else:
            self.lost_game()
      
    def lost_game(self):
        self.game_win = False        
            
    def show_score(self,side):
        if side == left:
            draw_text(str(self.score),300, H/4)
        else:
            draw_text(str(self.score), W-300, H/4)
            
    def calculate(self, i):
        if i == 1:
            self.side = left
            self.weapon = player1
        else:
            self.side = right
            self.weapon = player2
        
def choose_your_weapon():
    keys = pygame.key.get_pressed()
    if keys[pygame.K_z]:
        player_list[0].weapon_choice(rock)
        player_list[0].choice_ready = True
    if keys[pygame.K_x]:
        player_list[0].weapon_choice(saks)
        player_list[0].choice_ready = True
    if keys[pygame.K_c]:
        player_list[0].weapon_choice(hand)
        player_list[0].choice_ready = True

    if keys[pygame.K_KP1]:
        player_list[1].weapon_choice(rock)
        player_list[1].choice_ready = True
    if keys[pygame.K_KP2]:
        player_list[1].weapon_choice(saks)
        player_list[1].choice_ready = True
    if keys[pygame.K_KP3]:
        player_list[1].weapon_choice(hand)
        player_list[1].choice_ready = True

while run:



    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        pos = pygame.mouse.get_pos()

        
    if event.type == pygame.MOUSEBUTTONDOWN:
        nedtrykk = True
    if event.type == pygame.MOUSEBUTTONUP:
        nedtrykk = False
        
    if event.type == pygame.KEYUP:
        pass

    
    while i < nr_players:
        i += 1
        spiller_nr = spiller(score, game_win, None, None, i)
        spiller_nr.calculate(i)
        player_list.append(spiller_nr)
        
        
    choose_your_weapon()

        
    # if pos[0] in range(ball_pos.x , ball_pos.x + ball_pos.w) :
    #     if pos[1] in range(ball_pos.y, ball_pos.y + ball_pos.h):
    #         None

    # if nedtrykk == True:   
    #     draw_list.append((pos[0], pos[1]))
    
    # for drawings in draw_list:
    #     pygame.draw.circle(screen, colour_pen, drawings, 1)
    

    
    pygame.draw.rect(screen, BLACK, (0,0,W,H)) 

    draw_text_cent('STEIN SAKS PAPIIR 3000')
    # draw_controls()

    battle_comp()
    blip_weapon()  


    # battle_comp()
    pygame.display.flip()



    
    # draw_controls()
    
    clock.tick(20)



    pygame.display.flip()
pygame.quit()

