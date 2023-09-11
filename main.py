import time
from classes import Piece, CastleSide, Move
from moves import get_best_moveAB, get_pseudo_legal_moves, get_legal_moves, game_status
from board import Board, Color
from human import get_human_move
from evaluation import board_evaluation_move_correction
import random
from board import TRANSPOSITION_TABLE
import numpy as np

def main():
    humanPlaying = True
    humanColor = Color.WHITE
    b0 = Board()
    b0.base_board()
    print(b0)

    if humanPlaying and humanColor == Color.WHITE:
        print('*************** Human ******************')
        game_status(b0)
        print('To play: ', b0.color_to_play.name)
        human_move = get_human_move(b0)
        b0 = b0.move(human_move)

    while True:

        print('*************** Cheeser AB ******************')
        game_status(b0)
        ss1 = time.time()
        moveAB,score = get_best_moveAB(b0, 0)
        ee1 = time.time()
        print(b0.color_to_play, moveAB, '  -  Took: ', round(ee1-ss1), 's')
        print(b0.move(moveAB, score))
        b0 = b0.move(moveAB, score)

        if humanPlaying:
            print('*************** Human ******************')
            game_status(b0)
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
    #main()

    humanPlaying = False
    humanColor = Color.BLACK
    b0 = Board()
    pboard =[['r' '_' 'b' 'q' 'k' '_' 'n' 'r'],
             ['p' 'p' 'p' 'p' '_' '_' '_' 'p'],
             ['_' '_' '_' 'N' '_' '_' 'p' '_'],
             ['_' '_' 'n' 'P' '_' '_' '_' '_'],
             ['_' '_' '_' 'R' 'p' '_' '_' '_'],
             ['P' '_' '_' '_' 'B' '_' '_' '_'],
             ['_' 'P' 'P' '_' '_' 'P' 'P' 'P'],
             ['_' '_' 'K' '_' '_' 'B' 'N' 'R']]
    b0.from_printed_board(pboard=pboard, color_to_play=Color.WHITE)
    #b0.base_board()
    print(b0)

    if humanPlaying and humanColor == Color.WHITE:
        print('*************** Human ******************')
        game_status(b0)
        print('To play: ', b0.colorF_to_play.name)
        human_move = get_human_move(b0)
        b0 = b0.move(human_move)

    for i in range(4):

        print('*************** Cheeser AB ******************')
        game_status(b0)
        ss1 = time.time()
        moveAB, score = get_best_moveAB(b0, 3)
        ee1 = time.time()
        print(b0.color_to_play, moveAB, '  -  Took: ', round(ee1 - ss1), 's')
        print(b0.move(moveAB, score))
        b0 = b0.move(moveAB, score)

        if humanPlaying:
            print('*************** Human ******************')
            game_status(b0)
            print('To play: ', b0.color_to_play.name)
            human_move = get_human_move(b0)
            b0 = b0.move(human_move)