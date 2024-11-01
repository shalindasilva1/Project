from typing import List, Any, Tuple
import random

def play(board: List[List[int]], choices: List[int], player: int, memory: Any) -> Tuple[int, Any]:
    '''Tic-Tac bot that tries to block oponent to the best and guess the best column.'''
    
    opponent = 1 if player == 0 else 0
    n_target = memory.get('n_target', 3) if memory else 3  # reading memory or init n_target.

    def check_winning_move(board, col, player):
        '''Check for possible wining moves on the board.'''
        board[col].append(player)  # select col for each plaer.
        result = is_winning(board, player)
        board[col].pop()  # remove the move.
        return result

    def is_winning(board, player):
        '''Check horizontally, vertically, diagonally for winnig mmoves.'''
        n_target = memory.get('n_target', 3) if memory else 3  # Start with 3 or use from memory

        # horizontal
        for row in range(max(len(col) for col in board)):
            for col in range(len(board) - n_target + 1):
                if all(len(board[c]) > row and board[c][row] == player for c in range(col, col + n_target)):
                    return True

        # vertical
        for col in range(len(board)):
            if len(board[col]) >= n_target:
                for row in range(len(board[col]) - n_target + 1):
                    if all(board[col][row + r] == player for r in range(n_target)):
                        return True

        # top-left -> bottom-right
        for row in range(max(len(col) for col in board) - n_target + 1):
            for col in range(len(board) - n_target + 1):
                if all(len(board[col + i]) > row + i and board[col + i][row + i] == player for i in range(n_target)):
                    return True

        # bottom-left -> top-right
        for row in range(n_target - 1, max(len(col) for col in board)):
            for col in range(len(board) - n_target + 1):
                if all(len(board[col + i]) > row - i and board[col + i][row - i] == player for i in range(n_target)):
                    return True

        return False

    def heuristic_score(board, col, player):
        '''
            applying heuristic score to the board to find the best move.
            https://medium.com/@ma274/tic-tac-toe-game-using-heuristic-alpha-beta-tree-search-algorithm-26b13273bc5b
        '''
        score = 0
        board[col].append(player)

        # horizontal
        for row in range(max(len(col) for col in board)):
            for c in range(len(board) - n_target + 1):
                if all(len(board[c + i]) > row and board[c + i][row] == player for i in range(n_target)):
                    score += 1

        # vertical
        for c in range(len(board)):
            if len(board[c]) >= n_target:
                for row in range(len(board[c]) - n_target + 1):
                    if all(board[c][row + r] == player for r in range(n_target)):
                        score += 1

        # top-left -> bottom-right
        for row in range(max(len(col) for col in board) - n_target + 1):
            for c in range(len(board) - n_target + 1):
                if all(len(board[c + i]) > row + i and board[c + i][row + i] == player for i in range(n_target)):
                    score += 1

        # bottom-left -> top-right
        for row in range(n_target - 1, max(len(col) for col in board)):
            for c in range(len(board) - n_target + 1):
                if all(len(board[c + i]) > row - i and board[c + i][row - i] == player for i in range(n_target)):
                    score += 1

        board[col].pop()
        return score

    # 1. Check win move avilability.
    for col in choices:
        if check_winning_move(board, col, player):
            return col, memory

    # 2. Opponent win move handle.
    for col in choices:
        if check_winning_move(board, col, opponent):
            return col, memory

    # 3. heuristic_score to guess.
    best_score = -1
    best_col = random.choice(choices)
    for col in choices:
        score = heuristic_score(board, col, player)
        if score > best_score:
            best_score = score
            best_col = col

    return best_col, memory