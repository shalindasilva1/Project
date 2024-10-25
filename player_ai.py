from typing import List, Any, Tuple

def play(board: List[List[int]], choices: List[int], player: int, memory: Any) -> Tuple[int, Any]:
    '''AI Player Function with heuristic evaluation for optimal move selection.'''
    
    opponent = 1 if player == 0 else 0
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
        
        # Check horizontally
        # board = [[],[],[],[],[],[],[]] length can be n (0 to 9)
        # board[0] = [] length can be m (0 to n)
        # board[0][0] = None if empty
        # board[0][] = 0 or 1 if filled
        for row in range(max(len(col) for col in board)):
            for col in range(len(board) - n_target + 1):
                if all(len(board[c]) > row and board[c][row] == player for c in range(col, col + n_target)):
                    return True
        
        # Check vertically
        for col in range(len(board)):
            if len(board[col]) >= n_target:
                for row in range(len(board[col]) - n_target + 1):
                    if all(board[col][row + r] == player for r in range(n_target)):
                        return True
        
        # Diagonal checks (top-left to bottom-right)
        for row in range(max(len(col) for col in board) - n_target + 1):
            for col in range(len(board) - n_target + 1):
                if all(len(board[col + i]) > row + i and board[col + i][row + i] == player for i in range(n_target)):
                    return True

        # Diagonal checks (bottom-left to top-right)
        for row in range(n_target - 1, max(len(col) for col in board)):
            for col in range(len(board) - n_target + 1):
                if all(len(board[col + i]) > row - i and board[col + i][row - i] == player for i in range(n_target)):
                    return True
        
        
        return False

    def evaluate_position(board, col, player):
        '''Heuristic evaluation of a move.'''
        score = 0
        
        # Simulate placing the piece
        board[col].append(player)  # Place the piece

        # Check for vertical, horizontal, and diagonal potentials (simplified heuristic logic)
        
        # Vertical potential
        if len(board[col]) >= n_target - 1 and all(board[col][r] == player for r in range(len(board[col]) - n_target + 1, len(board[col]))):
            score += 10
        
        # Horizontal potential
        for row in range(len(board[col])):
            for c in range(max(0, col - n_target + 1), min(len(board), col + n_target)):
                if c != col and len(board[c]) > row and board[c][row] == player:
                    board[c].append(player)
                    if is_winning(board, player):
                        score += 1
                    board[c].pop()
        
        # Diagonal potential (top-left to bottom-right)
        for row in range(len(board[col])):
            for i in range(-n_target + 1, n_target):
                if 0 <= col + i < len(board) and 0 <= row + i < len(board[col + i]):
                    board[col + i].append(player)
                    if is_winning(board, player):
                        score += 1
                    board[col + i].pop()
        
        # Diagonal potential (bottom-left to top-right)
        for row in range(len(board[col])):
            for i in range(-n_target + 1, n_target):
                if 0 <= col + i < len(board) and 0 <= row - i < len(board[col + i]):
                    board[col + i].append(player)
                    if is_winning(board, player):
                        score += 1
                    board[col + i].pop()

        # Undo the move after evaluation
        board[col].pop()

        return score
    
    # Step 1: Try to win the game (if any move will result in a win)
    for col in choices:
        if check_winning_move(board, col, player):
            return col, memory

    # Step 2: Block opponent's winning move
    for col in choices:
        if check_winning_move(board, col, opponent):
            return col, memory

    # Step 3: Evaluate all valid moves and pick the best one based on the heuristic
    best_score = -float('inf')
    best_move = None
    for col in choices:
        score = evaluate_position(board, col, player)
        if score > best_score:
            best_score = score
            best_move = col

    # Default fallback (in case no best move found)
    return best_move or choices[0], memory