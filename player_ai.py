from typing import List, Any, Tuple

# Memory structure to track moves and state
__memory__ = {
    'count': 0,
    'last_board': None,
    'opponent_last_moves': [],  # Track opponent's last moves
}

def find_opponent_first_move(board: List[List[int]], player: int) -> Tuple[int, int]:
    opponent = 1 - player  # The opponent's symbol is the opposite of the player's symbol
    
    # Search for the first occurrence of the opponent's symbol
    for col in range(len(board)):
        for row in range(len(board[col])):
            if board[col][row] == opponent:
                return (col, row)  # Return the first opponent's move (column, row)
    
    return None  # No opponent move found yet (the player started)

def update_board(board: List[List[int]], move: int, player: int) -> None:
    board[move].append(player)

def find_opponent_last_move(last_board: List[List[int]], current_board: List[List[int]]) -> Tuple[int, int]:
    # Iterate through columns to detect where the board has changed
    for col in range(len(current_board)):
        if len(last_board[col]) != len(current_board[col]):
            # Find the first row where a new symbol (opponent's) has been added
            for row in range(len(current_board[col])):
                if len(last_board[col]) <= row or last_board[col][row] != current_board[col][row]:
                    return (col, row)  # Return the column and row of the opponent's move
    
    return None  # No change detected if there's no move


def play(board: List[List[int]], choices: List[int], player: int, memory: Any) -> Tuple[int, Any]:
    '''AI Player Function with heuristic evaluation for optimal move selection.'''
    try:
        opponent = 1 - player  # The opponent's symbol is the opposite of the player's symbol
        optimal_choice = 1  # Placeholder for the AI's selected move
        __memory__['count'] += 1  # Increment turn counter
        
        # If no previous board is recorded, it's the first turn
        if __memory__['last_board'] is None:
            # Detect if the opponent has already made a move
            opponent_first_move = find_opponent_first_move(board, player)
            
            if opponent_first_move:
                print(f"Opponent's first move was at: Column {opponent_first_move[0]}, Row {opponent_first_move[1]}")
                # Store the opponent's first move in memory
                __memory__['opponent_last_moves'].append(opponent_first_move)
            
            # Update the last_board to the current state for future comparisons
            __memory__['last_board'] = board
        else:
            last_board = __memory__['last_board']  # Retrieve the previous board state
            
            # Find the opponent's last move by comparing the last and current board
            opponent_last_move = find_opponent_last_move(last_board, board)
            
            if opponent_last_move:
                print(f"Opponent's last move was at: Column {opponent_last_move[0]}, Row {opponent_last_move[1]}")
                # Store the opponent's last move in memory
                __memory__['opponent_last_moves'].append(opponent_last_move)
    
        update_board(board, optimal_choice, player)
    finally:
        # Update memory with the current board state
        __memory__['last_board'] = board
        memory = __memory__
    
    return optimal_choice, memory