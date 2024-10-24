from typing import List, Any, Tuple

__memory__ = {
    'count': 0,
    'last_board': None,
    'opponent_last_moves': [],
}

def find_opponent_first_move(board: List[List[int]], player: int) -> Tuple[int, int]:
    opponent = 1 - player
    
    for col in range(len(board)):
        for row in range(len(board[col])):
            if board[col][row] == opponent:
                return (col, row)
    
    return None

def update_board(board: List[List[int]], move: int, player: int) -> None:
    board[move].append(player)

def find_opponent_last_move(last_board: List[List[int]], current_board: List[List[int]]) -> Tuple[int, int]:
    for col in range(len(current_board)):
        if len(last_board[col]) != len(current_board[col]):
            for row in range(len(current_board[col])):
                if len(last_board[col]) <= row or last_board[col][row] != current_board[col][row]:
                    return (col, row)
    
    return None


def play(board: List[List[int]], choices: List[int], player: int, memory: Any) -> Tuple[int, Any]:
    '''AI Player Function with heuristic evaluation for optimal move selection.'''
    try:
        opponent = 1 - player
        optimal_choice = 1
        __memory__['count'] += 1
        
        if __memory__['last_board'] is None:
            opponent_first_move = find_opponent_first_move(board, player)
            
            if opponent_first_move:
                __memory__['opponent_last_moves'].append(opponent_first_move)
            
            __memory__['last_board'] = board
        else:
            last_board = __memory__['last_board']
            
            opponent_last_move = find_opponent_last_move(last_board, board)
            
            if opponent_last_move:
                __memory__['opponent_last_moves'].append(opponent_last_move)
        
        #
        update_board(board, optimal_choice, player)
    finally:
        __memory__['last_board'] = board
        memory = __memory__
    
    return optimal_choice, memory