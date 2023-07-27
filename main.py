import time
from utils import Piece
from moves import Move, get_best_moveAB
from board import Board

def main():

    b0 = Board()
    b0.base_board()
    print(b0)

    print('*************** Cheeser ******************')
    ss1 = time.time()
    move123 = get_best_moveAB(b0, 4, False, "-")
    ee1 = time.time()
    print(b0.color_to_play)
    print(move123)
    print(b0.move(move123))
    print(ee1-ss1, move123)

    b0 = b0.move(move123)

    print('*************** Human ******************')
    mP = Move(11, 27, Piece.PAWN)
    print(b0.color_to_play)
    print(mP)
    print(b0.move(mP))
    b0 = b0.move(mP)
    
if __name__ == "__main__":
    main()