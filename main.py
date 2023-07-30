import time
from utils import Piece, CastleSide
from moves import Move, get_best_moveAB, get_best_move
from board import Board

def main():
    humanPlaying = True
    b0 = Board()
    b0.base_board()
    print(b0)
    while True:

        print('*************** Cheeser AB ******************')
        ss1 = time.time()
        moveAB = get_best_moveAB(b0, 3, False, "-")
        ee1 = time.time()
        print(b0.color_to_play, moveAB, '  -  Took: ', round(ee1-ss1), 's')
        print(b0.move(moveAB))
        b0 = b0.move(moveAB)

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
    b0 = Board()
    pboard = \
        [['r' 'n' 'b' 'q' 'k' 'b' '_' 'r'],
         ['p' '_' 'p' 'p' '_' 'p' 'p' '_'],
         ['_' 'p' '_' '_' 'p' 'n' '_' 'p'],
         ['_' 'N' '_' '_' '_' '_' 'B' '_'],
         ['_' '_' '_' 'P' '_' '_' '_' '_'],
         ['_' '_' '_' '_' '_' '_' '_' '_'],
         ['P' 'P' 'P' '_' 'P' 'P' 'P' 'P'],
         ['R' '_' '_' 'Q' 'K' 'B' 'N' 'R']]
    from utils import Color
    b0.from_printed_board(pboard, Color.WHITE)
    print(b0)

    print('****** Depts 1 ')
    ss1 = time.time()
    moveAB = get_best_moveAB(b0, 1, False, "-")
    ee1 = time.time()
    print(b0.color_to_play, moveAB, '  -  Took: ', round(ee1 - ss1), 's')
    print(b0.move(moveAB))

    print('****** Depts 2 ')
    ss1 = time.time()
    moveAB = get_best_moveAB(b0, 2, False, "-")
    ee1 = time.time()
    print(b0.color_to_play, moveAB, '  -  Took: ', round(ee1 - ss1), 's')
    print(b0.move(moveAB))

    print('****** Depts 3 ')
    ss1 = time.time()
    moveAB = get_best_moveAB(b0, 3, False, "-")
    ee1 = time.time()
    print(b0.color_to_play, moveAB, '  -  Took: ', round(ee1 - ss1), 's')
    print(b0.move(moveAB))

    print('****** Depts 4 ')
    ss1 = time.time()
    moveAB = get_best_moveAB(b0, 4, False, "-")
    ee1 = time.time()
    print(b0.color_to_play, moveAB, '  -  Took: ', round(ee1 - ss1), 's')
    print(b0.move(moveAB))

    print('****** Depts 5 ')
    ss1 = time.time()
    moveAB = get_best_moveAB(b0, 5, False, "-")
    ee1 = time.time()
    print(b0.color_to_play, moveAB, '  -  Took: ', round(ee1 - ss1), 's')
    print(b0.move(moveAB))

    #main()