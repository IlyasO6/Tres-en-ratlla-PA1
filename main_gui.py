"""
Author: Jose L Balcazar, ORCID 0000-0003-4248-4528 
Copyleft: MIT License (https://en.wikipedia.org/wiki/MIT_License)

Pygame-based handling of a simple tic-tac-toe-like board, 2021.
Intended for Grau en Intel-ligencia Artificial, Programacio i Algorismes 1.
"""

# Import library for game programming 
import pygame

# Import: colors BLACK, GRAY, WHITE, PLAYER_COLOR; 
#         board dimensions BSIZ, WIDTH, HEIGHT, SLOT, SEP, ROOM, RAD
from constants import *

# Initialize the game engine, indicate a caption and
# set the height and width of the screen.
pygame.init()
screen = pygame.display.set_mode( (WIDTH, HEIGHT) )
pygame.display.set_caption("Tres en ratlla")
clock = pygame.time.Clock() 
FONT_TITLE1 = pygame.font.SysFont('Verdana', 50)
FONT_TITLE2 = pygame.font.SysFont('Calibri', 28)
# Import initialization of the separately programmed abstract board:
from abs_board_h import set_board_up

# Prepare board:
# this will set up all stones as unplayed, select a first stone to play,
# and obtain functions to handle them as follows:
#   the call stones() allows one to loop on all stones,
#   the call select_st(i, j) marks as selected the stone at these coordinates,
#   the call move_st(i, j) 
#     if the square at these coordinates is free, moves the selected  
#     stone there, changes player, unselects the stone and checks for 
#     end of game; otherwise, does nothing, leaving the stone selected;
#     returns: bool "stone still selected", next player (may be the same), 
#     and bool "end of game"
#   the call to draw_txt(end) prints a text-based version of the board
stones, select_st, move_st, draw_txt = set_board_up()

# Grid:
def trans_coord(x, y):
    'translates pixel coordinates into board coordinates'
    return round((x - ROOM - SEP - 0.5*SLOT)/(SEP + SLOT)), round((y - SEP - 0.5*SLOT)/(SEP + SLOT))

def draw_square(screen, i, j):
    pygame.draw.polygon(screen, GRAY,
        ( (ROOM + SEP + i*(SLOT + SEP), SEP + j*(SLOT + SEP)),
          (ROOM + SEP + i*(SLOT + SEP) + SLOT, SEP + j*(SLOT + SEP)),
          (ROOM + SEP + i*(SLOT + SEP) + SLOT, SEP + j*(SLOT + SEP) + SLOT),
          (ROOM + SEP + i*(SLOT + SEP), SEP + j*(SLOT + SEP) + SLOT)
        ))

def draw_stone(screen, i, j, color):
    pygame.draw.circle(screen, color, 
        (ROOM + 0.5*SEP + (i + 0.5)*(SLOT + SEP), 0.5*SEP + (j + 0.5)*(SLOT + SEP)), 
        RAD)

def draw_board(curr_player = 0, end = False):
    'on fresh screen, draw grid, stones, player turn mark, then make it appear'
    screen.fill(WHITE if not end else (55, 55, 55))
    for i in range(BSIZ):
        for j in range(BSIZ):
            draw_square(screen, i, j)
    for s in stones():
        draw_stone(screen, *s)
    if not end:
        'colored rectangle indicates who plays next'
        width = BSIZ*(SEP + SLOT) - SEP
        height = SLOT
        x = ROOM + SEP
        y = BSIZ*(SEP + SLOT) + SEP
        pygame.draw.rect(screen, PLAYER_COLOR[curr_player], (x, y, width, height))


    pygame.display.flip()

def draw_game_over():
    #  rectangle de Game Over (el mateix que el que mostrava el torn)
    width = BSIZ*(SEP + SLOT) - SEP
    height = SLOT
    x = ROOM + SEP
    y = BSIZ*(SEP + SLOT) + SEP
    pygame.draw.rect(screen, (255, 255, 255), (x, y, width, height) )

    #  botó de New Game
    new_game_x = x + 100
    new_game_y = y + 65
    new_game_width = width - 200
    new_game_height = height - 70
    pygame.draw.rect(screen, (100, 100, 100), (new_game_x, new_game_y, new_game_width, new_game_height))

    screen.blit(FONT_TITLE1.render("GAME OVER", True, (0, 0, 0)), (x + 15, y))
    screen.blit(FONT_TITLE2.render("New Game", True, (255, 255, 255)), (x + 107, y + 68))
    pygame.display.flip()

    return new_game_x, new_game_y, new_game_width, new_game_height


# set_board_up() already selects a first stone; set curr_player to zero.
stone_selected = True
curr_player = 0

# Show grid and stones:
draw_board()

# Loop until the user clicks the close button.
done = False

# Play until game ends
end = False

while not done:
    
    # This limits the while loop to a max of 10 times per second.
    # Leave this out and we will use all CPU we can.
    clock.tick(10)
    
    for event in pygame.event.get(): 
        "User did something"
        if event.type == pygame.QUIT:
            "User clicked 'close window', set flag to exit loop"
            done = True
        if event.type == pygame.MOUSEBUTTONDOWN and not end:
            "game is afoot and user clicked something"
            if stone_selected:
                "User should click on a free destination square, otherwise ignore event"
                stone_selected, curr_player, end = move_st(*trans_coord(*event.pos))
                draw_board(curr_player, end)
            else:
                "User should click on a stone to select it"
                stone_selected = select_st(*trans_coord(*event.pos))
        
        if end: 
            run = True
            while run:
                clock.tick(10)
                x, y, width, height = draw_game_over()

                mouse = pygame.mouse.get_pos()

                for event in pygame.event.get():
                    
                    if event.type == pygame.QUIT:
                        "User clicked 'close window', set flag to exit loop"
                        done = True
                        run = False
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        "game is afoot and user clicked something"

                        #  si ha fet click al botó de New Game:
                        if x <= mouse[0] <= x + width and y <= mouse[1] <= y + height:
                            stones, select_st, move_st, draw_txt = set_board_up() #  reinicia tot
                            draw_board()
                            end = False
                            run = False

# Friendly finish-up:
pygame.quit()
