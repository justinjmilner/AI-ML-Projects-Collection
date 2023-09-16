"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """

    # Counts how many x's and o's on the board
    Xs = 0
    Os = 0

    for i in range(3):
        for j in range(3):
            if board[i][j] == O:
                Os += 1

            elif board[i][j] == X:
                Xs += 1

    # Determine whether it's X or O's turn
    zero_or_one = (Xs + Os) % 2

    if zero_or_one == 0:
        return X

    else:
        return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """

    moves = set()

    # Add each possible action to set of moves
    for i in range(3):
        for j in range(3):
            if board[i][j] == None:
                moves.add((i, j))

    # If no possible moves left, end game
    if len(moves) == 0:
        return None

    else:
        return moves


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """

    # Create a copy of the board to return
    board_copy = copy.deepcopy(board)

    # Check the intended action is valid
    if board[action[0]][action[1]] != None:
        raise Exception('Invalid move')

    else:
        # Add the current players move to the board copy
        board_copy[action[0]][action[1]] = player(board)

    return board_copy


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """

    # Check for 3 in a row horizontally
    for i in range(3):
        horizontal = []

        for j in range(3):
            horizontal.append(board[i][j])

            if horizontal == [X, X, X]:
                return X
            if horizontal == [O, O, O]:
                return O

    # Check for 3 in a row vertically
    n = 0
    k = 0
    passes = 0

    for i in range(3):
        vertical = []

        for j in range(3):
            vertical.append(board[n][k])
            n += 1

            if vertical == [X, X, X]:
                return X

            if vertical == [O, O, O]:
                return O

            if n % 3 == 0:
                n = 0
                k += 1

    # Check for 3 in a row diagonally right
    diagonal_right = []

    for i in range(3):

        for j in range(3):

            if i == j:
                diagonal_right.append(board[i][j])

            if diagonal_right == [X, X, X]:
                return X

            if diagonal_right == [O, O, O]:
                return O

    # Check for 3 in a row diagonally left
    diagonal_left = []

    for i in range(3):

        for j in range(3):

            if i + j == 2:

                diagonal_left.append(board[i][j])

                if diagonal_left == [X, X, X]:
                    return X

                if diagonal_left == [O, O, O]:
                    return O

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """

    # Check if there is a winner or no more possible moves
    if winner(board) != None or actions(board) is None:
        return True

    else:
        return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """

    player = winner(board)

    # Return a utility value for the result of a game
    if player == X:
        return 1

    if player == O:
        return -1

    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """

    # Return if no more possible moves
    if terminal(board):
        return None

    # Determine the current player
    current_player = player(board)

    # Return optimal move for that player
    if current_player == X:
        best_move = maxvalue(board)

    else:
        best_move = minvalue(board)

    return best_move[1]


def maxvalue(board):

    # Once the terminal state has been reached return the utility value
    if terminal(board):
        best_move = [utility(board), None]
        return best_move

    else:
        temp = -math.inf

        # Determine the highest value of all possible minvalue results
        for action in actions(board):
            best_value = temp
            temp2 = minvalue(result(board, action))

            if temp2 == None:
                break

            # Update the highest possible choice from the minvalue function
            temp = max(temp, temp2[0])

            if temp > best_value:
                best_move = [temp, action]

            # If best possible value is reached then return that move
            if temp == 1:
                return best_move

        # Add the best value for that move to the list
        return best_move


def minvalue(board):

    # Once the terminal state has been reached return the utility value
    if terminal(board):
        best_move = [utility(board), None]
        return best_move

    else:
        temp = math.inf

        # Determine the highest value of all possible maxvalue results
        for action in actions(board):
            best_value = temp
            temp2 = maxvalue(result(board, action))

            # Update the lowest possible choice from the maxvalue function
            temp = min(temp, temp2[0])

            if temp < best_value:
                best_move = [temp, action]

            if temp == -1:
                return best_move

        # Add the best value for that move to the list
        return best_move













