import numpy as np
from enum import IntEnum
# TODO:
#     Game:
#     - Implement promotions
#     - Implement En pasant
#     - Implement check for check
#
#     Speed:
#     Speed:
#     - Pre calculate tables
#     - Implement En pasant
#     - Implement check for check

m1  = np.uint64(0x5555555555555555)
m2  = np.uint64(0x3333333333333333)
m4  = np.uint64(0x0f0f0f0f0f0f0f0f)
m8  = np.uint64(0x00ff00ff00ff00ff)
m16 = np.uint64(0x0000ffff0000ffff)
m32 = np.uint64(0x00000000ffffffff)
h01 = np.uint64(0x0101010101010101)


# center count
ring0 = np.uint64(0b0000000000000000000000000001100000011000000000000000000000000000)
ring1 = np.uint64(0b0000000000000000001111000010010000100100001111000000000000000000)

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

A_file = np.uint64(0b0000000100000001000000010000000100000001000000010000000100000001)
Files = np.array([A_file << np.uint64(i) for i in range(8)], dtype=np.uint64)

First_rank = np.uint64(0b0000000000000000000000000000000000000000000000000000000011111111)
Ranks = np.array([First_rank << np.uint64(i*8) for i in range(8)], dtype=np.uint64)

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

class Move(object):
    def __init__(self, from_, to, piece, promotion = None, en_passant = False, castleSide = None):
        self.from_ = from_
        self.to = to
        self.piece = piece
        self.promotion = promotion
        self.en_passant = en_passant
        self.castleSide = castleSide
        
    def __str__(self):
        return self.piece.name + ": " + "(" + str(self.from_) + ", " + str(self.to) + ")"

def count_bits(x):
    x -= (x >> np.uint64(1)) & m1
    x = (x & m2) + ((x >> np.uint64(2)) & m2)
    x = (x + (x >> np.uint64(4))) & m4
    c = (x * h01) >> np.uint64(56)
    print(c)
    return c

def evaluate_board(board):
    score = 0

    score_map = {
        Piece.PAWN: 1000,
        Piece.KNIGHT: 3000,
        Piece.BISHOP: 3250,
        Piece.ROOK: 5000,
        Piece.QUEEN: 9000,
        Piece.KING: 999999999,
    }

    if board.color_to_play == Color.WHITE:
        score += 0
    else:
        score -= 0

    # piece count
    for color in Color:
        if color == Color.WHITE: factor = 1
        else: factor = -1

        for piece in Piece:

            count = count_bits(board.pieces[color][piece])

            if piece != Piece.KING:
                count0 = count_bits(board.pieces[color][piece] & ring0)
                count1 = count_bits(board.pieces[color][piece] & ring1)
            else:
                count0 = 0
                count1 = 0
            score += (count + count0 * 0.005 + count1 * 0.001) * factor * score_map[piece]

    return score

class Board(object):
    def __init__(self):
        self.pieces = np.zeros((2, 6), dtype=np.uint64)  
        self.all_pieces_per_color = np.zeros(2, dtype=np.uint64)
        self.all_pieces = np.uint64(0)  
        self.color_to_play = Color.WHITE  
        self.en_passant_sqr = None
        self.castling_available =  
        
    def __str__(self):
        board = np.empty(64, dtype=str)
        board[:] = '_'
        for i in range(64):
            pos = np.uint64(1) << np.uint64(i)
            colorBreak = False
            for color in Color:
                if colorBreak: break
                for piece in Piece:
                    if pos & self.pieces[color][piece]:
                        colorBreak = True
                        board[i] = piece.toChar(color)
                        break

        board = np.flip(board.reshape((8, 8)), 0)

        return str(board)

    def base_board(self):
        self.color_to_play = Color.WHITE  # Color to move
        self.en_passant_sqr = None
        
        # paws
        self.pieces[Color.WHITE][Piece.PAWN] = np.uint64(
            0b0000000000000000000000000000000000000000000000001111111100000000)
        self.pieces[Color.BLACK][Piece.PAWN] = np.uint64(
            0b0000000011111111000000000000000000000000000000000000000000000000)

        # rook
        self.pieces[Color.WHITE][Piece.ROOK] = np.uint64(
            0b0000000000000000000000000000000000000000000000000000000010000001)
        self.pieces[Color.BLACK][Piece.ROOK] = np.uint64(
            0b1000000100000000000000000000000000000000000000000000000000000000)

        # horse
        self.pieces[Color.WHITE][Piece.KNIGHT] = np.uint64(
            0b0000000000000000000000000000000000000000000000000000000001000010)
        self.pieces[Color.BLACK][Piece.KNIGHT] = np.uint64(
            0b0100001000000000000000000000000000000000000000000000000000000000)

        # bishop
        self.pieces[Color.WHITE][Piece.BISHOP] = np.uint64(
            0b0000000000000000000000000000000000000000000000000000000000100100)
        self.pieces[Color.BLACK][Piece.BISHOP] = np.uint64(
            0b0010010000000000000000000000000000000000000000000000000000000000)

        # queen
        self.pieces[Color.WHITE][Piece.QUEEN] = np.uint64(
            0b0000000000000000000000000000000000000000000000000000000000001000)
        self.pieces[Color.BLACK][Piece.QUEEN] = np.uint64(
            0b0000100000000000000000000000000000000000000000000000000000000000)

        # king
        self.pieces[Color.WHITE][Piece.KING] = np.uint64(
            0b0000000000000000000000000000000000000000000000000000000000010000)
        self.pieces[Color.BLACK][Piece.KING] = np.uint64(
            0b0001000000000000000000000000000000000000000000000000000000000000)

        self.all_pieces_per_color[Color.WHITE] = np.uint64(
            0b0000000000000000000000000000000000000000000000001111111111111111)
        self.all_pieces_per_color[Color.BLACK] = np.uint64(
            0b1111111111111111000000000000000000000000000000000000000000000000)
        self.all_pieces = np.uint64(
            0b1111111111111111000000000000000000000000000000001111111111111111)

    def move(self, m):
        board = Board()
        board.pieces = np.copy(self.pieces)
        board.all_pieces_per_color = np.copy(self.all_pieces_per_color)
        board.all_pieces = np.copy(self.all_pieces)
        board.color_to_play = self.color_to_play

        bb_not_from = ~ Square(m.from_).toBoard()
        bb_to = Square(m.to).toBoard()

        # En Passant
        if m.piece == Piece.PAWN and abs(m.from_ - m.to) == 16:
            board.en_passant_sqr = m.from_ + (1 - 2*board.color_to_play)*8
        else:
            board.en_passant_sqr = None
            
        # Same color
        board.pieces[board.color_to_play][m.piece] = (board.pieces[board.color_to_play][m.piece] & bb_not_from) | bb_to
        board.all_pieces_per_color[board.color_to_play] = (board.all_pieces_per_color[board.color_to_play] & bb_not_from) | bb_to

        # All color joint bb
        board.all_pieces = (board.all_pieces & bb_not_from) | bb_to

        # Capture
        opposite_color = board.color_to_play.flip()
        isCapture = bb_to & board.all_pieces_per_color[opposite_color]

        if isCapture:
            for piece in Piece:
                board.pieces[opposite_color][piece] = board.pieces[opposite_color][piece] & ~bb_to
            board.all_pieces_per_color[opposite_color] = board.all_pieces_per_color[opposite_color] & ~bb_to

        board.color_to_play = opposite_color

        return board

class Square(object):
    def __init__(self, index):
        self.index = index

    def toBoard(self):
        return np.uint64(1) << np.uint64(self.index)

    def fromBoard(self):
        None

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

def get_rook_moves(bb, occupancy, same_color_occupancy):
    return (get_file_moves(bb, occupancy) | get_rank_moves(bb, occupancy)) & ~ same_color_occupancy

def get_bishop_move(bb, occupancy, same_color_occupancy):
    return (get_right_diagonal_moves(bb, occupancy) | get_left_diagonal_moves(bb, occupancy)) & ~ same_color_occupancy

def get_queen_move(bb, occupancy, same_color_occupancy):
    return (get_bishop_move(bb, occupancy, same_color_occupancy) | get_rook_moves(bb, occupancy, same_color_occupancy))

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
    if piece == Piece.PAWN:
        # TODO: Add en pasant
        if board.color_to_play == Color.WHITE:
            movesSimple = get_pawn_moves_white(sq.toBoard(), board.all_pieces)
            movesAttack = get_pawn_attacks_white(sq.toBoard(), board.all_pieces_per_color[Color.BLACK])
            moves = movesSimple | movesAttack
        else:
            moves = get_pawn_moves_black(sq.toBoard(), board.all_pieces) | get_pawn_attacks_white(sq.toBoard(), board.all_pieces_per_color[Color.WHITE])
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
        start = right_bit_index + 1

        list_of_moves.append(Move(from_, right_bit_index, piece))

        moves = moves & ~Square(right_bit_index).toBoard()

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
#
# def negamax(board, depth = 0, debug = False, debug_str = ""):
#     if depth < 1:
#         if debug:
#             print(debug_str, "Score: ", evaluate_board(board), "   ---   Board: \n", board)
#         return evaluate_board(board)
#     factor = - board.color_to_play * 2 + 1
#     lms = get_legal_moves(board)
#
#     scores = [factor*negamax(board.move(m), depth - 1, debug, debug_str[0]*(len(debug_str) +2)) for m in lms]
#     index = np.argmax(scores)
#     score = scores[index]
#     if debug:
#         print(debug_str, " ***! Score: ", score, "   ---   Move: \n", lms[index], "   ---   Board: \n", board.move(lms[index]))
#     return factor*score
#
# def get_best_move(board, depth = 1, debug = False, debug_str = ""):
#     factor = - board.color_to_play * 2 + 1
#     lms = get_legal_moves(board)
#     lbs = []
#     for m in lms:
#         print(debug_str, "Move: ", m)
#         score = factor*negamax(board.move(m), depth - 1, debug, debug_str[0]*(len(debug_str) +2))
#         print(debug_str,'        Score: ', score)
#
#         lbs.append(score)
#     index = np.argmax([m for m in lbs])
#     if debug:
#         print(debug_str, "Score: ", factor*lbs[index], "   ---   Move: ", lms[index])
#
#     return lms[index]

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


