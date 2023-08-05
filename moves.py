import random
from utils import count_bits, get_right_bit_index
import numpy as np
from evaluation import evaluate_board
from precalculations import Files, Ranks, KING_MOVES, KNIGHT_MOVES, FILE_MOVES, RANK_MOVES, FILE_MASK, RANK_MASK, \
    DIAGONAL_MOVES, DIAGONAL_MASK, ANTI_DIAGONAL_MOVES, ANTI_DIAGONAL_MASK, BLACK_PAWN_ATTACK_MOVES, BLACK_PAWN_MOVES, \
    WHITE_PAWN_ATTACK_MOVES, WHITE_PAWN_MOVES
from classes import Move, Square, Piece, Color


def get_king_moves(bb):
    return KING_MOVES[bb]


def get_knight_moves(bb):
    return KNIGHT_MOVES[bb]


def get_file_moves(bb, occupancy):
    occupancy &= FILE_MASK[bb]
    return FILE_MOVES[(bb, occupancy)]


def get_rank_moves(bb, occupancy):
    occupancy &= RANK_MASK[bb]
    return RANK_MOVES[(bb, occupancy)]


def get_right_diagonal_moves(bb, occupancy):
    clean_occupancy = occupancy & DIAGONAL_MASK[bb]
    return DIAGONAL_MOVES[(bb, clean_occupancy)]


def get_left_diagonal_moves(bb, occupancy):
    clean_occupancy = occupancy & ANTI_DIAGONAL_MASK[bb]
    return ANTI_DIAGONAL_MOVES[(bb, clean_occupancy)]


def get_rook_moves(bb, occupancy, same_color_occupancy):
    return (get_file_moves(bb, occupancy) | get_rank_moves(bb, occupancy)) & ~same_color_occupancy


def get_bishop_move(bb, occupancy, same_color_occupancy):
    return (get_right_diagonal_moves(bb, occupancy) | get_left_diagonal_moves(bb, occupancy)) & ~ same_color_occupancy


def get_queen_move(bb, occupancy, same_color_occupancy):
    return get_bishop_move(bb, occupancy, same_color_occupancy) | get_rook_moves(bb, occupancy, same_color_occupancy)


def get_pawn_attack_en_passant_white(bb, opposite_color_occunpancy):
    # p_pp
    # ____
    # _pP_

    # TODO

    return None


def get_pawn_attacks_white(bb, opposite_color_occunpancy):
    clean_occupancy = opposite_color_occunpancy & (RANK_MASK[bb] << np.uint64(8))
    return WHITE_PAWN_ATTACK_MOVES[(bb, clean_occupancy)]


def get_pawn_attacks_black(bb, opposite_color_occunpancy):
    clean_occupancy = opposite_color_occunpancy & (RANK_MASK[bb] >> np.uint64(8))
    return BLACK_PAWN_ATTACK_MOVES[(bb, clean_occupancy)]


def get_pawn_moves_white(bb, occupancy):
    clean_occupancy = occupancy & FILE_MASK[bb]
    return WHITE_PAWN_MOVES[(bb, clean_occupancy)]


def get_pawn_moves_black(bb, occupancy):
    clean_occupancy = occupancy & FILE_MASK[bb]
    return BLACK_PAWN_MOVES[(bb, clean_occupancy)]


def get_legal_moves_from(piece, board, from_):
    sq_bb = Square(from_).toBoard()
    if piece == Piece.PAWN:
        # TODO: Add en pasant
        if board.color_to_play == Color.WHITE:
            simple_moves = get_pawn_moves_white(sq_bb, board.all_pieces)
            attack_moves = get_pawn_attacks_white(sq_bb, board.all_pieces_per_color[Color.BLACK])
        else:
            simple_moves = get_pawn_moves_black(sq_bb, board.all_pieces)
            attack_moves = get_pawn_attacks_black(sq_bb, board.all_pieces_per_color[Color.WHITE])

        list_of_moves = []
        while attack_moves:
            right_bit_index = get_right_bit_index(attack_moves)
            rbi_bb = Square(right_bit_index).toBoard()

            if bool(rbi_bb & Ranks[7 * (1 - board.color_to_play)]):
                list_of_moves.append(Move(piece, from_, right_bit_index, promotion=Piece.QUEEN))
                list_of_moves.append(Move(piece, from_, right_bit_index, promotion=Piece.KNIGHT))
                list_of_moves.append(Move(piece, from_, right_bit_index, promotion=Piece.ROOK))
                list_of_moves.append(Move(piece, from_, right_bit_index, promotion=Piece.BISHOP))

            else:
                list_of_moves.append(Move(piece, from_, right_bit_index))
            attack_moves = attack_moves & ~rbi_bb

        start = 0
        while simple_moves:
            right_bit_index = get_right_bit_index(simple_moves)
            rbi_bb = Square(right_bit_index).toBoard()
            start = right_bit_index + 1

            if bool(rbi_bb & Ranks[7 * (1 - board.color_to_play)]):
                list_of_moves.append(Move(piece, from_, right_bit_index, promotion=Piece.QUEEN))
                list_of_moves.append(Move(piece, from_, right_bit_index, promotion=Piece.KNIGHT))
                list_of_moves.append(Move(piece, from_, right_bit_index, promotion=Piece.ROOK))
                list_of_moves.append(Move(piece, from_, right_bit_index, promotion=Piece.BISHOP))

            else:
                list_of_moves.append(Move(piece, from_, right_bit_index))
            simple_moves = simple_moves & ~rbi_bb
        return list_of_moves
    elif piece == Piece.ROOK:
        moves = get_rook_moves(sq_bb, board.all_pieces, board.all_pieces_per_color[board.color_to_play])
    elif piece == Piece.BISHOP:
        moves = get_bishop_move(sq_bb, board.all_pieces, board.all_pieces_per_color[board.color_to_play])
    elif piece == Piece.KNIGHT:
        moves = get_knight_moves(sq_bb) & ~ board.all_pieces_per_color[board.color_to_play]
    elif piece == Piece.QUEEN:
        moves = get_queen_move(sq_bb, board.all_pieces, board.all_pieces_per_color[board.color_to_play])
    elif piece == Piece.KING:
        # TODO: Add castling
        moves = get_king_moves(sq_bb) & ~ board.all_pieces_per_color[board.color_to_play]

    start = 0
    list_of_moves = []
    while moves:
        right_bit_index = get_right_bit_index(moves)
        rbi_bb = Square(right_bit_index).toBoard()
        list_of_moves.append(Move(piece, from_, right_bit_index))
        moves = moves & ~rbi_bb

    return list_of_moves


def get_legal_moves(board):
    lms = []
    for piece in [Piece.KNIGHT, Piece.BISHOP, Piece.QUEEN, Piece.ROOK, Piece.PAWN, Piece.KING]:
        piece_bb = board.pieces[board.color_to_play][piece]
        while piece_bb:
            right_bit_index = get_right_bit_index(piece_bb)
            lms += get_legal_moves_from(piece, board, right_bit_index)
            piece_bb = piece_bb & ~Square(right_bit_index).toBoard()
    return lms


def get_legal_moves_from_count(piece, board, from_):
    # used to develop a perf statistics
    return None

def get_legal_moves_count(board):
    # used to develop a perf statistics
    None


def negamaxAB(board, alpha, beta, depth=0):
    # [ALO-ZORBRIST] zorbrist makes everything too slow
    # if board.hash_value in board.transposition_table and board.transposition_table[board.hash_value]['depth'] >= depth:
    #     return board.transposition_table[board.hash_value]['move'], board.transposition_table[board.hash_value]['score']

    if depth < 1:
        return board.eval

    factor = - board.color_to_play * 2 + 1
    lms = get_legal_moves(board)
    maxScore = -9999999999
    for m in lms:
        score = factor * negamaxAB(board.move(m), -beta, -alpha, depth - 1)

        if score > maxScore:
            maxScore = score
            if score > alpha:
                alpha = score
                if alpha >= beta: break
                
    # [ALO-ZORBRIST] zorbrist makes everything too slow
    # board.add_to_transpotition_table(m, depth, factor*maxScore)
    return factor * maxScore


def get_best_moveAB(board, depth=1):
    factor = - board.color_to_play * 2 + 1
    lms = get_legal_moves(board)
    lbs = []
    alpha = -99999999
    beta = 99999999

    # [ALO-ZORBRIST] zorbrist makes everything too slow
    # if board.hash_value in board.transposition_table and board.transposition_table[board.hash_value]['depth'] >= depth:
    #     return board.transposition_table[board.hash_value]['move'], board.transposition_table[board.hash_value]['score']

    for m in lms:
        score = factor * negamaxAB(board.move(m), -beta, -alpha, depth - 1)
        lbs.append(score)
        
    index = np.argmax([m for m in lbs])
    
    # [ALO-ZORBRIST] zorbrist makes everything too slow
    # board.add_to_transpotition_table(lms[index], depth, lbs[index])
    return lms[index], factor*lbs[index]

def get_random_move(board, depth=1, debug=False, debug_str=""):
    lms = get_legal_moves(board)
    if lms:
        index = random.randint(0, len(lms) - 1)
        return lms[index]
    else:
        return None


#################################
# Legacy - Good for testing
#################################

def negamax(board, depth=0, debug=False, debug_str=""):
    if depth < 1:
        if debug:
            print(debug_str, "Score: ", evaluate_board(board), "   ---   Board: \n", board)
        return evaluate_board(board)
    factor = - board.color_to_play * 2 + 1
    lms = get_legal_moves(board)

    scores = [factor * negamax(board.move(m), depth - 1, debug, debug_str[0] * (len(debug_str) + 2)) for m in lms]
    index = np.argmax(scores)
    score = scores[index]
    if debug:
        print(debug_str, " ***! Score: ", score, "   ---   Move: \n", lms[index], "   ---   Board: \n",
              board.move(lms[index]))
    return factor * score


def get_best_move(board, depth=1, debug=False, debug_str=""):
    factor = - board.color_to_play * 2 + 1
    lms = get_legal_moves(board)
    lbs = []
    for m in lms:
        print(debug_str, "Move: ", m)
        score = factor * negamax(board.move(m), depth - 1, debug, debug_str[0] * (len(debug_str) + 2))
        print(debug_str, '        Score: ', score)

        lbs.append(score)
    index = np.argmax([m for m in lbs])
    if debug:
        print(debug_str, "Score: ", factor * lbs[index], "   ---   Move: ", lms[index])

    return lms[index]