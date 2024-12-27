"""
Author: Jose L Balcazar, ORCID 0000-0003-4248-4528 
Copyleft: MIT License (https://en.wikipedia.org/wiki/MIT_License)

Headers for functions in abstract board for simple tic-tac-toe-like games, 2021.
Intended for Grau en Intel-ligencia Artificial, Programacio i Algorismes 1.
I would prefer to do everything in terms of object-oriented programming though.
"""

# Import: 
# color GRAY; PLAYER_COLOR, NO_PLAYER
# board dimension BSIZ
from constants import PLAYER_COLOR, BSIZ, NO_PLAYER, GRAY, ST_PLAYER

# Data structure for stones
from collections import namedtuple
import time
#  exemple de stone: Stone(1, 2, PLAYER_COLOR[0])
Stone = namedtuple('Stone', ('x', 'y', 'color'))


def set_board_up(stones_per_player = ST_PLAYER):
    'Init stones and board, prepare functions to provide, act as their closure'
    # init board and game data here

    board_matrix = [[NO_PLAYER for _ in range(BSIZ)] for _ in range(BSIZ)]
    played_stones = list()
    unplayed_stones = list()
    current_player = 0
    
    #  creem 4 pedres per jugador, i les afegim a la llista de pedres no jugades, alternant colors:
    for _ in range(stones_per_player):
        unplayed_stones.append(Stone(0, 0, PLAYER_COLOR[0]))
        unplayed_stones.append(Stone(0, 0, PLAYER_COLOR[1]))

    #  seleccionem la primera pedra
    selected_stone: Stone

    def stones() -> list:
        "return iterable with the stones already played"
        return played_stones

    def select_st(i, j):
        '''
        Select stone that current player intends to move. 
        Player must select a stone of his own.
        To be called only after all stones played.
        Report success by returning a boolean;
        '''
        nonlocal selected_stone

        for stone in played_stones:
            #  comprovem quina pedra s'ha premut (comparant les coordenadas donades) i que sigui del jugador actual
            if stone.x == i and stone.y == j and stone.color == PLAYER_COLOR[current_player]:
                #  si ho és, la guardem com a selected_stone
                selected_stone = stone
        
        return selected_stone

    def end() -> bool:
        'Test whether there are 3 aligned stones'
      #  en les files:
        for x in range(len(board_matrix)):
            for y in range(len(board_matrix)-2):
                if board_matrix[x][y] == board_matrix[x][y+1] == board_matrix[x][y+2] != NO_PLAYER:
                    return current_player + 1
        
        #  en les columnes:
        for y in range(len(board_matrix)):
            for x in range(len(board_matrix)-2):
                if board_matrix[x][y] == board_matrix[x+1][y] == board_matrix[x+2][y] != NO_PLAYER:
                    return current_player + 1
    
       #  en la diagonal:
        for x in range(len(board_matrix)-2):
            for y in range(len(board_matrix)-2):
                if board_matrix[x][y] == board_matrix[x+1][y+1] == board_matrix[x+2][y+2] != NO_PLAYER:
                    return current_player + 1
        
        #  en la antidiagonal:
        for x in range(len(board_matrix)-2):
            for y in range(len(board_matrix)-2):
                if board_matrix[x][y+2] == board_matrix[x+1][y+1] == board_matrix[x+2][y]  != NO_PLAYER:
                    return current_player + 1
        return 0
    
    def move_st(i, j):
        '''If valid square, move there selected stone and unselect it,
        then check for end of game, then select new stone for next
        player unless all stones already played;
        if square not valid, do nothing and keep selected stone.
        Return 3 values: bool indicating whether a stone is
        already selected, current player, and boolean indicating
        the end of the game.
        '''
        nonlocal selected_stone, played_stones, unplayed_stones, current_player

        #  comprovem si la casella on volem col·locar la pedra està dins del tauler o si està ocupada per una altra:
        if i < 0 or i > (BSIZ - 1) or j < 0 or j > (BSIZ - 1) or board_matrix[i][j] != NO_PLAYER:
            return True, current_player, False
        
        #  afegim el jugador de la pedra seleccionada a la matriu del tauler:
        board_matrix[i][j] = current_player
        

        if len(played_stones) >= stones_per_player * 2:
            #  si ja s'han jugat totes les pedres, eliminem les dades anteriors de la pedras seleccionada:
            board_matrix[selected_stone.x][selected_stone.y] = NO_PLAYER
            played_stones.remove(selected_stone)
        
        else:
            #  si no, seleccionem automaticament la següent pedra:
            selected_stone = unplayed_stones.pop(0)
        
        #  actualitzem les coordenades de la pedra seleccionada i l'afegim a la llista de pedres jugades:
        selected_stone = selected_stone._replace(x = i, y = j)
        played_stones.append(selected_stone)
        selected_stone = 0

        #  comprovem si algun jugador ha guanyat, en cas que sigui possible (si hi ha més de 4 pedres jugades):
        if len(played_stones)>4:
            fi = end()
        else:
            fi = False

        #  Canviem de jugador:
        current_player = (current_player + 1) % 2

        #  retornem els valors:
        return len(played_stones) < stones_per_player*2, current_player, fi

    def draw_txt(x):
        'Use ASCII characters to draw the board.'
        #  funció del main txt
        for i in range(len(board_matrix)):
            
            for j in range(len(board_matrix[i])):
                print(" ", end="")
                
                if board_matrix[i][j] == NO_PLAYER:
                    print(" ", end="")
                
                elif board_matrix[i][j] == 0:
                    print("X", end="")
                
                else:
                    print("O", end="")
                
                if j < 2:
                    print(" ", end="")
                    print("|", end="")
            print()
            
            if i < 2:
                print("---+---+---")

    #  return these 4 functions to make them available to the main program
    return stones, select_st, move_st, draw_txt
