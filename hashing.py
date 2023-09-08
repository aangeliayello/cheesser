import random
from classes import Color, Piece, CastleSide, File
import numpy as np

random.seed("notoes")
LOWER_BOUND = 1
UPPER_BOUND = 2**64-1

# Generate Zobrist keys for pieces
zobrist_table = {
    ("Piece", color, piece, sqr): np.uint64(random.randint(LOWER_BOUND, UPPER_BOUND))
    for sqr in range(64)
    for color in Color
    for piece in Piece
}

# Generate Zobrist key for side to move
zobrist_table[("Color", Color.BLACK)] = np.uint64(random.randint(LOWER_BOUND, UPPER_BOUND))

# Generate Zobrist keys for castling
zobrist_table.update({
    ("Castling", color, castling_side): np.uint64(random.randint(LOWER_BOUND, UPPER_BOUND))
    for color in Color
    for castling_side in CastleSide
})

# Generate Zobrist keys for en passant
zobrist_table.update({
    ("EnPassant", file): np.uint64(random.randint(LOWER_BOUND, UPPER_BOUND))
    for file in File
})

# Convert to a NumPy array for faster indexing
#ZOBRIST_TABLE = np.array([zobrist_table[key] for key in sorted(zobrist_table.keys())])
ZOBRIST_TABLE = zobrist_table