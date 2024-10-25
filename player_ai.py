from typing import List, Any, Tuple

def play(board: List[List[int]], choices: List[int], player: int, memory: Any) -> Tuple[int, Any]:
    '''AI Player Function with heuristic evaluation for optimal move selection.'''
    
    opponent = 2 if player == 1 else 1
    n_target = memory.get('n_target', 3) if memory else 3  # Start with 3 or use from memory

    def check_winning_move(board, col, player):
        '''Simulate placing the piece and check if it's a winning move.'''
        board[col].append(player)  # Place the piece
        result = is_winning(board, player)  # Check if the move leads to a win
        board[col].pop()  # Undo the move
        return result

    def is_winning(board, player):
        '''Check if the player has won after placing a piece.'''
        n_rows = max(len(col) for col in board)
        n_cols = len(board)
        n_target = memory.get('n_target', 3) if memory else 3  # Start with 3 or use from memory

        # Check horizontally
        for row in range(n_rows):
            for col in range(n_cols - n_target + 1):
                if all(len(board[col + i]) > row and board[col + i][row] == player for i in range(n_target)):
                    return True

        # Check vertically
        for col in range(n_cols):
            for row in range(n_rows - n_target + 1):
                if all(len(board[col]) > row + i and board[col][row + i] == player for i in range(n_target)):
                    return True

        # Diagonal checks (top-left to bottom-right and bottom-left to top-right)
        for row in range(n_rows):
            for col in range(n_cols):
                # Top-left to bottom-right
                if col + n_target <= n_cols and row + n_target <= n_rows:
                    if all(len(board[col + i]) > row + i and board[col + i][row + i] == player for i in range(n_target)):
                        return True
                # Bottom-left to top-right
                if col + n_target <= n_cols and row - n_target + 1 >= 0:
                    if all(len(board[col + i]) > row - i and board[col + i][row - i] == player for i in range(n_target)):
                        return True

        return False

    def evaluate_position(board, col, player):
        '''Heuristic evaluation of a move.'''
        score = 0
        opponent = 2 if player == 1 else 1

        # Place the piece temporarily
        board[col].append(player)

        # Check for potential winning move
        if is_winning(board, player):
            score += 100

        # Check for potential opponent winning move
        board[col][-1] = opponent
        if is_winning(board, opponent):
            score -= 100
        board[col][-1] = player

        # Prioritize center column (for 3x3 board)
        center_col = len(board) // 2
        if col == center_col:
            score += 10

        # Prioritize corner columns (for 3x3 board)
        if col in [0, len(board) - 1]:
            score += 5

        # Undo the move
        board[col].pop()

        return score

    # Step 1: Block opponent's winning move
    for col in choices:
        if check_winning_move(board, col, opponent):
            return col, {'n_target': n_target}

    # Step 2: Try to win the game (if any move will result in a win)
    for col in choices:
        if check_winning_move(board, col, player):
            return col, {'n_target': n_target}

    # Step 3: Evaluate all valid moves and pick the best one based on the heuristic
    best_score = -float('inf')
    best_move = None
    for col in choices:
        score = evaluate_position(board, col, player)
        if score > best_score:
            best_score = score
            best_move = col

    # Check if any player has `n_target` consecutive marks and increase `n_target` if so
    if is_winning(board, player) or is_winning(board, opponent):
        n_target = min(n_target + 1, 9)

    # Default fallback (in case no best move found)
    return best_move or choices[0], {'n_target': n_target}