import unittest
from board import Board
from moves import get_best_moveAB

class GameProgressionTests(unittest.TestCase):
    def test_upper(self):
        b0 = Board()
        b0.base_board()
        for _ in range(10):
            moveAB, score = get_best_moveAB(b0, 3, debug_str = " ")
            b0 = b0.move(moveAB, score)
        expected_result = "[WHITE_KNIGHT_1_18_(10.0)][BLACK_KNIGHT_62_45_(7.0)][WHITE_KNIGHT_18_33_(985.0)][BLACK_KNIGHT_45_28_(985.0)][WHITE_PAWN_11_19_(998.0)][BLACK_KNIGHT_28_34_(10.0)][WHITE_BISHOP_2_20_(1001.25)][BLACK_PAWN_52_36_(257.25)][WHITE_KNIGHT_6_21_(1016.25)][BLACK_QUEEN_59_45_(263.25)]"
        self.assertEqual( b0.board_history, expected_result)

    def test_isupper(self):
        b0 = Board()
        b0.base_board()
        for _ in range(20):
            moveAB, score = get_best_moveAB(b0, 2, debug_str = " ")
            b0 = b0.move(moveAB, score)
        expected_result = """[WHITE_PAWN_11_27][BLACK_PAWN_51_35_(-9.0)][WHITE_QUEEN_3_19][BLACK_PAWN_55_39_(-45.0)][WHITE_BISHOP_2_20_(3.25)][BLACK_QUEEN_59_43_(-39.25)][WHITE_PAWN_15_31_(-32.75)][BLACK_BISHOP_58_44_(-36.0)][WHITE_KNIGHT_1_18_(-33.0)][BLACK_KNIGHT_57_42_(-1017.0)][WHITE_KNIGHT_6_21_(-1014.0)][BLACK_KNIGHT_62_45_(-1017.0)][WHITE_PAWN_8_16_(-1017.0)][BLACK_PAWN_48_32_(-1017.0)][WHITE_PAWN_9_17_(-1017.0)][BLACK_PAWN_32_24_(-1017.0)][WHITE_PAWN_17_24_(-17.0)][BLACK_PAWN_49_33_(-2017.0)][WHITE_PAWN_24_33_(983.0)][BLACK_KNIGHT_42_32_(-3020.0)]"""
        self.assertEqual( b0.board_history, expected_result)


if __name__ == '__main__':
    unittest.main()