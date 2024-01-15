"""
Tic Tac Toe Player
"""

import math, copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY], [EMPTY, EMPTY, EMPTY], [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    x_counter = 0
    o_counter = 0
    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j] == X:
                x_counter += 1
            elif board[i][j] == O:
                o_counter += 1
    if x_counter > o_counter:
        return O
    else:
        return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible_actions = set()
    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j] == EMPTY:
                possible_actions.add((i, j))
    return possible_actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    new_board = copy.deepcopy(board)
    new_board[action[0]][action[1]] = player(board)
    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # Test rows
    for i in range(len(board)):
        x_cnt = 0
        o_cnt = 0
        for j in range(len(board)):
            if board[i][j] == X:
                x_cnt += 1
            elif board[i][j] == O:
                o_cnt += 1
        if x_cnt == 3:
            return X
        elif o_cnt == 3:
            return O

    # Test columns
    for j in range(len(board)):
        x_cnt = 0
        o_cnt = 0
        for i in range(len(board)):
            if board[i][j] == X:
                x_cnt += 1
            elif board[i][j] == O:
                o_cnt += 1
        if x_cnt == 3:
            return X
        elif o_cnt == 3:
            return O

    # Test diagonals
    x_cnt_1 = 0
    o_cnt_1 = 0
    x_cnt_2 = 0
    o_cnt_2 = 0
    for i in range(len(board)):
        if board[i][i] == X:
            x_cnt_1 += 1
        elif board[i][i] == O:
            o_cnt_1 += 1

        if board[i][len(board) - 1 - i] == X:
            x_cnt_2 += 1
        elif board[i][len(board) - 1 - i] == O:
            o_cnt_2 += 1

    if x_cnt_1 == 3 or x_cnt_2 == 3:
        return X
    elif o_cnt_1 == 3 or o_cnt_2 == 3:
        return O

    # No winner found
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    empty_cnt = 0
    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j] == EMPTY:
                empty_cnt += 1

    if winner(board) is not None or empty_cnt == 0:
        return True
    else:
        return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return utility(board), None

    # Initial conditions
    alpha = -math.inf
    beta = math.inf
    depth = 0

    def maximize(board, alpha, beta, depth):
        if terminal(board):
            return utility(board), None
        v = -math.inf
        move = None
        for action in actions(board):
            value, _ = minimize(result(board, action), alpha, beta, depth + 1)
            if value > v:
                v, move = value, action
            alpha = max(alpha, v)
            if alpha >= beta:
                break
        return v, move

    def minimize(board, alpha, beta, depth):
        if terminal(board):
            return utility(board), None
        v = math.inf
        move = None
        for action in actions(board):
            value, _ = maximize(result(board, action), alpha, beta, depth + 1)
            if value < v:
                v, move = value, action
            beta = min(beta, v)
            if beta <= alpha:
                break
        return v, move

    if player(board) == X:
        _, move = maximize(board, alpha, beta, depth)
    else:
        _, move = minimize(board, alpha, beta, depth)
    return move
