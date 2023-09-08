import time

import classes
from classes import Piece, CastleSide, Move, File, Rank, Square
from moves import get_best_moveAB
from board import Board, Color
from evaluation import board_evaluation_move_correction
import random

def fileRankToSquare(file, rank):
    return Square((rank - Rank.One)*8 + file - File.A)

def get_move(board: Board):
    while True:
        try:
            from_, to = input( "Enter 'from', 'to' coordinates\n").replace(" ", "").upper().split(",")

            from_file = File[from_[0]]
            from_rank = Rank(int(from_[1])-1)
            to_file = File[to[0]]
            to_rank = Rank(int(to[1])-1)

            from_sqr = fileRankToSquare(from_file, from_rank)
            from_bb = from_sqr.toBoard()

            to_sqr = fileRankToSquare(to_file, to_rank)
            to_bb = from_sqr.toBoard()

            # Get Color
            if from_bb & board.all_pieces_per_color[Color.WHITE]:
                color = Color.WHITE
            else:
                color = Color.BLACK

            # Get Piece
            piece = None
            for p in Piece:
                if from_bb & board.pieces[color][p]:
                    piece = p
                    break

            # Get Promotion
            promotion = None
            if (piece == Piece.PAWN):
                # check if promotion required
                if (color == Color.WHITE and to_rank == Rank.Eight) or (color == Color.BLACK and to_rank == Rank.One):
                    promotion_str = input("Enter promotion piece.\n").replace(" ", "").upper()
                    promotion = Piece[promotion_str]

            # Get En-Passant
            en_passant = False
            if (piece == Piece.PAWN and board.en_passant_sqr is not None and (Square(board.en_passant_sqr).toBoard() & to_bb)):
                en_passant = True

            # Get CastleSide
            castleSide = None
            if (piece == Piece.KING and abs( from_file - to_file) == 2):
                if from_file > to_file: # King moved to the left (White bottom of the board)
                    castleSide = CastleSide.QueenSide
                else:
                    castleSide = CastleSide.KingSide

            mP = Move(piece, from_sqr.index, to_sqr.index, promotion, en_passant, castleSide)

            break
        except:
            pass
    return mP

def validate_move(move, board):
    #TODO: validate human move
    return True

def get_human_move(board):
    while True:
        move = get_move(board)
        isLegalMove = validate_move(move, board)

        if not isLegalMove:
            print("Move inputed is not legal, please retry!")
            continue

        print(board.move(move))
        yesNo = input("Is this the board that you expect, [y, n]?\n")

        if yesNo == 'y' or yesNo == 'Y':
            print(board.color_to_play, move)
            print(board.move(move))
            break
        else:
            print("Let's try again!")

    return move