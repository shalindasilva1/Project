from typing import List, Any, Tuple
import random

def play(board: List[List[int]], choices: List[int], player: int, memory: Any) -> Tuple[int, Any]:
    '''AI player using minimax algorithm with alpha-beta pruning.'''
    
    opponent = 1 if player == 0 else 0
    if memory is None:
        memory = {'n_target': 3}
    n_target = memory['n_target']
    # log n_target to a text file
    with open('n_target.txt', 'a') as f:
        f.write(str(n_target) + '\n')

    def check_winning_move(board, col, player):
        '''Check for possible winning moves on the board.'''
        board[col].append(player)  # select col for each player.
        result = is_winning(board, player)
        board[col].pop()  # remove the move.
        return result

    def is_winning(board, player):
        '''Check horizontally, vertically, diagonally for winning moves.'''
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

    def minimax(board, depth, alpha, beta, maximizing_player):
        '''Minimax algorithm with alpha-beta pruning.'''
        if depth == 0 or is_winning(board, player) or is_winning(board, opponent):
            return heuristic_score(board, player) - heuristic_score(board, opponent)

        if maximizing_player:
            max_eval = float('-inf')
            for col in choices:
                board[col].append(player)
                eval = minimax(board, depth - 1, alpha, beta, False)
                board[col].pop()
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float('inf')
            for col in choices:
                board[col].append(opponent)
                eval = minimax(board, depth - 1, alpha, beta, True)
                board[col].pop()
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval

    def heuristic_score(board, player):
        '''Heuristic score to evaluate the board state.'''
        score = 0

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

        return score

    def adjust_n_target(board, n_target):
        '''Adjust n_target based on the current game state.'''
        max_consecutive = 0

        # Check horizontally
        for row in range(max(len(col) for col in board)):
            for col in range(len(board)):
                consecutive = 0
                for c in range(col, len(board)):
                    if len(board[c]) > row and board[c][row] == player:
                        consecutive += 1
                    else:
                        break
                max_consecutive = max(max_consecutive, consecutive)

        # Check vertically
        for col in range(len(board)):
            consecutive = 0
            for row in range(len(board[col])):
                if board[col][row] == player:
                    consecutive += 1
                else:
                    break
            max_consecutive = max(max_consecutive, consecutive)

        # Check top-left -> bottom-right
        for row in range(max(len(col) for col in board)):
            for col in range(len(board)):
                consecutive = 0
                for i in range(min(len(board) - col, max(len(col) for col in board) - row)):
                    if len(board[col + i]) > row + i and board[col + i][row + i] == player:
                        consecutive += 1
                    else:
                        break
                max_consecutive = max(max_consecutive, consecutive)

        # Check bottom-left -> top-right
        for row in range(max(len(col) for col in board)):
            for col in range(len(board)):
                consecutive = 0
                for i in range(min(len(board) - col, row + 1)):
                    if len(board[col + i]) > row - i and board[col + i][row - i] == player:
                        consecutive += 1
                    else:
                        break
                max_consecutive = max(max_consecutive, consecutive)

        # Adjust n_target based on the maximum consecutive marks found
        if max_consecutive >= n_target:
            n_target += 1
        elif max_consecutive < n_target - 1:
            n_target = max(3, max_consecutive + 1)  # Ensure n_target is at least 3
        return n_target

    # Adjust n_target before making a move
    n_target = adjust_n_target(board, n_target)
    memory['n_target'] = n_target

    # 1. Check win move availability.
    for col in choices:
        if check_winning_move(board, col, player):
            return col, memory

    # 2. Opponent win move handle.
    for col in choices:
        if check_winning_move(board, col, opponent):
            return col, memory

    # 3. Use minimax to guess the best move.
    best_score = float('-inf')
    best_col = random.choice(choices)
    for col in choices:
        board[col].append(player)
        score = minimax(board, 3, float('-inf'), float('inf'), False)
        board[col].pop()
        if score > best_score:
            best_score = score
            best_col = col

    # Check if there are n_target consecutive marks in any direction
    board[best_col].append(player)
    if is_winning(tuple(map(tuple, board)), player):
        memory['n_target'] += 1
    board[best_col].pop()

    return best_col, memory
