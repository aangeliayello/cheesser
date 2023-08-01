from utils import *
from classes import Piece, Color
# Center rings
ring0 = np.uint64(0b0000000000000000000000000001100000011000000000000000000000000000)
ring1 = np.uint64(0b0000000000000000001111000010010000100100001111000000000000000000)

score_map = {
    Piece.PAWN: 1000,
    Piece.KNIGHT: 3000,
    Piece.BISHOP: 3250,
    Piece.ROOK: 5000,
    Piece.QUEEN: 9000,
    Piece.KING: 999999999,
}

def evaluate_board(board):
    score = 0

    # piece count
    for piece in Piece:

        count = int(count_bits(board.pieces[Color.WHITE][piece])) - int(count_bits(board.pieces[Color.BLACK][piece]))

        if piece != Piece.KING:
            count0 = int(count_bits(board.pieces[Color.WHITE][piece] & ring0)) -  int(count_bits(board.pieces[Color.BLACK][piece] & ring0))
            count1 = int(count_bits(board.pieces[Color.WHITE][piece] & ring1)) -  int(count_bits(board.pieces[Color.BLACK][piece] & ring1))
        else:
            count0 = 0
            count1 = 0
        score += (count + count0 * 0.005 + count1 * 0.001) * score_map[piece]

    return score