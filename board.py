from utils import *
from hashing import ZOBRIST_TABLE
from precalculations import SQUARE_TO_FILE
from classes import Move, Square, Piece, Color, CastleSide

class Board(object):
    def __init__(self):
        self.pieces = np.zeros((2, 6), dtype=np.uint64)  
        self.all_pieces_per_color = np.zeros(2, dtype=np.uint64)
        self.all_pieces = np.uint64(0)  
        self.color_to_play = Color.WHITE  
        self.en_passant_sqr = None
        self.castling_available = np.ones((2, 2), dtype=bool)
        self.board_history = ""
        self.hash_value = None
        self.transposition_table = {}

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

        # [ALO-ZORBRIST] zorbrist makes everything too slow
        #self.hash_value = self.zobrist_hash()

    def move(self, m, score = None):
        board = Board()
        board.pieces = np.copy(self.pieces)
        board.all_pieces_per_color = np.copy(self.all_pieces_per_color)
        board.all_pieces = np.copy(self.all_pieces)
        board.transposition_table = self.transposition_table.copy()

        board.color_to_play = self.color_to_play

        score_str= ""
        if score:
            score_str = "_(" + str(score) + ")"
        event = "[" + self.color_to_play.name + "_" + m.piece.name + "_" + str(m.from_) + "_" + str(m.to) + score_str + "]"
        board.board_history = self.board_history + event

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

        if m.piece == Piece.KING:
            board.castling_available[board.color_to_play][:] = False
            
        if  (m.piece == Piece.ROOK):
            if board.castling_available[board.color_to_play][CastleSide.QueenSide]:
                board.castling_available[board.color_to_play][CastleSide.QueenSide] = m.from_ != 56*board.color_to_play
            elif board.castling_available[board.color_to_play][CastleSide.KingSide]:
                board.castling_available[board.color_to_play][CastleSide.KingSide] = m.from_ != 7+56*board.color_to_play
            
        # En Passant Capture
        if m.en_passant:
            if board.color_to_play == Color.WHITE:
                capture_sqr = bb_to >> np.uint(8) # down from the 'to' sqr
            else:
                capture_sqr = bb_to << np.uint(8) # up from the 'to' sqr
            board.pieces[opposite_color][Piece.PAWN] = board.pieces[opposite_color][Piece.PAWN] & ~capture_sqr
            board.all_pieces_per_color[opposite_color] = board.all_pieces_per_color[opposite_color] & ~capture_sqr
            
        # Promotion of Pawn
        if m.promotion:
            # clear pawn 
            board.pieces[board.color_to_play][Piece.PAWN] = board.pieces[board.color_to_play][Piece.PAWN] & ~bb_to  
            # add promotion piece          
            board.pieces[board.color_to_play][m.promotion] = board.pieces[board.color_to_play][m.promotion] | bb_to

        if m.castleSide: # No need to take care of the King, since already the from_-to move it 
            if board.color_to_play == Color.WHITE:
                rook_from = Square(0 if m.casleSide == CastleSide.QueenSide else 7)
                rook_to   = Square(3 if m.casleSide == CastleSide.QueenSide else 5)
                
            else: 
                rook_from = Square(56 if m.casleSide == CastleSide.QueenSide else 63)
                rook_to   = Square(59 if m.casleSide == CastleSide.QueenSide else 61)
                
            # Clear rook initial possition (m.to)
            board.pieces[board.color_to_play][Piece.ROOK] = board.pieces[board.color_to_play][Piece.ROOK] & ~ Square(rook_from).toBoard() 
            # Add rook in King initial possit
            board.pieces[board.color_to_play][Piece.ROOK] = board.pieces[board.color_to_play][Piece.ROOK] | Square(rook_to).toBoard()
        
        board.color_to_play = opposite_color
        #board.hash_value = board.zobrist_hash()
        return board

    def from_printed_board(self, pboard, color_to_play):
        self.color_to_play = color_to_play
        lettter_to_piece = {
            "p": Piece.PAWN,
            "r": Piece.ROOK,
            "n": Piece.KNIGHT,
            "b": Piece.BISHOP,
            "q": Piece.QUEEN,
            "k": Piece.KING,
        }

        for i in range(64):
            letter = pboard[7 - (i // 8)][0][(i % 8)]
            if letter == '_':
                continue
            if letter == letter.upper():
                piece_color = Color.WHITE
            else:
                piece_color = Color.BLACK

            self.pieces[piece_color][lettter_to_piece[letter.lower()]] |= Square(i).toBoard()
            self.all_pieces_per_color[piece_color] |= Square(i).toBoard()
            self.all_pieces |= Square(i).toBoard()

    def zobrist_hash(self):
        zobrist_hash_number = np.uint64(0)

        # PIECES
        for color in Color:
            for piece in Piece:
                piece_bb = self.pieces[color][piece]
                start = 0
                while piece_bb:
                    rsi = get_right_bit_index(piece_bb)
                    zobrist_hash_number ^= ZOBRIST_TABLE[("Piece", color, piece, rsi)]
                    piece_bb ^= Square(rsi).toBoard()
                    start += 1


        # SIDE TO MOVE
        if self.color_to_play == Color.BLACK:
            zobrist_hash_number ^= ZOBRIST_TABLE[("Color", Color.BLACK)]

        # CASTLING
        for color in Color:
            for castling_side in CastleSide:
                if self.castling_available[color][castling_side]:
                    zobrist_hash_number ^= ZOBRIST_TABLE[("Caslting",  color, castling_side)]

        if self.en_passant_sqr:
            zobrist_hash_number ^= ZOBRIST_TABLE[("EnPassant", SQUARE_TO_FILE[self.en_passant_sqr])]

        return zobrist_hash_number

    def add_to_transpotition_table(self, move, depth, score):
        if (self.hash_value not in self.transposition_table) or self.transposition_table[self.hash_value]['depth'] <= depth:
            self.transposition_table[self.hash_value] = \
                {
                    "depth": depth,
                    "move": move,
                    "score": score
                }