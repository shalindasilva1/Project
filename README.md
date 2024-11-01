# AI Player with Minimax Algorithm

This project implements an AI player for a board game using the Minimax algorithm with alpha-beta pruning. The AI player can make intelligent moves based on the current state of the board and dynamically adjust its strategy.

## Features

- **Minimax Algorithm**: The AI uses the Minimax algorithm with alpha-beta pruning to evaluate the best possible moves.
- **Dynamic Strategy Adjustment**: The AI adjusts its target number of consecutive marks (`n_target`) based on the current game state.
- **Heuristic Evaluation**: The AI evaluates the board state using a heuristic scoring function.

## Requirements

- Python 3.x

## Usage

 **Run the AI player**:
    ```python
    from player_ai_new import play

    # Example board and choices
    board = [[0, 1], [1, 0], [0, 1], []]
    choices = [0, 1, 2, 3]
    player = 0
    memory = None

    best_move, memory = play(board, choices, player, memory)
    print(f"Best move: {best_move}, Memory: {memory}")
    ```

## Functions

- **play(board, choices, player, memory)**: Main function to determine the best move for the AI player.
- **is_winning(board, player)**: Checks if the given player has a winning move on the board.
- **check_winning_move(board, col, player)**: Checks if placing a mark in the specified column results in a win.
- **minimax(board, depth, alpha, beta, maximizing_player)**: Minimax algorithm with alpha-beta pruning to evaluate the best move.
- **heuristic_score(board, player)**: Evaluates the board state using a heuristic scoring function.
- **adjust_n_target(board, n_target)**: Adjusts the target number of consecutive marks based on the current game state.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
