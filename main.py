import time
from classes import Piece, CastleSide, Move
from moves import get_best_moveAB, get_best_move, get_random_move
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
        moveAB,score = get_best_moveAB(b0, 4, False, "-")
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

if __name__ == "__main__":
    #main()
    b0 = Board()
    b0.base_board()


    print(b0)
    ss0 = time.time()
    for _ in range(10):
        print('*************** Cheeser AB ******************')
        ss1 = time.time()
        moveAB,score = get_best_moveAB(b0, 3)
        ee1 = time.time()
        print(b0.color_to_play, moveAB, '  -  Took: ', round(ee1-ss1), 's')
        print(b0.move(moveAB, score))
        b0 = b0.move(moveAB, score)
    ee0 = time.time()
    print( ' Took: ', round(ee0-ss0,2), 's')