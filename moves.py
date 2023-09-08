import random
import itertools
from utils import count_bits, get_right_bit_index
import numpy as np
from evaluation import evaluate_board
from precalculations import Files, Ranks, KING_MOVES, KNIGHT_MOVES, FILE_MOVES, RANK_MOVES, FILE_MASK, RANK_MASK, \
    DIAGONAL_MOVES, DIAGONAL_MASK, ANTI_DIAGONAL_MOVES, ANTI_DIAGONAL_MASK, BLACK_PAWN_ATTACK_MOVES, BLACK_PAWN_MOVES, \
    WHITE_PAWN_ATTACK_MOVES, WHITE_PAWN_MOVES
from board import Board, TRANSPOSITION_TABLE
from classes import Move, Square, Piece, Color, CastleSide

COLLITION_COUNTER = 0
NODES_COUNT = 0

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

def king_in_check(board: Board, from_color_to_play_perspective = True):
    if from_color_to_play_perspective: 
        current_color = board.color_to_play        
    else: 
        current_color = board.color_to_play.flip()
        
    king_bb = board.pieces[current_color][Piece.KING]
    
    return is_square_attacked(king_bb, board, from_color_to_play_perspective)

def is_square_attacked(sq_bb, board: Board, from_color_to_play_perspective = True):
    # assume the king is the attacking piece, then if it can attack the respective pieces then the king is attacked.
    
    if from_color_to_play_perspective: 
        current_color = board.color_to_play
        opposite_color = current_color.flip()
        
    else: 
        opposite_color = board.color_to_play
        current_color = opposite_color.flip()
        
    opposite_pieces= board.pieces[opposite_color]
    sq_bb = board.pieces[current_color][Piece.KING]

    if get_knight_moves(sq_bb) & opposite_pieces[Piece.KNIGHT]:
        return True

    if (get_bishop_move(sq_bb, board.all_pieces, board.all_pieces_per_color[current_color]) & (opposite_pieces[Piece.QUEEN] | opposite_pieces[Piece.BISHOP])):
        return True

    if (get_rook_moves(sq_bb, board.all_pieces, board.all_pieces_per_color[current_color]) & (opposite_pieces[Piece.QUEEN] | opposite_pieces[Piece.ROOK])):
        return True

    pawn_attacks = get_pawn_attacks_white(sq_bb, opposite_pieces[Piece.PAWN]) if current_color == Color.WHITE else get_pawn_attacks_black(sq_bb, opposite_pieces[Piece.PAWN])
    if pawn_attacks:
        return True

    if get_king_moves(sq_bb) & opposite_pieces[Piece.KING]:
        return True

    return False

def get_legal_moves_from(piece, board, from_):
    sq_bb = Square(from_).toBoard()
    list_of_moves = []
    if piece == Piece.PAWN:
        if board.en_passant_sqr:
            en_passant_bb = Square(board.en_passant_sqr).toBoard()
            en_passant_attacks = get_pawn_attacks_white(sq_bb, en_passant_bb)
            if en_passant_attacks:
                list_of_moves.append(Move(piece, from_, board.en_passant_sqr, en_passant_capture=True))

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

        while simple_moves:
            right_bit_index = get_right_bit_index(simple_moves)
            rbi_bb = Square(right_bit_index).toBoard()

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
        moves = get_king_moves(sq_bb) & ~ board.all_pieces_per_color[board.color_to_play]
        # check if castling is allowed
        king_side_allowed = (board.castling_available[board.color_to_play][CastleSide.KingSide] and \
            (board.all_pieces & np.uint8(96) == 0))
        queen_side_allowed = (board.castling_available[board.color_to_play][CastleSide.QueenSide] and \
            (board.all_pieces & np.uint8(14) == 0))
        if king_side_allowed and queen_side_allowed:
            is_king_in_check = king_in_check(board)
            if king_side_allowed and \
                (not is_king_in_check) and \
                (not is_square_attacked(Square(from_ +1).toBoard(), board)) and \
                (not is_square_attacked(Square(from_ +2).toBoard(), board)):
                # check if squares are attacked
                list_of_moves.append(Move(Piece.KING, from_, from_ + 2, castleSide=CastleSide.KingSide))
            if queen_side_allowed and \
                (not is_king_in_check) and \
                (not is_square_attacked(Square(from_ -1).toBoard(), board)) and \
                (not is_square_attacked(Square(from_ -2).toBoard(), board)):
                list_of_moves.append(Move(Piece.KING, from_, from_ - 2, castleSide=CastleSide.QueenSide))

    while moves:
        right_bit_index = get_right_bit_index(moves)
        rbi_bb = Square(right_bit_index).toBoard()
        list_of_moves.append(Move(piece, from_, right_bit_index))
        moves = moves & ~rbi_bb

    return list_of_moves

def get_pseudo_legal_moves(board):
    lms = []
    for piece in [Piece.KNIGHT, Piece.BISHOP, Piece.QUEEN, Piece.ROOK, Piece.PAWN, Piece.KING]:
        piece_bb = board.pieces[board.color_to_play][piece]
        while piece_bb:
            right_bit_index = get_right_bit_index(piece_bb)
            lms += get_legal_moves_from(piece, board, right_bit_index)
            piece_bb = piece_bb & ~Square(right_bit_index).toBoard()

    return lms

def get_legal_moves(board):
    def check(m):
        return not king_in_check(board.move(m), False)

    plms = get_pseudo_legal_moves(board)

    return [m for m in plms if check(m)]

def negamaxAB(board, alpha, beta, depth=0):
    # [ALO-ZORBRIST] zorbrist makes everything too slow
    if board.hash_value in TRANSPOSITION_TABLE and TRANSPOSITION_TABLE[board.hash_value]['depth'] >= depth:
        global COLLITION_COUNTER
        COLLITION_COUNTER += 1
        return TRANSPOSITION_TABLE[board.hash_value]['score']

    if depth < 1:
        global NODES_COUNT
        NODES_COUNT += 1
        return board.eval

    factor = - board.color_to_play * 2 + 1
    lms = get_pseudo_legal_moves(board)
    max_score = -123456789
    best_move = None
    for m in lms:
        new_board = board.move(m)
        if king_in_check(new_board, False):
            continue
        score = factor * negamaxAB(new_board, -beta, -alpha, depth - 1)

        if score > max_score:
            max_score = score
            best_move = m
            if score > alpha:
                alpha = score
                if alpha >= beta: break
                
    # [ALO-ZORBRIST] zorbrist makes everything too slow
    board.add_to_transpotition_table(best_move, depth, factor*max_score)

    return factor * max_score


def get_best_moveAB(board, depth=1):
    factor = - board.color_to_play * 2 + 1
    lms = get_pseudo_legal_moves(board)
    alpha = -99999999
    beta = 99999999
    global COLLITION_COUNTER
    global NODES_COUNT
    NODES_COUNT = 0

    # [ALO-ZORBRIST] zorbrist makes everything too slow
    if board.hash_value in TRANSPOSITION_TABLE and TRANSPOSITION_TABLE[board.hash_value]['depth'] >= depth:
        return TRANSPOSITION_TABLE[board.hash_value]['move'], TRANSPOSITION_TABLE[board.hash_value]['score']

    max_score = -123456789
    best_move = None
    for m in lms:
        new_board = board.move(m)
        if king_in_check(new_board, False):
            continue
        score = factor * negamaxAB(new_board, -beta, -alpha, depth - 1)
        
        if score > max_score:
            max_score = score
            best_move = m

    # [ALO-ZORBRIST] zorbrist makes everything too slow
    board.add_to_transpotition_table(best_move, depth, max_score)
    print(NODES_COUNT, COLLITION_COUNTER)
    return best_move, max_score


def get_best_moveAB(board, depth=1):
    factor = - board.color_to_play * 2 + 1
    lms = get_pseudo_legal_moves(board)
    alpha = -99999999
    beta = 99999999
    global COLLITION_COUNTER
    global NODES_COUNT
    NODES_COUNT = 0

    # [ALO-ZORBRIST] zorbrist makes everything too slow
    if board.hash_value in TRANSPOSITION_TABLE and TRANSPOSITION_TABLE[board.hash_value]['depth'] >= depth:
        return TRANSPOSITION_TABLE[board.hash_value]['move'], TRANSPOSITION_TABLE[board.hash_value]['score']

    max_score = -123456789
    best_move = None
    scores_moves = []
    for m in lms:
        new_board = board.move(m)
        if king_in_check(new_board, False):
            continue
        score = factor * negamaxAB(new_board, -beta, -alpha, depth - 1)

        if score > max_score:
            max_score = score
            best_move = m


    # [ALO-ZORBRIST] zorbrist makes everything too slow
    board.add_to_transpotition_table(best_move, depth, max_score)
    print(NODES_COUNT, COLLITION_COUNTER)
    return best_move, max_score


def get_random_move(board, depth=1, debug=False, debug_str=""):
    lms = get_pseudo_legal_moves(board)
    lms_filtered = []
    for m in lms:
        new_board = board.move(m)
        if king_in_check(new_board, False):
            continue
        lms_filtered.append(m)
        
    if lms:
        index = random.randint(0, len(lms) - 1)
        return lms[index]
    else:
        return None

#################################
# Parallel implementation
#################################
from multiprocessing import Pool, cpu_count

def evaluate_move(args):
    board, move, depth, factor, alpha, beta = args
    score = factor * negamaxAB_parallel(board.move(move), -beta, -alpha, depth - 1)
    return move, score

def negamaxAB_parallel(board, alpha, beta, depth=0):
    if depth < 1:
        return board.eval

    factor = -board.color_to_play * 2 + 1
    lms = get_pseudo_legal_moves(board)

    with Pool(cpu_count()) as pool:
        args_list = [(board, move, depth, factor, -beta, -alpha) for move in lms]
        results = pool.map(evaluate_move, args_list)

    maxScore = max(results, key=lambda x: x[1])[1]
    if maxScore > alpha:
        alpha = maxScore
        if alpha >= beta:
            return factor * maxScore

    return factor * maxScore

def get_best_moveAB_parallel(board, depth=1):
    factor = -board.color_to_play * 2 + 1
    lms = get_pseudo_legal_moves(board)

    with Pool(cpu_count()) as pool:
        args_list = [(board, move, depth, factor, -99999999, 99999999) for move in lms]
        results = pool.map(evaluate_move, args_list)

    best_move, best_score = max(results, key=lambda x: x[1])
    return best_move, best_score


#################################
# Legacy - Good for testing
#################################

def negamax(board, depth=0, debug=False, debug_str=""):
    if depth < 1:
        if debug:
            print(debug_str, "Score: ", evaluate_board(board), "   ---   Board: \n", board)
        return evaluate_board(board)
    factor = - board.color_to_play * 2 + 1
    lms = get_pseudo_legal_moves(board)

    scores = [factor * negamax(board.move(m), depth - 1, debug, debug_str[0] * (len(debug_str) + 2)) for m in lms]
    index = np.argmax(scores)
    score = scores[index]
    if debug:
        print(debug_str, " ***! Score: ", score, "   ---   Move: \n", lms[index], "   ---   Board: \n",
              board.move(lms[index]))
    return factor * score


def get_best_move(board, depth=1, debug=False, debug_str=""):
    factor = - board.color_to_play * 2 + 1
    lms = get_pseudo_legal_moves(board)
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