import numpy as np
from board import Board
from classes import Color
from moves import get_best_moveAB

# KingSide White Castle
pboard = [['_' '_' '_' '_' '_' '_' '_' '_'],
        ['_' '_' '_' '_' '_' '_' '_' 'p'],
        ['_' '_' '_' '_' '_' '_' '_' '_'],
        ['_' 'p' '_' '_' '_' '_' '_' '_'],
        ['_' 'P' '_' '_' '_' '_' '_' '_'],
        ['B' 'p' '_' '_' '_' '_' '_' '_'],
        ['p' 'P' '_' '_' '_' '_' '_' '_'],
        ['k' '_' '_' '_' 'K' '_' '_' 'R']]

print('Castle KingSide White')
color_to_play = Color.WHITE
castling_available = np.array([[False, True], 
                            [False, False]])
board = Board()
board.from_printed_board(pboard, color_to_play)
board.castling_available = castling_available
castling_king_side_white1, _ = get_best_moveAB(board, 1)
print(castling_king_side_white1)
castling_king_side_white2, _ = get_best_moveAB(board, 2)
print(castling_king_side_white2)
castling_king_side_white3, _ = get_best_moveAB(board, 3)
print(castling_king_side_white3)
castling_queen_side_white4, _ = get_best_moveAB(board, 4)
print(castling_queen_side_white4)

# QueenSide White Castle
pboard = [['_' '_' '_' '_' '_' '_' '_' '_'],
          ['p' 'p' 'p' 'p' 'p' 'p' 'p' 'p'],
          ['_' '_' '_' '_' '_' '_' '_' '_'],
          ['_' '_' '_' '_' '_' '_' '_' '_'],
          ['_' '_' '_' '_' '_' '_' '_' '_'],
          ['R' 'R' '_' '_' '_' 'R' 'R' 'R'],
          ['P' 'P' 'P' '_' '_' 'P' 'P' 'P'],
          ['R' '_' '_' '_' 'K' '_' '_' 'k']]

print('Castle QueenSide White')

color_to_play = Color.WHITE
castling_available = np.array([[True,  False], 
                            [False, False]])
board = Board()
board.from_printed_board(pboard, color_to_play)
board.castling_available = castling_available
castling_queen_side_white1, _ = get_best_moveAB(board, 1)
print(castling_queen_side_white1)
castling_queen_side_white2, _ = get_best_moveAB(board, 2)
print(castling_queen_side_white2)
castling_queen_side_white3, _ = get_best_moveAB(board, 3)
print(castling_queen_side_white3)
castling_queen_side_white4, _ = get_best_moveAB(board, 4)
print(castling_queen_side_white4)


# KingSide Black Castle
pboard = [['K' '_' '_' '_' 'k' '_' '_' 'r'],
          ['p' 'p' 'p' 'p' '_' 'p' 'p' 'p'],
          ['_' '_' '_' '_' '_' 'r' 'r' 'r'],
          ['_' '_' '_' '_' '_' '_' '_' '_'],
          ['_' '_' '_' '_' '_' '_' '_' '_'],
          ['_' '_' '_' '_' '_' '_' '_' '_'],
          ['P' 'P' 'P' '_' '_' 'P' 'P' 'P'],
          ['R' '_' '_' '_' '_' '_' '_' '_']]

print('Castle KingSide Black')

color_to_play = Color.WHITE
castling_available = np.array([[False,  False], 
                            [False, True]])
board = Board()
board.from_printed_board(pboard, color_to_play)
board.castling_available = castling_available
castling_queen_side_white1, _ = get_best_moveAB(board, 1)
print(castling_queen_side_white1)
castling_queen_side_white2, _ = get_best_moveAB(board, 2)
print(castling_queen_side_white2)
castling_queen_side_white3, _ = get_best_moveAB(board, 3)
print(castling_queen_side_white3)
castling_queen_side_white4, _ = get_best_moveAB(board, 4)
print(castling_queen_side_white4)


# QueenSide Black Castle
pboard = [['r' '_' '_' '_' 'k' '_' '_' 'K'],
          ['p' 'p' 'p' 'p' 'p' 'p' 'p' 'p'],
          ['_' '_' '_' '_' '_' 'r' 'r' 'r'],
          ['_' '_' '_' '_' '_' '_' '_' '_'],
          ['_' '_' '_' '_' '_' '_' '_' '_'],
          ['_' '_' '_' '_' '_' '_' '_' '_'],
          ['P' 'P' 'P' '_' '_' 'P' 'P' 'P'],
          ['R' '_' '_' '_' '_' '_' '_' '_']]

print('Castle QueenSide Black')

color_to_play = Color.BLACK
castling_available = np.array([[False,  False], 
                               [True, False]])
board = Board()
board.from_printed_board(pboard, color_to_play)
board.castling_available = castling_available
castling_queen_side_white1, _ = get_best_moveAB(board, 1)
print(castling_queen_side_white1)
castling_queen_side_white2, _ = get_best_moveAB(board, 2)
print(castling_queen_side_white2)
castling_queen_side_white3, _ = get_best_moveAB(board, 3)
print(castling_queen_side_white3)
castling_queen_side_white4, _ = get_best_moveAB(board, 4)
print(castling_queen_side_white4)