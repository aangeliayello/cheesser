import numpy as np
from board import Board
from classes import Color, Move, Piece
from moves import get_best_moveAB
from evaluation import board_evaluation_move_correction
from utils import printBb

# KingSide White Castle
pboard = [['_' '_' '_' '_' 'k' 'b' '_' 'r'],
        ['_' '_' 'p' 'B' 'p' 'p' 'p' 'p'],
        ['_' '_' '_' '_' '_' '_' '_' '_'],
        ['_' '_' '_' '_' '_' '_' '_' '_'],
        ['_' '_' '_' '_' '_' '_' '_' '_'],
        ['q' '_' '_' '_' '_' 'P' '_' '_'],
        ['_' '_' 'P' 'B' '_' 'P' 'P' 'P'],
        ['_' '_' '_' 'Q' 'K' '_' '_' 'R']]


color_to_play = Color.BLACK
castling_available = np.array([[False, False], 
                            [False, False]])
board = Board()
board.from_printed_board(pboard, color_to_play)
# board.castling_available = castling_available
# castling_king_side_white1, _ = get_best_moveAB(board, 1)
# print(castling_king_side_white1)
# castling_king_side_white2, _ = get_best_moveAB(board, 2)
# print(castling_king_side_white2)
# castling_king_side_white3, _ = get_best_moveAB(board, 3)
# print(castling_king_side_white3)





# KingSide White Castle
pboard = [['r' 'n' 'b' '_' 'k' 'b' '_' 'r'],
 ['p' 'p' 'p' 'p' '_' 'p' 'p' 'p'],
 ['_' '_' '_' '_' 'p' '_' '_' '_'],
 ['_' '_' '_' '_' '_' '_' '_' '_'],
 ['_' '_' '_' 'P' 'n' '_' '_' 'q'],
 ['_' '_' '_' 'B' '_' '_' '_' '_'],
 ['P' 'P' 'P' '_' '_' 'P' 'P' 'P'],
 ['R' 'N' 'B' 'Q' 'K' '_' 'N' 'R']]

color_to_play = Color.WHITE
castling_available = np.array([[False, False], 
                            [False, False]])
board = Board()
board.from_printed_board(pboard, color_to_play)
# board.castling_available = castling_available
# castling_king_side_white1, _ = get_best_moveAB(board, 1)
# print(castling_king_side_white1)
# castling_king_side_white2, _ = get_best_moveAB(board, 2)
# print(castling_king_side_white2)
# castling_king_side_white3, _ = get_best_moveAB(board, 3)
# print(castling_king_side_white3)
# castling_king_side_white4, _ = get_best_moveAB(board, 4)
# print(castling_king_side_white4)


# KingSide White Castle
pboard =       [['r' 'n' 'b' 'q' 'k' 'b' '_' 'r'],
                ['p' 'p' 'p' 'p' '_' 'p' 'p' 'p'],
                ['_' '_' '_' '_' 'p' 'n' '_' '_'],
                ['_' '_' '_' '_' 'P' '_' '_' '_'],
                ['_' '_' '_' 'P' '_' '_' '_' '_'],
                ['_' '_' '_' '_' '_' '_' '_' '_'],
                ['P' 'P' 'P' '_' '_' 'P' 'P' 'P'],
                ['R' 'N' 'B' 'Q' 'K' 'B' 'N' 'R']]

color_to_play = Color.BLACK
castling_available = np.array([[False, False], 
                            [False, False]])
board = Board()
board.from_printed_board(pboard, color_to_play)
board.castling_available = castling_available
# castling_king_side_white1, _ = get_best_moveAB(board, 1)
# print(castling_king_side_white1)
# castling_king_side_white2, _ = get_best_moveAB(board, 2)
# print(castling_king_side_white2)
# castling_king_side_white3, _ = get_best_moveAB(board, 3)
# print(castling_king_side_white3)
# castling_king_side_white4, _ = get_best_moveAB(board, 4)
# print(castling_king_side_white4)
castling_king_side_white4 = Move(Piece.KNIGHT, 45, 28)
new_board = board.move(castling_king_side_white4)
print(new_board)
delta = board_evaluation_move_correction(board.color_to_play, \
                                                        board.all_pieces_per_color[board.color_to_play.flip()], \
                                                        board.pieces[board.color_to_play.flip()], \
                                                        castling_king_side_white4, 0)

print(delta)

for piece in Piece: 
    xorPiece = board.pieces[Color.WHITE][piece] ^ new_board.pieces[Color.WHITE][piece]
    if xorPiece:
            print(piece.name)
            printBb(xorPiece)

xorPiece = board.all_pieces_per_color[Color.WHITE] ^ new_board.all_pieces_per_color[Color.WHITE]
if xorPiece:
        print("white Pieces")
        printBb(xorPiece)
        
xorPiece = board.all_pieces ^ new_board.all_pieces
if xorPiece:
        print("all  Pieces")
        printBb(xorPiece)
        
for piece in Piece: 
    xorPiece = board.pieces[Color.BLACK][piece] ^ new_board.pieces[Color.BLACK][piece]
    if xorPiece:
            print(piece.name)
            printBb(xorPiece)

xorPiece = board.all_pieces_per_color[Color.BLACK] ^ new_board.all_pieces_per_color[Color.BLACK]
if xorPiece:
        print("black Pieces")
        printBb(xorPiece)