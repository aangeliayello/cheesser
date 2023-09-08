import time
from classes import Piece, CastleSide, Move
from moves import get_best_moveAB, get_pseudo_legal_moves, get_legal_moves
from board import Board, Color
from human import get_human_move
from evaluation import board_evaluation_move_correction
import random
from board import TRANSPOSITION_TABLE
import numpy as np

def main():
    humanPlaying = True
    b0 = Board()
    #b0.base_board()
    pboard = [['_' '_' '_' '_' '_' 'r' 'k' '_'],
 ['_' '_' '_' '_' '_' 'p' 'p' 'p'],
 ['_' 'p' 'p' 'p' '_' '_' '_' '_'],
 ['_' '_' '_' '_' '_' '_' '_' '_'],
 ['_' 'P' '_' '_' 'P' '_' '_' '_'],
 ['_' '_' '_' '_' '_' '_' '_' '_'],
 ['K' '_' 'q' '_' '_' '_' 'P' 'P'],
 ['_' '_' '_' 'R' '_' '_' '_' '_']]
    b0.from_printed_board(pboard, Color.WHITE)
    b0.castling_available[:][:] = False
    print(b0)

    while True:

        print('*************** Cheeser AB ******************')
        ss1 = time.time()
        moveAB,score = get_best_moveAB(b0, 0)
        ee1 = time.time()
        print(b0.color_to_play, moveAB, '  -  Took: ', round(ee1-ss1), 's')
        print(b0.move(moveAB, score))
        b0 = b0.move(moveAB, score)

        if humanPlaying:
            print('*************** Human ******************')
            print('To play: ', b0.color_to_play.name)
            human_move = get_human_move(b0)
            b0 = b0.move(human_move)

def timed_main():
    b0 = Board()
    b0.base_board()
    b0.keep_board_history = True
    print(b0)
    ss0 = time.time()
    for i in range(10):

        print('*************** Cheeser AB ******************')
        ss1 = time.time()
        moveAB, score = get_best_moveAB(b0, 4)
        ee1 = time.time()
        print(b0.color_to_play, moveAB, '  -  Took: ', round(ee1 - ss1), 's')
        print(b0.move(moveAB, score))
        b0 = b0.move(moveAB, score)
        print(b0.board_history)
    ee0 = time.time()
    print('Total Took: ', round(ee0 - ss0), 's')

if __name__ == "__main__":
    main()
    #
    # # from hashing import ZOBRIST_TABLE
    # # b0 = Board()
    # # b0.base_board()
    # # b0.keep_board_history = True
    # # print(b0)
    # # ss0 = time.time()
    # # moveAB, score = get_best_moveAB(b0, 3)
    # # move = Move(Piece.KNIGHT,1,18)
    # # bm = b0.move(move)
    # #
    # # zobrist_number = bm.hash_value ^ b0.hash_value
    # # a = 0b1100110101010111110010011011111000001010101110100001110000110000 #rook
    # # b = 0b110011110101110000110001110100010101110001100111110101000111101 #king
    # # c = a ^ b
    # #
    # # for key in ZOBRIST_TABLE.keys():
    # #     h = ZOBRIST_TABLE[key]
    # #     if h == a or h == b or h == c:
    # #         print('key', key, 'val', h)
    # #
    #
    # # pboard = [['r' '_' 'b' 'q' 'k' 'b' 'n' 'r'],
    # #          ['p' 'p' 'p' 'p' 'p' 'p' 'p' 'p'],
    # #          ['n' '_' '_' '_' '_' '_' '_' '_'],
    # #          ['_' '_' '_' '_' '_' '_' '_' '_'],
    # #          ['_' '_' '_' '_' '_' '_' '_' '_'],
    # #          ['N' '_' '_' '_' '_' '_' '_' '_'],
    # #          ['P' 'P' 'P' 'P' 'P' 'P' 'P' 'P'],
    # #          ['R' '_' '_' '_' 'K' 'B' 'N' 'R']]
    # #
    # # board = Board()
    # # board.from_printed_board(pboard, Color.WHITE)
    # # board.hash_value = board.zobrist_hash()
    # # move = Move(Piece.ROOK, 0,1)
    # # bm = board.move(move)
    #
    # b0 = Board()
    # b0.base_board()
    # b0.keep_board_history = True
    # # print(b0)
    # # ss0 = time.time()
    # # for i in range(10):
    # #     print('*************** Cheeser AB ******************')
    # #     ss1 = time.time()
    # #     moveAB, score = get_best_moveAB(b0, 4)
    # #     ee1 = time.time()
    # #     print(b0.color_to_play, moveAB, '  -  Took: ', round(ee1 - ss1,2), 's')
    # #     TRANSPOSITION_TABLE.clear()
    # #     b0 = Board()
    # #     b0.base_board()
    # #     b0.keep_board_history = True
    # # ee0 = time.time()
    # # print('Total Took: ', round(ee0 - ss0), 's')
    # #
    #
    # boards = []
    # lms = get_legal_moves(b0)
    #
    # def get_boards(board, depth = 0):
    #     if depth == 0:
    #         return [board]
    #     boards = []
    #     legal_moves = get_legal_moves(board)
    #     for move in legal_moves:
    #         boards += get_boards(board.move(move), depth - 1)
    #
    #     return boards
    #
    # ss1 = time.time()
    # moveAB, score = get_best_moveAB(b0, 4)
    # ee1 = time.time()
    # print(b0.color_to_play, moveAB, '  -  Took: ', round(ee1 - ss1, 2), 's')
    #
    #
    # boards = get_boards(b0,4)
    # print(len(boards))
    #
    # # print(len(set([b.__str__() for b in boards])))
    # # print(boards[-1])