import time
from utils import Piece, CastleSide
from moves import Move, get_best_moveAB, get_best_move, get_random_move
from board import Board
import random

def main():
    humanPlaying = False
    b0 = Board()
    b0.base_board()
    print(b0)
    while True:
        print('*************** Cheeser AB ******************')
        ss1 = time.time()
        moveAB,score = get_best_moveAB(b0, 3, False, "-")
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
                promotion = Piece[promotion.replace(" ","").upper()] if promotion else promotion
                en_passant = bool(en_passant.replace(" ","")) if en_passant else en_passant
                castleSide = CastleSide[castleSide.replace(" ","")] if castleSide else castleSide
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

if __name__ == "__main__" and True:
    #main()
    b0 = Board()
    b0.base_board()
    print(b0)
    for _ in range(1):
        print('*************** Cheeser AB ******************')
        ss1 = time.time()
        moveAB,score = get_best_moveAB(b0, 4, False, "-")
        ee1 = time.time()
        print(b0.color_to_play, moveAB, '  -  Took: ', round(ee1-ss1), 's')
        print(b0.move(moveAB, score))
        b0 = b0.move(moveAB, score)
    print(b0.board_history)
    random.seed(10)
    # for foo in range(3):
    #     b0 = Board()
    #     b0.base_board()
    #     index = 0
    #     cycles = 0
    #     cycles = 0
    #     sinceCycle = 0
    #     ss0 = time.time()
    #
    #     while True:
    #         ss1 = time.time()
    #         moveAB = get_random_move(b0, 1, False, "-")
    #         if moveAB is None or sinceCycle > 50:
    #             cycles += 1
    #             sinceCycle = 1
    #             b0 = Board()
    #             b0.base_board()
    #             moveAB = get_random_move(b0, 1, False, "-")
    #
    #         ee1 = time.time()
    #         b0 = b0.move(moveAB)
    #         index += 1
    #         sinceCycle += 1
    #         if index == 50000:
    #             break
    #     ee0 = time.time()
    #     print('Took: ', round(ee0 - ss0, 2), 's')