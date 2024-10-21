#====================================================================================================#
# Imports:                                                                                           #
#====================================================================================================#
from typing import Any, List, Tuple

#====================================================================================================#
# Play Function:                                                                                     #
#====================================================================================================#
def play(board: List[List[int]], choices: List[int], player: int, memory: Any) -> Tuple[int, Any]:
    '''AI Player Function with heuristic evaluation for optimal move selection.'''
    
    if player == 1:
        opponent = 2
    else:
        opponent = 1

    def check_winning_move(board, col, player):
        '''check for a wining move.'''
        temp_board = [col[:] for col in board] # create a deep copy of the board to run checks.
        temp_board[col].append(player)
        return is_winning(temp_board, player)

    def is_winning(board, player):
        '''Check if the player has won after placing a piece.'''
        n_cols = n_target = n_rows = len(board)
        # Check horizontally
        for row in range(n_rows):
            for col in range(n_cols - n_target + 1):
                if all(len(board[c]) > row and board[c][row] == player for c in range(col, col + n_target)):
                    return True
        
        # Check vertically
        for col in range(n_cols):
            if len(board[col]) >= n_target and all(board[col][r] == player for r in range(len(board[col]) - n_target, len(board[col]))):
                return True
        
        return False

    def evaluate_position(board, col, player):
        '''Heuristic evaluation of a move.'''
        score = 0
        
        # Simulate placing the piece
        temp_board = [c[:] for c in board]
        temp_board[col].append(player)

        # Check for potential lines horizontally and vertically
        for row in range(len(temp_board[col])):
            # Vertical potential
            if len(temp_board[col]) >= 3 and all(temp_board[col][r] == player for r in range(max(0, row-2), row+1)):
                score += 10  # Add points if there are 3 aligned pieces vertically

        # Check horizontally across rows
        for r in range(len(board)):
            in_row = 0
            for c in range(len(board)):
                if len(temp_board[c]) > r and temp_board[c][r] == player:
                    in_row += 1
                    if in_row == 2:
                        score += 5  # Add points for 2 aligned pieces horizontally
                    if in_row == 3:
                        score += 10  # Add more for 3 aligned
                else:
                    in_row = 0  # Reset if interrupted

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

    return best_move, memory