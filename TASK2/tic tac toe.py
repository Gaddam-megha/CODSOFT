import numpy as np

# Function to print the Tic-Tac-Toe board
def print_board(board):
    for row in board:
        print(" | ".join(row))
        print("-" * 5)

# Function to check if someone has won
def check_winner(board, player):
    for row in board:
        if all(cell == player for cell in row):
            return True
    for col in range(3):
        if all(board[row][col] == player for row in range(3)):
            return True
    if all(board[i][i] == player for i in range(3)) or \
       all(board[i][2 - i] == player for i in range(3)):
        return True
    return False

# Function to check if the board is full
def is_board_full(board):
    return not any("" in row for row in board)

# Function for the AI move using Minimax algorithm
def ai_move(board, depth, maximizing_player):
    if check_winner(board, "X"):
        return -10 + depth, None
    elif check_winner(board, "O"):
        return 10 - depth, None
    elif is_board_full(board):
        return 0, None

    if maximizing_player:
        best_score = -np.inf
        best_move = None
        for i in range(3):
            for j in range(3):
                if board[i][j] == "":
                    board[i][j] = "O"
                    score, _ = ai_move(board, depth + 1, False)
                    board[i][j] = ""
                    if score > best_score:
                        best_score = score
                        best_move = (i, j)
        return best_score, best_move
    else:
        best_score = np.inf
        best_move = None
        for i in range(3):
            for j in range(3):
                if board[i][j] == "":
                    board[i][j] = "X"
                    score, _ = ai_move(board, depth + 1, True)
                    board[i][j] = ""
                    if score < best_score:
                        best_score = score
                        best_move = (i, j)
        return best_score, best_move

# Function to play the game
def play_game():
    board = [["" for _ in range(3)] for _ in range(3)]
    print("Welcome to Tic-Tac-Toe!")
    print_board(board)

    while True:
        # Human player's move
        while True:
            row = int(input("Enter the row (0, 1, 2): "))
            col = int(input("Enter the column (0, 1, 2): "))
            if 0 <= row < 3 and 0 <= col < 3 and board[row][col] == "":
                board[row][col] = "X"
                break
            else:
                print("Invalid move! Try again.")
        print_board(board)

        # Check if human player wins
        if check_winner(board, "X"):
            print("Congratulations! You win!")
            break
        # Check if it's a tie
        if is_board_full(board):
            print("It's a tie!")
            break

        # AI player's move
        score, move = ai_move(board, 0, True)
        board[move[0]][move[1]] = "O"
        print("AI's move:")
        print_board(board)

        # Check if AI wins
        if check_winner(board, "O"):
            print("AI wins! Better luck next time.")
            break
        # Check if it's a tie
        if is_board_full(board):
            print("It's a tie!")
            break

if __name__ == "__main__":
    play_game()