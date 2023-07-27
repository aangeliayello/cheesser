import numpy as np
from enum import IntEnum



#
# def negamax(board, depth = 0, debug = False, debug_str = ""):
#     if depth < 1:
#         if debug:
#             print(debug_str, "Score: ", evaluate_board(board), "   ---   Board: \n", board)
#         return evaluate_board(board)
#     factor = - board.color_to_play * 2 + 1
#     lms = get_legal_moves(board)
#
#     scores = [factor*negamax(board.move(m), depth - 1, debug, debug_str[0]*(len(debug_str) +2)) for m in lms]
#     index = np.argmax(scores)
#     score = scores[index]
#     if debug:
#         print(debug_str, " ***! Score: ", score, "   ---   Move: \n", lms[index], "   ---   Board: \n", board.move(lms[index]))
#     return factor*score
#
# def get_best_move(board, depth = 1, debug = False, debug_str = ""):
#     factor = - board.color_to_play * 2 + 1
#     lms = get_legal_moves(board)
#     lbs = []
#     for m in lms:
#         print(debug_str, "Move: ", m)
#         score = factor*negamax(board.move(m), depth - 1, debug, debug_str[0]*(len(debug_str) +2))
#         print(debug_str,'        Score: ', score)
#
#         lbs.append(score)
#     index = np.argmax([m for m in lbs])
#     if debug:
#         print(debug_str, "Score: ", factor*lbs[index], "   ---   Move: ", lms[index])
#
#     return lms[index]



