import numpy as np

# Constants for mirroring
k1 = np.uint64(0x5555555555555555)
k2 = np.uint64(0x3333333333333333)
k4 = np.uint64(0x0f0f0f0f0f0f0f0f)

# Constants for right/left significant bit
debruij = np.uint64(0x03f79d71b4cb0a89)
right_bit_map = np.array([
    0,  1, 48,  2, 57, 49, 28,  3,
   61, 58, 50, 42, 38, 29, 17,  4,
   62, 55, 59, 36, 53, 51, 43, 22,
   45, 39, 33, 30, 24, 18, 12,  5,
   63, 47, 56, 27, 60, 41, 37, 16,
   54, 35, 52, 21, 44, 32, 23, 11,
   46, 26, 40, 15, 34, 20, 31, 10,
   25, 14, 19,  9, 13,  8,  7,  6])

left_bit_map = np.array([
    0, 47, 1, 56, 48, 27, 2, 60,
    57, 49, 41, 37, 28, 16, 3, 61,
    54, 58, 35, 52, 50, 42, 21, 44,
    38, 32, 29, 23, 17, 11, 4, 62,
    46, 55, 26, 59, 40, 36, 15, 53,
    34, 51, 20, 43, 31, 22, 10, 45,
    25, 39, 14, 33, 19, 30, 9, 24,
    13, 18, 8, 12, 7, 6, 5, 63])

# Constants for population count black magic
m1  = np.uint64(0x5555555555555555)
m2  = np.uint64(0x3333333333333333)
m4  = np.uint64(0x0f0f0f0f0f0f0f0f)
m8  = np.uint64(0x00ff00ff00ff00ff)
m16 = np.uint64(0x0000ffff0000ffff)
m32 = np.uint64(0x00000000ffffffff)
h01 = np.uint64(0x0101010101010101)

def coordinate_to_index(coordinate):
    file = ord(coordinate[0].upper()) - ord('A')
    rank = coordinate[0] - 1

    return file + rank * 8

def count_bits(x):
    x -= (x >> np.uint64(1)) & m1
    x = (x & m2) + ((x >> np.uint64(2)) & m2)
    x = (x + (x >> np.uint64(4))) & m4
    c = (x * h01) >> np.uint64(56)
    return c

def get_right_bit_index(bb):
    return right_bit_map[((bb & -bb) * debruij) >> np.uint64(58)]

def get_left_bit_index(bb):
    bb |= bb >> np.int64(1)
    bb |= bb >> np.int64(2)
    bb |= bb >> np.int64(4)
    bb |= bb >> np.int64(8)
    bb |= bb >> np.int64(16)
    bb |= bb >> np.int64(32)
    return left_bit_map[(bb * debruij) >> np.int64(58)]

def index_to_coordinate(index):
    file = index % 8
    rank = index // 8
    return chr(ord('A') + file) + str(rank + 1)

def printBb(bb):
    board = np.empty(64, dtype=str)
    board[:] = '_'
    for i in range(64):
        pos = np.uint64(1) << np.uint64(i)
        if pos & bb:
            board[i] = "X"

    board = np.flip(board.reshape((8, 8)), 0)

    print(board)

def mirror_bb_horizontal(bb):
   bb = ((bb >> np.uint64(1)) & k1) | ((bb & k1) << np.uint64(1))
   bb = ((bb >> np.uint64(2)) & k2) | ((bb & k2) << np.uint64(2))
   bb = ((bb >> np.uint64(4)) & k4) | ((bb & k4) << np.uint64(4))
   return bb
