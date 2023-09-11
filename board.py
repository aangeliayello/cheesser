from utils import *
from hashing import ZOBRIST_TABLE
from precalculations import SQUARE_TO_FILE
from classes import Square, Piece, Color, CastleSide
from evaluation import evaluate_board, board_evaluation_move_correction

TRANSPOSITION_TABLE = {}
NODES_COUNTER = 0
class Board(object):
    def __init__(self):
        self.pieces = np.zeros((2, 6), dtype=np.uint64)  
        self.all_pieces_per_color = np.zeros(2, dtype=np.uint64)
        self.all_pieces = np.uint64(0)  
        self.color_to_play = Color.WHITE  
        self.en_passant_sqr = None
        self.castling_available = np.ones((2, 2), dtype=bool)
        self.keep_board_history = False
        self.board_history = ""
        self.hash_value = None
        self.eval = 0

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

        return str(board)+"\n Color: "+str(self.color_to_play) + "\n Castling:" + str(self.castling_available.flatten()) + "\n En Passant: " + str(self.en_passant_sqr)

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

        self.eval = evaluate_board(self)
        self.hash_value = self.zobrist_hash()

    def move(self, m, score = None):
        board = Board()
        board.pieces = np.copy(self.pieces)
        board.all_pieces_per_color = np.copy(self.all_pieces_per_color)
        board.all_pieces = np.copy(self.all_pieces)
        board.castling_available = np.copy(self.castling_available)
        board.color_to_play = self.color_to_play
        board.keep_board_history = self.keep_board_history
        zobrist_hash_number = self.hash_value

        if board.keep_board_history:
            score_str= ""
            if score:
                score_str = "_(" + str(round(score, 3)) + ")"
            event = "[" + self.color_to_play.name + "_" + m.piece.name + "_" + str(m.from_) + "_" + str(m.to) + score_str + "]"
            board.board_history = self.board_history + event

        color_to_play = board.color_to_play
        opposite_color = color_to_play.flip()
        bb_not_from = ~ Square(m.from_).toBoard()
        bb_to = Square(m.to).toBoard()

        # En Passant Square
        if self.en_passant_sqr is not None:
            # clear en_passant in zobrist hash if initial board had an en-passant
            zobrist_hash_number ^= ZOBRIST_TABLE[("EnPassant", SQUARE_TO_FILE[self.en_passant_sqr])]

        if m.piece == Piece.PAWN and abs(m.from_ - m.to) == 16:
            board.en_passant_sqr = m.from_ + (1 - 2*color_to_play)*8
            zobrist_hash_number ^= ZOBRIST_TABLE[("EnPassant", SQUARE_TO_FILE[board.en_passant_sqr])]
        else:
            board.en_passant_sqr = None

        # En Passant Capture
        if m.en_passant_capture:
            if color_to_play == Color.WHITE:
                capture_sqr = bb_to >> np.uint(8)  # down from the 'to' sqr
            else:
                capture_sqr = bb_to << np.uint(8)  # up from the 'to' sqr
            board.pieces[opposite_color][Piece.PAWN] = board.pieces[opposite_color][Piece.PAWN] & ~capture_sqr
            board.all_pieces_per_color[opposite_color] = board.all_pieces_per_color[opposite_color] & ~capture_sqr
            zobrist_hash_number ^= ZOBRIST_TABLE[("Piece", opposite_color, Piece.PAWN, right_bit_map(capture_sqr))]

        # Promotion of Pawn
        if m.promotion is not None:
            # clear pawn
            board.pieces[color_to_play][Piece.PAWN] = board.pieces[color_to_play][Piece.PAWN] & ~bb_to
            zobrist_hash_number ^= ZOBRIST_TABLE[("Piece", color_to_play, Piece.PAWN, m.to)]

            # add promotion piece
            board.pieces[color_to_play][m.promotion] = board.pieces[color_to_play][m.promotion] | bb_to
            zobrist_hash_number ^= ZOBRIST_TABLE[("Piece", color_to_play, m.promotion, m.to)]


        # Same color
        board.pieces[color_to_play][m.piece] = (board.pieces[color_to_play][m.piece] & bb_not_from) | bb_to
        board.all_pieces_per_color[color_to_play] = (board.all_pieces_per_color[color_to_play] & bb_not_from) | bb_to
        zobrist_hash_number ^= ZOBRIST_TABLE[("Piece", color_to_play, m.piece, m.from_)]
        zobrist_hash_number ^= ZOBRIST_TABLE[("Piece", color_to_play, m.piece, m.to)]

        # All color joint bb
        board.all_pieces = (board.all_pieces & bb_not_from) | bb_to

        # Capture (Non-En-Passant)
        captured_piece_non_en_passant = None
        if bb_to & board.all_pieces_per_color[opposite_color]:
            for piece in Piece:
                if board.pieces[opposite_color][piece] & bb_to:
                    captured_piece_non_en_passant = piece
                    board.pieces[opposite_color][piece] = board.pieces[opposite_color][piece] & ~bb_to
                    zobrist_hash_number ^= ZOBRIST_TABLE[("Piece", opposite_color, piece, m.to)]
                    break

            board.all_pieces_per_color[opposite_color] = board.all_pieces_per_color[opposite_color] & ~bb_to

        delta_castling_rights = 0
        if m.piece == Piece.KING:
            delta_castling_rights = -self.castling_available[color_to_play].sum()
            board.castling_available[color_to_play][:] = False
            
        if (m.piece == Piece.ROOK):
            if board.castling_available[color_to_play][CastleSide.QueenSide]:
                board.castling_available[color_to_play][CastleSide.QueenSide] = m.from_ != 56*color_to_play
            elif board.castling_available[color_to_play][CastleSide.KingSide]:
                board.castling_available[color_to_play][CastleSide.KingSide] = m.from_ != 7+56*color_to_play
            delta_castling_rights = board.castling_available[color_to_play].sum() - self.castling_available[color_to_play].sum()

        if m.castleSide is not None: # No need to take care of the King, since already the from_-to move it
            #TODO: consider captures of the rook, which would also null out the castling  
            if color_to_play == Color.WHITE:
                rook_from = Square(0 if m.castleSide == CastleSide.QueenSide else 7)
                rook_to   = Square(3 if m.castleSide == CastleSide.QueenSide else 5)
                
            else: 
                rook_from = Square(56 if m.castleSide == CastleSide.QueenSide else 63)
                rook_to   = Square(59 if m.castleSide == CastleSide.QueenSide else 61)
                
            # Clear rook initial possition (m.to)
            rook_from_bb_inv = ~ rook_from.toBoard()
            board.pieces[color_to_play][Piece.ROOK] &= rook_from_bb_inv
            board.all_pieces_per_color[color_to_play] &= rook_from_bb_inv
            board.all_pieces &= rook_from_bb_inv
            zobrist_hash_number ^= ZOBRIST_TABLE[("Piece", color_to_play, Piece.ROOK, rook_from.index)]

            # Add rook in King initial possit
            rook_to_bb = rook_to.toBoard()
            board.pieces[color_to_play][Piece.ROOK] |= rook_to_bb
            board.all_pieces_per_color[color_to_play] |=  rook_to_bb
            board.all_pieces |=  rook_to_bb
            zobrist_hash_number ^= ZOBRIST_TABLE[("Piece", color_to_play, Piece.ROOK, rook_to.index)]

        # Update Zobrist hash for castling rights:
        if np.any(self.castling_available != board.castling_available):
            for castling_side in CastleSide:
                if self.castling_available[color_to_play][castling_side] != board.castling_available[color_to_play][castling_side]:
                    zobrist_hash_number ^= ZOBRIST_TABLE[("Castling", color_to_play, castling_side)]

        board.color_to_play = opposite_color
        zobrist_hash_number ^= ZOBRIST_TABLE[("Color", Color.BLACK)]  # To add or remove is the same operation
        board.eval += self.eval + board_evaluation_move_correction(self.color_to_play, \
                                                        self.all_pieces_per_color[self.color_to_play.flip()], \
                                                        self.pieces[self.color_to_play.flip()], \
                                                        m, delta_castling_rights)
        board.hash_value = zobrist_hash_number
        zobrist_hash_number1 = self.zobrist_hash_delta(m, board.en_passant_sqr, board.castling_available, captured_piece_non_en_passant)
        if zobrist_hash_number1 != zobrist_hash_number:
            #TODO: Remove once confident we didn't introduce bugs by moving the zobrist
            print(self.__str__())
            print(m)
            print("In move calculation: ", zobrist_hash_number)
            print("Independent calculation: ", zobrist_hash_number1)
            assert(zobrist_hash_number1 == zobrist_hash_number)

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
            self.hash_value = self.zobrist_hash()

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
                    zobrist_hash_number ^= ZOBRIST_TABLE[("Castling",  color, castling_side)]

        if self.en_passant_sqr:
            zobrist_hash_number ^= ZOBRIST_TABLE[("EnPassant", SQUARE_TO_FILE[self.en_passant_sqr])]

        return zobrist_hash_number

    def zobrist_hash_delta(self, m, new_board_en_passant_sqr, new_board_castling_rights_available, captured_piece_non_en_passant):

        zobrist_hash_number = self.hash_value

        color_to_play = self.color_to_play
        opposite_color = color_to_play.flip()
        bb_to = Square(m.to).toBoard()

        # En Passant Square
        if self.en_passant_sqr is not None:
            # clear en_passant in zobrist hash if initial board had an en-passant
            zobrist_hash_number ^= ZOBRIST_TABLE[("EnPassant", SQUARE_TO_FILE[self.en_passant_sqr])]

        if m.piece == Piece.PAWN and abs(m.from_ - m.to) == 16:
            zobrist_hash_number ^= ZOBRIST_TABLE[("EnPassant", SQUARE_TO_FILE[new_board_en_passant_sqr])]

        # En Passant Capture
        if m.en_passant_capture:
            if color_to_play == Color.WHITE:
                capture_sqr = bb_to >> np.uint(8)  # down from the 'to' sqr
            else:
                capture_sqr = bb_to << np.uint(8)  # up from the 'to' sqr
            zobrist_hash_number ^= ZOBRIST_TABLE[("Piece", opposite_color, Piece.PAWN, right_bit_map(capture_sqr))]

        # Promotion of Pawn
        if m.promotion is not None:
            # clear pawn
            zobrist_hash_number ^= ZOBRIST_TABLE[("Piece", color_to_play, Piece.PAWN, m.to)]

            # add promotion piece
            zobrist_hash_number ^= ZOBRIST_TABLE[("Piece", color_to_play, m.promotion, m.to)]

        # Same color
        zobrist_hash_number ^= ZOBRIST_TABLE[("Piece", color_to_play, m.piece, m.from_)]
        zobrist_hash_number ^= ZOBRIST_TABLE[("Piece", color_to_play, m.piece, m.to)]

        # Capture (Non-En-Passant)
        if captured_piece_non_en_passant is not None:
            zobrist_hash_number ^= ZOBRIST_TABLE[("Piece", opposite_color, captured_piece_non_en_passant, m.to)]

        if m.castleSide is not None:  # No need to take care of the King, since already the from_-to move it
            # TODO: consider captures of the rook, which would also null out the castling (link to the
            if color_to_play == Color.WHITE:
                rook_from = Square(0 if m.castleSide == CastleSide.QueenSide else 7)
                rook_to = Square(3 if m.castleSide == CastleSide.QueenSide else 5)

            else:
                rook_from = Square(56 if m.castleSide == CastleSide.QueenSide else 63)
                rook_to = Square(59 if m.castleSide == CastleSide.QueenSide else 61)

            # Clear rook initial position (m.to)
            zobrist_hash_number ^= ZOBRIST_TABLE[("Piece", color_to_play, Piece.ROOK, rook_from.index)]
            zobrist_hash_number ^= ZOBRIST_TABLE[("Piece", color_to_play, Piece.ROOK, rook_to.index)]

        zobrist_hash_number ^= ZOBRIST_TABLE[("Color", Color.BLACK)]  # To add or remove is the same operation

        # Update zobrist hash for castling rights:
        if np.any(self.castling_available != new_board_castling_rights_available):
            for castling_side in CastleSide:
                if self.castling_available[color_to_play][castling_side] != new_board_castling_rights_available[color_to_play][castling_side]:
                    zobrist_hash_number ^= ZOBRIST_TABLE[("Castling", color_to_play, castling_side)]

        return zobrist_hash_number

    def add_to_transpotition_table(self, move, depth, score):
        global TRANSPOSITION_TABLE
        global NODES_COUNTER
        if (self.hash_value not in TRANSPOSITION_TABLE) or TRANSPOSITION_TABLE[self.hash_value]['depth'] <= depth:
            TRANSPOSITION_TABLE[self.hash_value] = \
                {
                    "depth": depth,
                    "move": move,
                    "score": score
                }





