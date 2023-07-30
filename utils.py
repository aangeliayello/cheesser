import numpy as np
from enum import IntEnum

ring0 = np.uint64(0b0000000000000000000000000001100000011000000000000000000000000000)
ring1 = np.uint64(0b0000000000000000001111000010010000100100001111000000000000000000)

class Square(object):
    def __init__(self, index):
        self.index = index

    def toBoard(self):
        return np.uint64(1) << np.uint64(self.index)

    def fromBoard(self):
        None
        
class Color(IntEnum):
    WHITE = 0
    BLACK = 1

    def flip(self):
        if self == Color.WHITE:
            return Color.BLACK
        else:
            return Color.WHITE

class File(IntEnum):
    A = 0
    B = 1
    C = 2
    D = 3
    E = 4
    F = 5
    G = 6
    H = 7

class Rank(IntEnum):
    One = 0
    Two = 1
    Three = 2
    Four = 3
    Five = 4
    Six = 5
    Seven = 6
    Eight = 7
    
class SpecialMoveType(IntEnum):
    EnPassant = 0
    QueenSideCastle = 1
    KingSideCastle = 2
    
class CastleSide(IntEnum):
    QueenSide = 0
    KingSide = 1
    
class Piece(IntEnum):
    PAWN = 0
    KNIGHT = 1
    BISHOP = 2
    ROOK = 3
    QUEEN = 4
    KING = 5

    def toChar(self, color=None):
        if self == Piece.PAWN:
            c = 'p'
        elif self == Piece.KNIGHT:
            c = 'n'
        elif self == Piece.BISHOP:
            c = 'b'
        elif self == Piece.ROOK:
            c = 'r'
        elif self == Piece.QUEEN:
            c = 'q'
        elif self == Piece.KING:
            c = 'k'

        if color == Color.WHITE:
            c = c.upper()
        return c

def coordinate_to_index(coordinate):
    file = ord(coordinate[0].upper()) - ord('A')
    rank = coordinate[0] - 1

    return file + rank * 8

def get_right_bit_index(bb, start = 0):
    power = np.uint64(1) << np.uint8(start)

    for i in range(64-start):
        if power & bb:
            break
        power = power << np.uint8(1)

    return i+start

def get_left_bit_index(bb):
    power = np.uint64(2**63)
    for i in range(64):
        if power & bb:
            break
        power = power >> np.uint8(1)
    return 63 - i

def index_to_coordinate(index):
    file = index % 8
    rank = index // 8

    return chr(ord('A') + file) + str(rank + 1)

def getRank(bb):
    get_right_bit_index(bb) % 8

def getFile(bb):
    get_right_bit_index(bb) // 8

def printBb(bb):
    board = np.empty(64, dtype=str)
    board[:] = '_'
    for i in range(64):
        pos = np.uint64(1) << np.uint64(i)
        if pos & bb:
            board[i] = "X"

    board = np.flip(board.reshape((8, 8)), 0)

    print(board)