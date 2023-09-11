from enum import IntEnum
import numpy as np

CHECK_MATE_SCORE = 999999999999

class Move(object):
    def __init__(self, piece, from_, to, promotion=None, en_passant_capture=False, castleSide=None):
        self.from_ = from_
        self.to = to
        self.piece = piece
        self.promotion = promotion
        self.en_passant_capture = en_passant_capture
        self.castleSide = castleSide

    def __str__(self):
        castle_str = ''
        if self.castleSide is not None:
            castle_str = ", " + self.castleSide.name
        return self.piece.name + ": " + "(" + str(self.from_) + ", " + str(self.to) + castle_str + ")"

SQUARE_TO_BOARD = dict([(i, np.uint64(1) << np.uint64(i)) for i in range(64)])
class Square(object):
    def __init__(self, index):
        self.index = index

    def toBoard(self):
        return SQUARE_TO_BOARD[self.index]

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

class KingStatus(IntEnum):
    NotInCheck = 0
    InCheck = 1
    NoKing = 2