import numpy as np
from classes import Piece, Color

score_map = {
    Piece.PAWN: 1000,
    Piece.KNIGHT: 3000,
    Piece.BISHOP: 3250,
    Piece.ROOK: 5000,
    Piece.QUEEN: 9000,
    Piece.KING: 20000,
}
heatmap_factor = 0.001

generic_heatmap_white = np.array([[+0, +0, +0, +0, +0, +0, +0, +0],
                         [+0, +0, +0, +0, +0, +0, +0, +0],
                         [+0, +0, +1, +1, +1, +1, +0, +0],
                         [+0, +0, +1, +5, +5, +1, +0, +0],
                         [-0, -0, +1, +5, +5, +1, -0, -0],
                         [+0, -0, +1, +1, +1, +1, -0, +0],
                         [+0, +0, +0, -0, -0, +0, +0, +0],
                         [+0, +0, +0, +0, +0, +0, +0, +0]])

pawn_heatmap_white = np.array([[+0, +0, +0, +0, +0, +0, +0, +0],
                         [+40, +40, +40, +40, +40, +40, +40, +40],
                         [+0, +0, +0, +22, +22, +0, +0, +0],
                         [+0, +0, +0, +21, +21, +0, +0, +0],
                         [-1, -1, -1, +20, +20, -1, -1, -1],
                         [+1, -1, -1, +5, +5, -1, -1, +1],
                         [+0, +0, +0, -60, -60, +0, +0, +0],
                         [+0, +0, +0, +0, +0, +0, +0, +0]])

rook_heatmap_white = np.array([[+0, +0, +0, +0, +0, +0, +0, +0],
                         [+8, +8, +8, +8, +8, +8, +8, +8],
                         [+0, +0, +0, +0, +0, +0, +0, +0],
                         [+0, +0, +0, +0, +0, +0, +0, +0],
                         [+0, +0, +0, +0, +0, +0, +0, +0],
                         [+0, +0, +0, +0, +0, +0, +0, +0],
                         [+0, +0, +0, +0, +0, +0, +0, +0],
                         [+0, +0, +2, +2, +2, +2, +0, +0]])

knight_heatmap_white = np.array([[-2, -2, -2, -2, -2, -2, -2, -2],
                           [-2, -1, -1, -1, -1, -1, -1, -2],
                           [-2, -1, +5, +5, +5, +5, -1, -2],
                           [-2, -1, +5, +5, +5, +5, -1, -2],
                           [-2, -1, +5, +5, +5, +5, -1, -2],
                           [-2, -1, +5, +5, +5, +5, -1, -2],
                           [-2, -1, -1, -1, -1, -1, -1, -2],
                           [-2, -5, -2, -2, -2, -2, -5, -2]])

bishop_heatmap_white = np.array([[-5, -1, -1, -1, -1, -1, -1, -5],
                           [-1, +0, +0, +0, +0, +0, +0, -1],
                           [-1, +0, +2, +2, +2, +2, +0, -1],
                           [-1, +0, +2, +5, +5, +2, +0, -1],
                           [-1, +0, +2, +5, +5, +2, +0, -1],
                           [-1, +0, +2, +2, +2, +2, +0, -1],
                           [-1, +0, +0, +0, +0, +0, +0, -1],
                           [-5, -1, -5, -1, -1, -5, -1, -5]])

queen_heatmap_white = np.array([[-5, -1, -1, -1, -1, -1, -1, -5],
                          [-1, +0, +0, +0, +0, +0, +0, -1],
                          [-1, +0, +2, +2, +2, +2, +0, -1],
                          [-1, +0, +2, +5, +5, +2, +0, -1],
                          [-1, +0, +2, +5, +5, +2, +0, -1],
                          [-1, +0, +2, +2, +2, +2, +0, -1],
                          [-1, +0, +0, +0, +0, +0, +0, -1],
                          [-5, -1, -1, -1, -1, -1, -1, -5]])

king_heatmap_white = np.array([[+0, +0, +0, +0, +0, +0, +0, +0],
                         [+0, +0, +0, +0, +0, +0, +0, +0],
                         [+0, +0, +0, +0, +0, +0, +0, +0],
                         [+0, +0, +0, +0, +0, +0, +0, +0],
                         [+0, +0, +0, +0, +0, +0, +0, +0],
                         [+0, +0, +0, +0, +0, +0, +0, +0],
                         [+0, +0, +0, +0, +0, +0, +0, +205],
                         [+0, +205, +200, +0, +0, +0, +200, +205]])

pawn_heatmap_black = np.flip(pawn_heatmap_white, axis=0)
rook_heatmap_black = np.flip(rook_heatmap_white, axis=0)
knight_heatmap_black = np.flip(knight_heatmap_white, axis=0)
bishop_heatmap_black = np.flip(bishop_heatmap_white, axis=0)
queen_heatmap_black = np.flip(queen_heatmap_white, axis=0)
king_heatmap_black = np.flip(king_heatmap_white, axis=0)

piece_color_to_heatmap = {
    # white
    (Color.WHITE, Piece.PAWN): lambda x, y: (1 + pawn_heatmap_white[x, y]*heatmap_factor) * score_map[Piece.PAWN],
    (Color.WHITE, Piece.ROOK): lambda x, y: (1 + rook_heatmap_white[x, y]*heatmap_factor) * score_map[Piece.ROOK],
    (Color.WHITE, Piece.KNIGHT): lambda x, y: (1 + knight_heatmap_white[x, y]*heatmap_factor) * score_map[Piece.KNIGHT],
    (Color.WHITE, Piece.BISHOP): lambda x, y: (1 + bishop_heatmap_white[x, y]*heatmap_factor) * score_map[Piece.BISHOP],
    (Color.WHITE, Piece.QUEEN): lambda x, y: (1 + queen_heatmap_white[x, y]*heatmap_factor) * score_map[Piece.QUEEN],
    (Color.WHITE, Piece.KING): lambda x, y: (1 + king_heatmap_white[x, y]*heatmap_factor*score_map[Piece.QUEEN]/score_map[Piece.KING]) * score_map[Piece.KING],

    # black
    (Color.BLACK, Piece.PAWN): lambda x, y: -(1 + pawn_heatmap_black[x, y]*heatmap_factor) * score_map[Piece.PAWN],
    (Color.BLACK, Piece.ROOK): lambda x, y: -(1 + rook_heatmap_black[x, y]*heatmap_factor) * score_map[Piece.ROOK],
    (Color.BLACK, Piece.KNIGHT): lambda x, y: -(1 + knight_heatmap_black[x, y]*heatmap_factor) * score_map[Piece.KNIGHT],
    (Color.BLACK, Piece.BISHOP): lambda x, y: -(1 + bishop_heatmap_black[x, y]*heatmap_factor) * score_map[Piece.BISHOP],
    (Color.BLACK, Piece.QUEEN): lambda x, y: -(1 + queen_heatmap_black[x, y]*heatmap_factor) * score_map[Piece.QUEEN],
    (Color.BLACK, Piece.KING): lambda x, y: -(1 + king_heatmap_black[x, y]*heatmap_factor*score_map[Piece.QUEEN]/score_map[Piece.KING]) * score_map[Piece.KING]
}

def piece_to_value(color, piece, square):
    # TODO: (Speed) do a map instead of computing with xy
    return piece_color_to_heatmap[(color, piece)](7 - square//8, square%8)