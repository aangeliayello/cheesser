import time
from classes import Piece, CastleSide, Move
from moves import get_best_moveAB, get_best_move, get_random_move, get_best_moveAB_parallel
from board import Board, Color
from evaluation import board_evaluation_move_correction
import random

import numpy as np
from board import Board
from classes import Color
from moves import get_best_moveAB

def main():
    humanPlaying = False
    b0 = Board()
    b0.base_board()
    print(b0)

    while True:
        
        print('*************** Cheeser AB ******************')
        ss1 = time.time()
        moveAB,score = get_best_moveAB(b0, 4)
        ee1 = time.time()
        print(b0.color_to_play, moveAB, '  -  Took: ', round(ee1-ss1), 's')
        print(b0.move(moveAB, score))
        b0 = b0.move(moveAB, score)
        
        if humanPlaying:
            print('*************** Human ******************')
            print('To play: ', b0.color_to_play.name)
            while True:
                while True:
                    try:
                        piece, from_, to, promotion, en_passant, castleSide = input("Enter from_, to, promotion, en_passant, castleSide\n").split(",")
                        break
                    except:
                        pass
                from_ = int(from_.replace(" ",""))
                to = int(to.replace(" ",""))
                piece = Piece[piece.replace(" ","").upper()]
                promotion = Piece[promotion.replace(" ","").upper()] if promotion else None
                en_passant = bool(en_passant.replace(" ","")) if en_passant else False
                castleSide = CastleSide[castleSide.replace(" ","")] if castleSide else None
                print(from_, to, promotion, en_passant, castleSide)

                mP = Move(piece, from_, to, promotion, en_passant, castleSide)

                print(b0.color_to_play, mP)
                print(b0.move(mP))

                yesNo = input("Is this the board that you expect, [y, n]?\n")
                if yesNo == 'y' or yesNo == 'Y':
                    b0 = b0.move(mP)
                    break
                else:
                    print("Let's try again!")

if __name__ == "__main__":
    #main()v
    random.seed(3)
    b0 = Board()
    b0.base_board()
    print(b0)
    ss0 = time.time()
    for i in range(1000):        
        print(i, '*************** Cheeser AB ******************')
        ss1 = time.time()
        moveAB, score = get_best_moveAB(b0, 4)
        ee1 = time.time()
        print(b0.color_to_play, moveAB, '  -  Took: ', round(ee1-ss1), 's   - ', round(score,2))
        print(b0.move(moveAB, score))
        b0 = b0.move(moveAB, score)
        
        # print(i, '*************** Radom  ******************')
        # ss1 = time.time()
        # moveAB = get_random_move(b0)
        # ee1 = time.time()
        # print(b0.color_to_play, moveAB, '  -  Took: ', round(ee1-ss1), 's   - ', round(score,2))
        # print(b0.move(moveAB, score))
        # b0 = b0.move(moveAB, score)
        
        
    ee0 = time.time()
    print(' Took: ', round(ee0-ss0), 's')