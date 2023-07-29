import numpy

from utils import *

A_file = np.uint64(0b0000000100000001000000010000000100000001000000010000000100000001)
Files = np.array([A_file << np.uint64(i) for i in range(8)], dtype=np.uint64)

First_rank = np.uint64(0b0000000000000000000000000000000000000000000000000000000011111111)
Ranks = np.array([First_rank << np.uint64(i*8) for i in range(8)], dtype=np.uint64)

file_mask = []
rank_mask = []
for i in range(64):
    sq_bb = Square(i).toBoard()
    file = i%8
    rank = i//8
    file_mask.append((sq_bb, Files[file]))
    rank_mask.append((sq_bb, Ranks[rank]))

FILE_MASK = dict(file_mask)
RANK_MASK = dict(rank_mask)

def get_kingLike_moves(bb):
    w = (bb >> np.uint64(1)) & ~Files[File.H]
    e = (bb << np.uint64(1)) & ~A_file
    s = bb >> np.uint64(8)
    n = bb << np.uint64(8)

    sw = (bb >> np.uint64(9)) & ~Files[File.H]
    nw = (bb << np.uint64(7)) & ~Files[File.H]
    se = (bb >> np.uint64(7)) & ~A_file
    ne = (bb << np.uint64(9)) & ~A_file

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

KING_MOVES = dict([ (Square(i).toBoard(),get_kingLike_moves(Square(i).toBoard())) for i in range(64)])
KNIGHT_MOVES = dict([ (Square(i).toBoard(),get_knightLike_moves(Square(i).toBoard())) for i in range(64)])

rank_moves = []
for square in range(8):
    sq_bb = Square(square).toBoard()
    for occupancy in range(256):
        occupancy_bb = np.uint64(occupancy)
        for shift in range(8):
            shifted_sqr_bb = sq_bb << np.uint64(8*shift)
            shifted_occupancy = occupancy_bb << np.uint64(8*shift)
            key = (shifted_sqr_bb, shifted_occupancy)
            rank_moves.append([key,get_rank_moves(shifted_sqr_bb, shifted_occupancy)])

RANK_MOVES = dict(rank_moves)

file_moves = []
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

FILE_MOVES = dict(file_moves)

