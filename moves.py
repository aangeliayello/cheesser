import numpy as np
from utils import *
from evaluation import evaluate_board
from precalculations import KING_MOVES, KNIGHT_MOVES

class Move(object):
    def __init__(self, piece, from_, to, promotion=None, en_passant=False, castleSide=None):
        self.from_ = from_
        self.to = to
        self.piece = piece
        self.promotion = promotion
        self.en_passant = en_passant
        self.castleSide = castleSide
        
    def __str__(self):
        return self.piece.name + ": " + "(" + str(self.from_) + ", " + str(self.to) + ")"


def get_kingLike_moves(bb):
    return KING_MOVES[bb]

def get_knightLike_moves(bb):
    return KNIGHT_MOVES[bb]

def get_file_moves(bb, occupancy):
    moves = np.uint64(0)
    bb_up = bb
    bb_down = bb

    # up
    for i in range(1, 8):
        bb_up = bb_up << np.uint64(8)
        if bb_up == 0: break
        moves |= bb_up
        if bb_up & occupancy: break

    for i in range(1, 8):
        bb_down = bb_down >> np.uint64(8)
        if bb_down == 0: break
        moves |= bb_down
        if bb_down & occupancy: break

    return moves

def get_rank_moves(bb, occupancy):
    moves = np.uint64(0)
    bb_right = bb
    bb_left = bb

    # right
    for i in range(1, 8):
        bb_right = (bb_right & ~Files[File.H]) << np.uint64(1)
        if bb_right == 0: break
        moves |= bb_right
        if bb_right & occupancy: break

    # left
    for i in range(1, 8):
        bb_left = (bb_left & ~Files[File.A]) >> np.uint64(1)
        if bb_left == 0: break
        moves |= bb_left
        if bb_left & occupancy: break
    return moves

def get_right_diagonal_moves(bb, occupancy):
    moves = np.uint64(0)
    bb_up_right = bb
    bb_down_left = bb

    # up
    for i in range(1, 8):
        bb_up_right = (bb_up_right & ~Files[File.H]) << np.uint64(9)
        if bb_up_right == 0: break
        moves |= bb_up_right
        if bb_up_right & occupancy: break

    for i in range(1, 8):
        bb_down_left = (bb_down_left & ~Files[File.A]) >> np.uint64(9)
        if bb_down_left == 0: break
        moves |= bb_down_left
        if bb_down_left & occupancy: break

    return moves

def get_left_diagonal_moves(bb, occupancy):
    moves = np.uint64(0)
    bb_up_left = bb
    bb_down_right = bb

    # up
    for i in range(1, 8):
        bb_up_left = (bb_up_left & ~Files[File.A]) << np.uint64(7)
        if bb_up_left == 0: break
        moves |= bb_up_left
        if bb_up_left & occupancy: break

    for i in range(1, 8):
        bb_down_right = (bb_down_right & ~Files[File.H]) >> np.uint64(7)
        if bb_down_right == 0: break
        moves |= bb_down_right
        if bb_down_right & occupancy: break

    return moves

def get_rook_moves(bb, occupancy, same_color_occupancy):
    return (get_file_moves(bb, occupancy) | get_rank_moves(bb, occupancy)) & ~ same_color_occupancy

def get_bishop_move(bb, occupancy, same_color_occupancy):
    return (get_right_diagonal_moves(bb, occupancy) | get_left_diagonal_moves(bb, occupancy)) & ~ same_color_occupancy

def get_queen_move(bb, occupancy, same_color_occupancy):
    return (get_bishop_move(bb, occupancy, same_color_occupancy) | get_rook_moves(bb, occupancy, same_color_occupancy))

def get_pawn_attack_en_passant_white(bb, opposite_color_occunpancy):
    # p_pp
    # ____
    # _pP_
    
    #TODO
    
    return None

def get_pawn_attacks_white(bb, opposite_color_occunpancy):
    # _A_B_
    # __X__
    a = ((bb & ~Files[File.A]) << np.uint64(7))&opposite_color_occunpancy
    b  = ((bb & ~Files[File.H]) << np.uint64(9))&opposite_color_occunpancy

    return a | b

def get_pawn_attacks_black(bb, opposite_color_occunpancy):
    # __X__
    # _A_B_

    a = ((bb & ~Files[File.A]) >> np.uint64(9))&opposite_color_occunpancy
    b = ((bb & ~Files[File.H]) >> np.uint64(7))&opposite_color_occunpancy

    return a | b

def get_pawn_moves_white(bb, occupancy):
    moves = (bb << np.uint64(8)) & ~occupancy
    if (bb & Ranks[Rank.Two]):
        moves |= (moves << np.uint64(8)) & ~occupancy
    return moves

def get_pawn_moves_black(bb, occupancy):
    moves = (bb >> np.uint64(8)) & ~occupancy
    if (bb & Ranks[Rank.Seven]) and (moves):
        moves |= (moves >> np.uint64(8)) & ~occupancy
    return moves

def get_legal_moves_from(piece, board, from_):
    sq = Square(from_)
    promotion_possible = False
    if piece == Piece.PAWN:
        # TODO: Add en pasant
        if board.color_to_play == Color.WHITE:
            moves = get_pawn_moves_white(sq.toBoard(), board.all_pieces) | get_pawn_attacks_white(sq.toBoard(), board.all_pieces_per_color[Color.BLACK])
        else:
            moves = get_pawn_moves_black(sq.toBoard(), board.all_pieces) | get_pawn_attacks_black(sq.toBoard(), board.all_pieces_per_color[Color.WHITE])
        promotion_possible = bool(moves & Ranks[7*(1-board.color_to_play)])
    elif piece == Piece.ROOK:
        moves = get_rook_moves(sq.toBoard(), board.all_pieces, board.all_pieces_per_color[board.color_to_play])
    elif piece == Piece.BISHOP:
        moves = get_bishop_move(sq.toBoard(), board.all_pieces, board.all_pieces_per_color[board.color_to_play])
    elif piece == Piece.KNIGHT:
        moves = get_knightLike_moves(sq.toBoard()) & ~ board.all_pieces_per_color[board.color_to_play]
    elif piece == Piece.QUEEN:
        moves = get_queen_move(sq.toBoard(), board.all_pieces, board.all_pieces_per_color[board.color_to_play])
    elif piece == Piece.KING:
        # TODO: Add castling
        moves = get_kingLike_moves(sq.toBoard()) & ~ board.all_pieces_per_color[board.color_to_play]

    start = 0
    list_of_moves = []
    while moves:
        right_bit_index = get_right_bit_index(moves, start)
        rbi_bb = Square(right_bit_index).toBoard()
        start = right_bit_index + 1
        
        if promotion_possible and bool(rbi_bb & Rank[7*(1-board.color_to_play)]):
            list_of_moves.append(Move(piece, from_, right_bit_index, promotion=Piece.QUEEN))
            list_of_moves.append(Move(piece, from_, right_bit_index, promotion=Piece.KNIGHT))
            list_of_moves.append(Move(piece, from_, right_bit_index, promotion=Piece.ROOK))
            list_of_moves.append(Move(piece, from_, right_bit_index, promotion=Piece.BISHOP))
            
        else:
            list_of_moves.append(Move(piece, from_, right_bit_index))
        moves = moves & ~rbi_bb

    return list_of_moves


def get_legal_moves(board):
    lms = []
    for piece in Piece:
        piece_bb = board.pieces[board.color_to_play][piece]
        start = 0
        while piece_bb:
            right_bit_index = get_right_bit_index(piece_bb, start)
            start = right_bit_index + 1
            lms += get_legal_moves_from(piece, board, right_bit_index)
            piece_bb = piece_bb & ~Square(right_bit_index).toBoard()
    return lms

def negamaxAB(board, alpha, beta, depth = 0, debug = False, debug_str = ""):
    if depth < 1:
        if debug:
            print(debug_str, "Score: ", evaluate_board(board), "   ---   Board: \n", board)
        return evaluate_board(board)
    factor = - board.color_to_play * 2 + 1
    lms = get_legal_moves(board)
    maxScore = -9999999999
    bestMove = lms[0] # TODO: stalemate
    for m in lms:
        score = factor*negamaxAB(board.move(m), -beta, -alpha, depth - 1, debug, debug_str[0]*(len(debug_str) +2))

        if score > maxScore:
            maxScore = score
            bestMove = m
        alpha = max(alpha, score)
        if alpha >= beta: break

    if debug:
        print(debug_str, " ***! Score: ", maxScore, "   ---   Move: \n", bestMove, "   ---   Board: \n", board.move(bestMove))
    return factor*maxScore

def get_best_moveAB(board, depth = 1, debug = False, debug_str = ""):
    factor = - board.color_to_play * 2 + 1
    lms = get_legal_moves(board)
    lbs = []
    alpha = -99999999
    beta  =  99999999

    for m in lms:
        if debug: print(debug_str, "Move: ", m)
        score = factor*negamaxAB(board.move(m), -beta, -alpha, depth - 1, debug, debug_str[0]*(len(debug_str) +2))
        if debug: print(debug_str,'        Score: ', score)
        lbs.append(score)
    index = np.argmax([m for m in lbs])
    if debug:
        print(debug_str, "Score: ", factor*lbs[index], "   ---   Move: ", lms[index])

    return lms[index]


# Legace - Good for testing
def negamax(board, depth = 0, debug = False, debug_str = ""):
    if depth < 1:
        if debug:
            print(debug_str, "Score: ", evaluate_board(board), "   ---   Board: \n", board)
        return evaluate_board(board)
    factor = - board.color_to_play * 2 + 1
    lms = get_legal_moves(board)

    scores = [factor*negamax(board.move(m), depth - 1, debug, debug_str[0]*(len(debug_str) +2)) for m in lms]
    index = np.argmax(scores)
    score = scores[index]
    if debug:
        print(debug_str, " ***! Score: ", score, "   ---   Move: \n", lms[index], "   ---   Board: \n", board.move(lms[index]))
    return factor*score

def get_best_move(board, depth = 1, debug = False, debug_str = ""):
    factor = - board.color_to_play * 2 + 1
    lms = get_legal_moves(board)
    lbs = []
    for m in lms:
        print(debug_str, "Move: ", m)
        score = factor*negamax(board.move(m), depth - 1, debug, debug_str[0]*(len(debug_str) +2))
        print(debug_str,'        Score: ', score)

        lbs.append(score)
    index = np.argmax([m for m in lbs])
    if debug:
        print(debug_str, "Score: ", factor*lbs[index], "   ---   Move: ", lms[index])

    return lms[index]
