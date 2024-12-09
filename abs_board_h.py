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

    board_matrix = [[0 for _ in range(3)] for _ in range(3)]
    played_stones = []
    unplayed_stones = []
    current_player = 0
    for _ in range(stones_per_player):
        #creem 4 pedres per jugador, i les afegim a la llista de pedres no jugades, alternant colors
        unplayed_stones.append(Stone(0, 0, PLAYER_COLOR[0]))
        unplayed_stones.append(Stone(0, 0, PLAYER_COLOR[1]))
        #com estem guardant les pedres a 0, 0 haurem de traduir les coodenades (en x,y aniran de 1 a 3 y en i,j de 0 a 2)

    #seleccionem la primera pedra
    selected_stone = unplayed_stones[0]
    #iniciem un contador de torns jugats
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
        #S'executa aquesta funció quan totes les pedres ja estan jugades
        nonlocal played_stones, selected_stone

        for stone in played_stones:
            #comprovem que la pedra en la posició i,j seleccionada sigui del jugador actual
            if stone.x == i and stone.y == j and stone.color == PLAYER_COLOR[current_player]:
                #si ho és, la guardem com a selected_stone
                selected_stone = stone
        return selected_stone

    def end() -> bool:
        'Test whether there are 3 aligned stones'
        winner = False
        #busquem diagonal
        for i in range(len(board_matrix)):
            if board_matrix[i][i]==current_player+1:
                winner = True
            else:
                winner = False
                break
        #busquem antidiagonal
        if not winner:
            for i in range(len(board_matrix)):
                if board_matrix[i][-1-i]==current_player+1:
                    winner = True
                else:
                    winner = False
                    break
        #busquem columnes
        for y in range(len(board_matrix)):
            if board_matrix[0][y]==board_matrix[1][y]==board_matrix[2][y]==current_player+1:
                winner = True
        #busquem files
        for x in range(len(board_matrix)):
            if board_matrix[x][0]==board_matrix[x][1]==board_matrix[x][2]==current_player+1:
                winner = True
        return winner
        

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
        #comprovem si la casella on volem col·locar és vàlida
        if i < 0 or i > 2 or j < 0 or j > 2:
            return True, current_player, False
        
        #comprovem si la casella on volem col·locar està ocupada
        for stones in played_stones:
            #agafa els valors de la llista played_stones retornada per stones().
            if stones.x == i and stones.y == j:
                #busca una pedra a la posicio i,j
                return True, current_player, False
                #stone_selected es True, curr_player es current_player, end es False

        #Quan ja hem comporvat que la pedra seleccionada és vàlida i la casella seleccionada està lliure
        if turn > 7:
            #Treiem la pedra de la llista de pedres jugades
            played_stones.remove(selected_stone)
        #Afegim la pedra a la llista de pedres jugades amb les noves coordenades
        selected_stone = selected_stone._replace(x = i, y = j)
        played_stones.append(selected_stone)
        
        #  afegim la pedra a 
        board_matrix[i][j] = current_player+1
        #comprovem si el jugador actual ha guanyat i guardem el resultat de end()
        fi = end()
        #Canviem de jugador
        current_player = (current_player + 1) % 2
        #quan encara no estan totes les pedres jugades
        if turn < 7:
            #eliminem de la llista de pedres no jugades la primera pedra, si encara no estan totes les pedres jugades
            unplayed_stones.pop(0)
            #seleccionem la següent pedra de la llista
            selected_stone = unplayed_stones[0]
        else:
            #ja estan totes les pedres col·locades
            selected_stone = 0
            #canviem el torn i retornem
            turn += 1
            return False, current_player, fi
        #canviem el torn i retornem
        turn += 1
        return True, current_player, fi

    def draw_txt(end = False):
        'Use ASCII characters to draw the board.'
        #funcion del main txt
        pass

    # return these 4 functions to make them available to the main program
    return stones, select_st, move_st, draw_txt
