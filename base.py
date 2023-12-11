import tkinter as tk
from tkinter import messagebox
import random

def check_win(board, player):
    for i in range(3):
        if all(board[i][j] == player for j in range(3)):  # Check rows
            return True
        if all(board[j][i] == player for j in range(3)):  # Check columns
            return True
    if all(board[i][i] == player for i in range(3)) or all(board[i][2 - i] == player for i in range(3)):  # Check diagonals
        return True
    return False

def check_draw(board):
    return all(cell != " " for row in board for cell in row)

def get_computer_move(board):
    empty_cells = [(i, j) for i in range(3) for j in range(3) if board[i][j] == " "]
    return random.choice(empty_cells)

def on_click(row, col):
    global board, current_player, winner
    if board[row][col] == " " and not winner:
        board[row][col] = current_player
        buttons[row][col].config(text=current_player, state=tk.DISABLED)
        
        if check_win(board, current_player):
            messagebox.showinfo("Tic-Tac-Toe", f"Player {current_player} wins!")
            winner = current_player
        elif not check_draw(board):
            ai_row, ai_col = get_computer_move(board)
            board[ai_row][ai_col] = "O"
            buttons[ai_row][ai_col].config(text="O", state=tk.DISABLED)
            if check_win(board, "O"):
                messagebox.showinfo("Tic-Tac-Toe", "Player O wins!")
                winner = "O"
            elif check_draw(board):
                messagebox.showinfo("Tic-Tac-Toe", "It's a draw!")

def restart_game():
    global board, current_player, winner
    board = [[" " for _ in range(3)] for _ in range(3)]
    current_player = "X"
    winner = None

    for i in range(3):
        for j in range(3):
            buttons[i][j].config(text=" ", state=tk.NORMAL)

# Create the main window
window = tk.Tk()
window.title("Tic-Tac-Toe")

# Create the game board
board = [[" " for _ in range(3)] for _ in range(3)]
buttons = []
for i in range(3):
    row_buttons = []
    for j in range(3):
        button = tk.Button(window, text=" ", font=("normal", 24), width=5, height=2, command=lambda i=i, j=j: on_click(i, j))
        button.grid(row=i, column=j)
        row_buttons.append(button)
    buttons.append(row_buttons)

# Create a restart button
restart_button = tk.Button(window, text="Restart", font=("normal", 16), command=restart_game)
restart_button.grid(row=3, column=0, columnspan=3)

# Initialize game variables
current_player = "X"
winner = None

# Start the game
window.mainloop()
