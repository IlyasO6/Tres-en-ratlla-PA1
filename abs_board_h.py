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
from constants import PLAYER_COLOR, BSIZ, NO_PLAYER, GRAY

# Data structure for stones
from collections import namedtuple

#  exemple de stone: Stone(1, 2, PLAYER_COLOR[0])
Stone = namedtuple('Stone', ('x', 'y', 'color'))


def set_board_up(stones_per_player = 4):
    'Init stones and board, prepare functions to provide, act as their closure'
    # init board and game data here

    board_matrix = [[0 for _ in range(BSIZ)] for _ in range(BSIZ)]
    played_stones = []
    unplayed_stones = []
    current_player = 0
    
    #  creem 4 pedres per jugador, i les afegim a la llista de pedres no jugades, alternant colors:
    for _ in range(stones_per_player):
        unplayed_stones.append(Stone(0, 0, PLAYER_COLOR[0]))
        unplayed_stones.append(Stone(0, 0, PLAYER_COLOR[1]))
        #  com estem guardant les pedres a 0, 0 haurem de traduir les coodenades (en x,y aniran de 1 a 3 y en i,j de 0 a 2)

    #  seleccionem la primera pedra
    selected_stone = unplayed_stones[0]
    
    #  iniciem un contador de torns jugats
    turn = 0

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
            if board_matrix[x][0] == board_matrix[x][1] == board_matrix[x][2] == current_player + 1:
                return True
        
        #  en les columnes:
        for y in range(len(board_matrix)):
            if board_matrix[0][y] == board_matrix[1][y] == board_matrix[2][y] == current_player + 1:
                return True
    
        #  en la diagonal:
        if board_matrix[0][0] == board_matrix[1][1] == board_matrix[2][2] == current_player + 1:
            return True
        
        #  en la antidiagonal:
        if board_matrix[0][2] == board_matrix[1][1] == board_matrix[2][0]  == current_player + 1:
            return True

        return False
    
    def move_st(i, j):
        '''If valid square, move there selected stone and unselect it,
        then check for end of game, then select new stone for next
        player unless all stones already played;
        if square not valid, do nothing and keep selected stone.
        Return 3 values: bool indicating whether a stone is
        already selected, current player, and boolean indicating
        the end of the game.
        '''
        nonlocal selected_stone, played_stones, unplayed_stones, current_player, turn
        
        #  comprovem que s'ha premut dins del tauler:
        if i < 0 or i > (BSIZ - 1) or j < 0 or j > (BSIZ - 1):
            return True, current_player, False
        
        #  comprovem si la casella on volem col·locar està ocupada comparant cada pedra de les jugades amb les
        #  coordenades de la casella

        for stones in played_stones:
            if stones.x == i and stones.y == j:
                return True, current_player, False

        #  Quan ja hem comprovat que la pedra seleccionada és vàlida i la casella seleccionada està lliure,
        #  afegim la pedra a la matriu del tauler i a la llista de pedres jugades amb les noves coordenades:
        board_matrix[i][j] = current_player + 1
        
        
        if turn > (stones_per_player * 2) - 1: 
            board_matrix[selected_stone.x][selected_stone.y] = 0
            played_stones.remove(selected_stone)
        
        selected_stone = selected_stone._replace(x = i, y = j)
        played_stones.append(selected_stone)
        
        #  quan encara no estan totes les pedres jugades:
        if turn < (stones_per_player * 2) - 1:
            unplayed_stones.pop(0) #  eliminem de la llista de pedres no jugades la primera pedra
            selected_stone = unplayed_stones[0] #  seleccionem la següent pedra de la llista
        
        else: #  ja estan totes les pedres col·locades, per tant ja no seleccionem manualment
            selected_stone = 0

        #  comprovem si algun jugador ha guanyat:
        fi = end()

        #  Canviem de jugador i aumentem el torn:
        current_player = (current_player + 1) % 2
        turn += 1

        #  retornem els valors:
        return selected_stone, current_player, fi

    def draw_txt(end = False):
        'Use ASCII characters to draw the board.'
        #  funcion del main txt
        pass

    #  return these 4 functions to make them available to the main program
    return stones, select_st, move_st, draw_txt
