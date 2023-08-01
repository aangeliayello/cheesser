import random
from classes import Color, Piece, CastleSide, File
import numpy as np

random.seed("notoes")

zobrist_table = []
LOWER_BOUND = 1
UPPER_BOUND = 2**64-1

# PIECES
for sqr in range(64):
    for color in Color:
        for piece in Piece:
            zobrist_table.append([("Piece", color, piece, sqr), np.uint64(random.randint(LOWER_BOUND, UPPER_BOUND))])

# SIDE TO MOVE
zobrist_table.append([("Color", Color.BLACK), np.uint64(random.randint(LOWER_BOUND, UPPER_BOUND))])

# CASTLING
for color in Color:
    for castling_side in CastleSide:
        zobrist_table.append([("Caslting", color, castling_side), np.uint64(random.randint(LOWER_BOUND, UPPER_BOUND))])

for file in File:
    zobrist_table.append([("EnPassant", file), np.uint64(random.randint(LOWER_BOUND, UPPER_BOUND))])

ZOBRIST_TABLE = dict(zobrist_table)