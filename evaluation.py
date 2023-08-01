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

    if board.color_to_play == Color.WHITE:
        score += 0
    else:
        score -= 0

    # piece count
    for color in Color:
        if color == Color.WHITE: factor = 1
        else: factor = -1

        for piece in Piece:

            count = count_bits(board.pieces[color][piece])

            if piece != Piece.KING:
                count0 = count_bits(board.pieces[color][piece] & ring0)
                count1 = count_bits(board.pieces[color][piece] & ring1)
            else:
                count0 = 0
                count1 = 0
            score += (count + count0 * 0.005 + count1 * 0.001) * factor * score_map[piece]

    return score