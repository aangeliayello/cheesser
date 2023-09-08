import numpy as np
from classes import Piece, Color

score_map = {
    Piece.PAWN: 100,
    Piece.KNIGHT: 300,
    Piece.BISHOP: 325,
    Piece.ROOK: 500,
    Piece.QUEEN: 900,
    Piece.KING: 90000,
}

pawn_heatmap_white = np.array([[+0, +0, +0, +0, +0, +0, +0, +0],
                         [+40, +40, +40, +40, +40, +40, +40, +40],
                         [+0, +0, +0, +22, +22, +0, +0, +0],
                         [+0, +0, +0, +21, +21, +0, +0, +0],
                         [-1, -1, -1, +20, +20, -1, -1, -1],
                         [+1, -1, -1, +5, +5, -1, -1, +1],
                         [+0, +0, +0, -10, -10, +0, +0, +0],
                         [+0, +0, +0, +0, +0, +0, +0, +0]]) + score_map[Piece.PAWN]

rook_heatmap_white = np.array([[+0, +0, +0, +0, +0, +0, +0, +0],
                         [+8, +8, +8, +8, +8, +8, +8, +8],
                         [+0, +0, +0, +0, +0, +0, +0, +0],
                         [+0, +0, +0, +0, +0, +0, +0, +0],
                         [+0, +0, +0, +0, +0, +0, +0, +0],
                         [+0, +0, +0, +0, +0, +0, +0, +0],
                         [+0, +0, +0, +0, +0, +0, +0, +0],
                         [+0, +0, +2, +2, +2, +2, +0, +0]]) + score_map[Piece.ROOK]

knight_heatmap_white = np.array([[-2, -2, -2, -2, -2, -2, -2, -2],
                           [-2, -1, -1, -1, -1, -1, -1, -2],
                           [-2, -1, +5, +5, +5, +5, -1, -2],
                           [-2, -1, +5, +5, +5, +5, -1, -2],
                           [-2, -1, +5, +5, +5, +5, -1, -2],
                           [-2, -1, +5, +5, +5, +5, -1, -2],
                           [-2, -1, -1, -1, -1, -1, -1, -2],
                           [-2, -2, -2, -2, -2, -2, -2, -2]]) + score_map[Piece.KNIGHT]

bishop_heatmap_white = np.array([[-5, -1, -1, -1, -1, -1, -1, -5],
                           [-1, +0, +0, +0, +0, +0, +0, -1],
                           [-1, +0, +2, +2, +2, +2, +0, -1],
                           [-1, +0, +2, +5, +5, +2, +0, -1],
                           [-1, +0, +2, +5, +5, +2, +0, -1],
                           [-1, +0, +2, +2, +2, +2, +0, -1],
                           [-1, +0, +0, +0, +0, +0, +0, -1],
                           [-5, -2, -2, -2, -2, -2, -2, -5]]) + score_map[Piece.BISHOP]

queen_heatmap_white = np.array([[-5, -1, -1, -1, -1, -1, -1, -5],
                          [-1, +0, +0, +0, +0, +0, +0, -1],
                          [-1, +0, +2, +2, +2, +2, +0, -1],
                          [-1, +0, +2, +5, +5, +2, +0, -1],
                          [-1, +0, +2, +5, +5, +2, +0, -1],
                          [-1, +0, +2, +2, +2, +2, +0, -1],
                          [-1, +0, +0, +0, +0, +0, +0, -1],
                          [-5, -2, -2, -2, -2, -2, -2, -5]]) + score_map[Piece.QUEEN]

king_heatmap_white = np.array([[+0, +0, +0, +0, +0, +0, +0, +0],
                         [+0, +0, +0, +0, +0, +0, +0, +0],
                         [+0, +0, +0, +0, +0, +0, +0, +0],
                         [+0, +0, +0, +0, +0, +0, +0, +0],
                         [+0, +0, +0, +0, +0, +0, +0, +0],
                         [+0, +0, +0, +0, +0, +0, +0, +0],
                         [+0, +0, +0, +0, +0, +0, +0, +0],
                         [+0, +20, +20, -5, +0, -5, +20, +20]]) + score_map[Piece.KING]


pawn_heatmap_black = -1*np.flip(pawn_heatmap_white, axis=0)
rook_heatmap_black = -1*np.flip(rook_heatmap_white, axis=0)
knight_heatmap_black = -1*np.flip(knight_heatmap_white, axis=0)
bishop_heatmap_black = -1*np.flip(bishop_heatmap_white, axis=0)
queen_heatmap_black = -1*np.flip(queen_heatmap_white, axis=0)
king_heatmap_black = -1*np.flip(king_heatmap_white, axis=0)

piece_color_to_heatmap = {
    # white
    (Color.WHITE, Piece.PAWN): lambda x, y: pawn_heatmap_white[x, y],
    (Color.WHITE, Piece.ROOK): lambda x, y: rook_heatmap_white[x, y],
    (Color.WHITE, Piece.KNIGHT): lambda x, y: knight_heatmap_white[x, y],
    (Color.WHITE, Piece.BISHOP): lambda x, y: bishop_heatmap_white[x, y],
    (Color.WHITE, Piece.QUEEN): lambda x, y: queen_heatmap_white[x, y],
    (Color.WHITE, Piece.KING): lambda x, y: king_heatmap_white[x, y],

    # black
    (Color.BLACK, Piece.PAWN): lambda x, y: pawn_heatmap_black[x, y],
    (Color.BLACK, Piece.ROOK): lambda x, y: rook_heatmap_black[x, y],
    (Color.BLACK, Piece.KNIGHT): lambda x, y: knight_heatmap_black[x, y],
    (Color.BLACK, Piece.BISHOP): lambda x, y: bishop_heatmap_black[x, y],
    (Color.BLACK, Piece.QUEEN): lambda x, y: queen_heatmap_black[x, y],
    (Color.BLACK, Piece.KING): lambda x, y: king_heatmap_black[x, y],
}


def piece_to_value(color, piece, square):
    # TODO: (Speed) do a map instead of computing with xy
    return piece_color_to_heatmap[(color, piece)](7 - square//8, square%8)
