import os
import pickle
from utils import *

def get_kingLike_moves(bb):
    w = (bb >> np.uint64(1)) & ~Files[File.H]
    e = (bb << np.uint64(1)) & ~Files[File.A]
    s = bb >> np.uint64(8)
    n = bb << np.uint64(8)

    sw = (bb >> np.uint64(9)) & ~Files[File.H]
    nw = (bb << np.uint64(7)) & ~Files[File.H]
    se = (bb >> np.uint64(7)) & ~Files[File.A]
    ne = (bb << np.uint64(9)) & ~Files[File.A]

    return w | e | s | n | sw | nw | se | ne

def get_knightLike_moves(bb):
    # _H_A_
    # G___B
    # __X__
    # F___C
    # _E_D_
    file_A_B = (Files[File.A] | Files[File.B])
    file_G_H = (Files[File.G] | Files[File.H])

    a = (bb << np.uint64(17)) & ~Files[File.A]
    b = (bb << np.uint64(10)) & ~file_A_B
    c = (bb >> np.uint64(6)) & ~file_A_B
    d = (bb >> np.uint64(15)) & ~Files[File.A]

    e = (bb >> np.uint64(17)) & ~Files[File.H]
    f = (bb >> np.uint64(10)) & ~file_G_H
    g = (bb << np.uint64(6)) & ~file_G_H
    h = (bb << np.uint64(15)) & ~Files[File.H]

    return a | b | c | d | e | f | g | h

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

data_dir = "tables"
os.makedirs(data_dir, exist_ok=True)

files_path = os.path.join(data_dir, "files.pkl")
ranks_path = os.path.join(data_dir, "ranks.pkl")
if os.path.exists(files_path) and os.path.exists(ranks_path):
    with open(files_path, "rb") as file:
        Files = pickle.load(file)
    with open(ranks_path, "rb") as file:
        Ranks = pickle.load(file)
else:
    print("RECALCULATING: FILES AND RANK TABLES")

    A_file = np.uint64(0b0000000100000001000000010000000100000001000000010000000100000001)
    Files = np.array([A_file << np.uint64(i) for i in range(8)], dtype=np.uint64)

    First_rank = np.uint64(0b0000000000000000000000000000000000000000000000000000000011111111)
    Ranks = np.array([First_rank << np.uint64(i*8) for i in range(8)], dtype=np.uint64)
    with open(files_path, "wb") as file:
        pickle.dump(Files, file)
    with open(ranks_path, "wb") as file:
        pickle.dump(Ranks, file)
        
file_mask_path = os.path.join(data_dir, "file_mask.pkl")
rank_mask_path = os.path.join(data_dir, "rank_mask.pkl")
square_to_file_path = os.path.join(data_dir, "square_to_file.pkl")
if os.path.exists(file_mask_path) and os.path.exists(rank_mask_path) and os.path.exists(square_to_file_path):
    with open(file_mask_path, "rb") as file:
        FILE_MASK = pickle.load(file)
    with open(rank_mask_path, "rb") as file:
        RANK_MASK = pickle.load(file)
    with open(square_to_file_path, "rb") as file:
        SQUARE_TO_FILE = pickle.load(file)
else:
    print("RECALCULATING: FILES MASK, RANK MASK, AND SQUARE-TO-FILE")

    file_mask = []
    rank_mask = []
    square_to_file = []
    for i in range(64):
        sq_bb = Square(i).toBoard()
        file = i%8
        rank = i//8
        file_mask.append((sq_bb, Files[file]))
        rank_mask.append((sq_bb, Ranks[rank]))
        square_to_file.append((i, File(file)))
    FILE_MASK = dict(file_mask)
    RANK_MASK = dict(rank_mask)
    SQUARE_TO_FILE = dict(square_to_file)
    
    with open(file_mask_path, "wb") as file:
        pickle.dump(FILE_MASK, file)
    with open(rank_mask_path, "wb") as file:
        pickle.dump(RANK_MASK, file)
    with open(square_to_file_path, "wb") as file:
        pickle.dump(SQUARE_TO_FILE, file)

diagonal_mask_path = os.path.join(data_dir, "diagonal_mask.pkl")
anti_diagonal_mask_path = os.path.join(data_dir, "anti_diagonal_mask.pkl")
if os.path.exists(diagonal_mask_path) and os.path.exists(anti_diagonal_mask_path):
    with open(diagonal_mask_path, "rb") as file:
        DIAGONAL_MASK = pickle.load(file)
    with open(anti_diagonal_mask_path, "rb") as file:
        ANTI_DIAGONAL_MASK = pickle.load(file)
else:
    print("RECALCULATING: DIAGONAL AND ANTI-DIAGONAL MASKS")

    A1H8_diagonal = np.uint64(0b1000000001000000001000000001000000001000000001000000001000000001)
    north_diagonals = []
    south_diagonals = []
    north_shifted_diag = A1H8_diagonal
    south_shifted_diag = A1H8_diagonal

    for i in range(1,8):
        north_shifted_diag = north_shifted_diag << np.uint64(8)
        south_shifted_diag = south_shifted_diag >> np.uint64(8)
        north_diagonals.append(north_shifted_diag)
        south_diagonals.append(south_shifted_diag)
    north_diagonals.reverse()
    diagonals = north_diagonals + [A1H8_diagonal] + south_diagonals
    anti_diagonals = []
    for d in diagonals:
        anti_diagonals.append(mirror_bb_horizontal(d))

    anti_diagonal_masks = []
    diagonal_masks = []
    for i in range(64):
        sqr_bb = Square(i).toBoard()
        for d in diagonals:
            if d & sqr_bb:
                diagonal_masks.append((sqr_bb, d))
                break
        for ad in anti_diagonals:
            if ad & sqr_bb:
                anti_diagonal_masks.append((sqr_bb, ad))
                break

    ANTI_DIAGONAL_MASK = dict(anti_diagonal_masks)
    DIAGONAL_MASK = dict(diagonal_masks)
    with open(diagonal_mask_path, "wb") as file:
        pickle.dump(DIAGONAL_MASK, file)
    with open(anti_diagonal_mask_path, "wb") as file:
        pickle.dump(ANTI_DIAGONAL_MASK, file)
        
# KING_MOVES
king_moves_path = os.path.join(data_dir, "king_moves.pkl")
if os.path.exists(king_moves_path):
    with open(king_moves_path, "rb") as file:
        KING_MOVES = pickle.load(file)
else:
    print("RECALCULATING: KING MOVES")
    KING_MOVES = dict([(Square(i).toBoard(), get_kingLike_moves(Square(i).toBoard())) for i in range(64)])
    with open(king_moves_path, "wb") as file:
        pickle.dump(KING_MOVES, file)

# KNIGHT_MOVES
knight_moves_path = os.path.join(data_dir, "knight_moves.pkl")
if os.path.exists(knight_moves_path):
    with open(knight_moves_path, "rb") as file:
        KNIGHT_MOVES = pickle.load(file)
else:
    print("RECALCULATING: KING MOVES")
    KNIGHT_MOVES = dict([(Square(i).toBoard(), get_knightLike_moves(Square(i).toBoard())) for i in range(64)])
    with open(knight_moves_path, "wb") as file:
        pickle.dump(KNIGHT_MOVES, file)

# RANK_MOVES
rank_moves_path = os.path.join(data_dir, "rank_moves.pkl")
if os.path.exists(rank_moves_path):
    with open(rank_moves_path, "rb") as file:
        RANK_MOVES = pickle.load(file)
else:
    print("RECALCULATING: RANK MOVES")
    rank_moves = []
    for square in range(8):
        sq_bb = Square(square).toBoard()
        for occupancy in range(256):
            occupancy_bb = np.uint64(occupancy)
            for shift in range(8):
                shifted_sqr_bb = sq_bb << np.uint64(8 * shift)
                shifted_occupancy = occupancy_bb << np.uint64(8 * shift)
                key = (shifted_sqr_bb, shifted_occupancy)
                rank_moves.append([key, get_rank_moves(shifted_sqr_bb, shifted_occupancy)])
    RANK_MOVES = dict(rank_moves)
    with open(rank_moves_path, "wb") as file:
        pickle.dump(RANK_MOVES, file)

# FILE_MOVES
file_moves_path = os.path.join(data_dir, "file_moves.pkl")
white_pawn_moves_path = os.path.join(data_dir, "white_pawn_moves.pkl")
black_pawn_moves_path = os.path.join(data_dir, "black_pawn_moves.pkl")
if os.path.exists(file_moves_path) and os.path.exists(white_pawn_moves_path) and os.path.exists(black_pawn_moves_path):
    with open(file_moves_path, "rb") as file:
        FILE_MOVES = pickle.load(file)
    with open(white_pawn_moves_path, "rb") as file:
        WHITE_PAWN_MOVES = pickle.load(file)
    with open(black_pawn_moves_path, "rb") as file:
        BLACK_PAWN_MOVES = pickle.load(file)
else:
    print("RECALCULATING: FILES AND PAWN SIMPLE MOVES")
    file_moves = []
    white_pawn_simple_moves = []
    black_pawn_simple_moves = []
    for occupancy in range(256):

        occupancy_bb = np.uint64(occupancy)
        rotated_occupancy_bb = np.uint64(0)

        # rotate first rank to the A-File
        for i in range(8):
            # pick the ith bit and move it diagonally i times
            rotated_occupancy_bb |= (occupancy_bb & (np.uint64(1) << np.uint64(i)))  << np.uint64(7*i)
        for square in range(8):
            sq_bb = Square(square*8).toBoard()
            for shift in range(8):
                shifted_sqr_bb = sq_bb << np.uint64(shift)
                shifted_occupancy = rotated_occupancy_bb << np.uint64(shift)
                key = (shifted_sqr_bb, shifted_occupancy)
                file_moves.append([key, get_file_moves(shifted_sqr_bb, shifted_occupancy)])
                white_pawn_simple_moves.append([key, get_pawn_moves_white(shifted_sqr_bb, shifted_occupancy)])
                black_pawn_simple_moves.append([key, get_pawn_moves_black(shifted_sqr_bb, shifted_occupancy)])

    FILE_MOVES = dict(file_moves)
    WHITE_PAWN_MOVES = dict(white_pawn_simple_moves)
    BLACK_PAWN_MOVES = dict(black_pawn_simple_moves)
    
    with open(file_moves_path, "wb") as file:
        pickle.dump(FILE_MOVES, file)
    with open(white_pawn_moves_path, "wb") as file:
        pickle.dump(WHITE_PAWN_MOVES, file)
    with open(black_pawn_moves_path, "wb") as file:
        pickle.dump(BLACK_PAWN_MOVES, file)

white_pawn_attack_moves_path = os.path.join(data_dir, "white_pawn_attack_moves.pkl")
black_pawn_attack_moves_path = os.path.join(data_dir, "black_pawn_attack_moves.pkl")
if os.path.exists(white_pawn_attack_moves_path) and os.path.exists(black_pawn_attack_moves_path):
    with open(white_pawn_attack_moves_path, "rb") as file:
        WHITE_PAWN_ATTACK_MOVES = pickle.load(file)
    with open(black_pawn_attack_moves_path, "rb") as file:
        BLACK_PAWN_ATTACK_MOVES = pickle.load(file)
else:
    print("RECALCULATING: PANW ATTACK MOVES")
    white_pawn_attack_moves = []
    black_pawn_attack_moves = []
    for square in range(8):
        sq_bb = Square(square).toBoard()
        for occupancy in range(256):
            occupancy_bb = np.uint64(occupancy)
            for shift in range(6):
                # White
                shifted_white_sqr_bb = sq_bb << np.uint64(8*(shift+1)) # start in 2nd rank and finish in the 7th rank
                shifted_white_occupancy = occupancy_bb << np.uint64(8*(shift+2)) # only care about the occupancy in the rank infront of the pawn
                key = (shifted_white_sqr_bb, shifted_white_occupancy)
                white_pawn_attack_moves.append([key,get_pawn_attacks_white(shifted_white_sqr_bb, shifted_white_occupancy)])

            for shift in range(6):
                # Black
                shifted_black_sqr_bb = sq_bb << np.uint64(8*(7 - shift -1)) #start in the 7th rank and finish in the 2nd rank
                shifted_black_occupancy = occupancy_bb << np.uint64(8 * (7 - shift - 2))
                key = (shifted_black_sqr_bb, shifted_black_occupancy)
                black_pawn_attack_moves.append([key, get_pawn_attacks_black(shifted_black_sqr_bb, shifted_black_occupancy)])

    WHITE_PAWN_ATTACK_MOVES = dict(white_pawn_attack_moves)
    BLACK_PAWN_ATTACK_MOVES = dict(black_pawn_attack_moves)
    with open(white_pawn_attack_moves_path, "wb") as file:
        pickle.dump(WHITE_PAWN_ATTACK_MOVES, file)
    with open(black_pawn_attack_moves_path, "wb") as file:
        pickle.dump(BLACK_PAWN_ATTACK_MOVES, file)

# DIAGONAL_MOVES
diagonal_moves_path = os.path.join(data_dir, "diagonal_moves.pkl")
anti_diagonal_moves_path = os.path.join(data_dir, "anti_diagonal_moves.pkl")
if os.path.exists(diagonal_moves_path) and os.path.exists(anti_diagonal_moves_path):
    with open(diagonal_moves_path, "rb") as file:
        DIAGONAL_MOVES = pickle.load(file)
    with open(anti_diagonal_moves_path, "rb") as file:
        ANTI_DIAGONAL_MOVES = pickle.load(file)
else:
    print("RECALCULATING: DIAGONAL AND ANTI-DIAGONAL MOVES")
    diagonal_moves = []
    anti_diagonal_moves = []
    for occupancy in range(256):
        occupancy_bb = np.uint64(occupancy)
        diagonal_occupancy_bb = np.uint64(0)

        # rotate first rank to the main diagonal
        for i in range(8):
            # pick the ith bit and move it up 8*i times
            diagonal_occupancy_bb |= (occupancy_bb & (np.uint64(1) << np.uint64(i))) << np.uint64(8*i)

        for square in range(8):
            sq_bb = Square(square).toBoard() << np.uint64(8*square)

            for shift in range(7):
                shifted_sqr_bb = sq_bb << np.uint64(8*(7-shift))
                shifted_occupancy = diagonal_occupancy_bb << np.uint64(8*(7-shift))
                key = (shifted_sqr_bb, shifted_occupancy)
                if shifted_sqr_bb!= 0:
                    diagonal_moves.append([key, get_right_diagonal_moves(shifted_sqr_bb, shifted_occupancy)])

                shifted_sqr_bb = mirror_bb_horizontal(shifted_sqr_bb)
                shifted_occupancy = mirror_bb_horizontal(shifted_occupancy)
                key = (shifted_sqr_bb, shifted_occupancy)
                if shifted_sqr_bb != 0:
                    anti_diagonal_moves.append([key, get_left_diagonal_moves(shifted_sqr_bb, shifted_occupancy)])

            for shift in range(8):
                shifted_sqr_bb = sq_bb >> np.uint64(8*shift)
                shifted_occupancy = diagonal_occupancy_bb >> np.uint64(8*shift)
                key = (shifted_sqr_bb, shifted_occupancy)
                if shifted_sqr_bb != 0:
                    diagonal_moves.append([key, get_right_diagonal_moves(shifted_sqr_bb, shifted_occupancy)])

                shifted_sqr_bb = mirror_bb_horizontal(shifted_sqr_bb)
                shifted_occupancy = mirror_bb_horizontal(shifted_occupancy)
                key = (shifted_sqr_bb, shifted_occupancy)
                if shifted_sqr_bb != 0:
                    anti_diagonal_moves.append([key, get_left_diagonal_moves(shifted_sqr_bb, shifted_occupancy)])

    DIAGONAL_MOVES = dict(diagonal_moves)
    ANTI_DIAGONAL_MOVES = dict(anti_diagonal_moves)

    with open(diagonal_moves_path, "wb") as file:
        pickle.dump(DIAGONAL_MOVES, file)
    with open(anti_diagonal_moves_path, "wb") as file:
        pickle.dump(ANTI_DIAGONAL_MOVES, file)