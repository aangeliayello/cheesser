from utils import *
from classes import Piece, Color, Move, Square
from piece_heatmap import piece_to_value
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


def board_evaluation_move_correction(color: Color, oppo_all_pieces: np.uint64, oppo_pieces, move: Move, delta_castling_rights): 

    if move.promotion is None:
        piece_to = move.piece
    else:
        piece_to = move.promotion
    
    to_value = piece_to_value(color, piece_to, move.to)
    from_value = piece_to_value(color, move.piece, move.from_)

    # check if capture
    en_passant_capture_value = 0
    opposite_color = color.flip()
    if move.en_passant_capture:
        captured_pawn_sqr = move.to + (-8 if color == Color.WHITE else +8)
        en_passant_capture_value = piece_to_value(opposite_color, Piece.PAWN, captured_pawn_sqr)
        
    to_bb = Square(move.to).toBoard()
    capture_value = 0
    if oppo_all_pieces & to_bb:
        to_bb = Square(move.to).toBoard()
        captured_piece = next(piece for piece in Piece if oppo_pieces[piece] & to_bb)
        capture_value = piece_to_value(opposite_color, captured_piece, move.to)
        
    rook_castle_value = 0
    if move.castleSide:
        rook_from, rook_to = castling_rook_move(color, move.castleSide)
        rook_to_score = piece_to_value(color, Piece.ROOK, rook_to)
        rook_from_score = piece_to_value(color, Piece.ROOK, rook_from)
        rook_castle_value = rook_to_score - rook_from_score
    
    delta_castling_rights_value = 0
    if False and delta_castling_rights: # negative if it lost rigthts
        delta_castling_rights_value = delta_castling_rights*500*(-1 if color == Color.BLACK else 1)
        
    return (to_value - from_value) - en_passant_capture_value - capture_value + rook_castle_value + delta_castling_rights_value