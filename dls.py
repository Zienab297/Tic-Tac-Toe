import tkinter as tk
from tkinter import messagebox

def check_win(board, player):
    for i in range(3):
        row_win = True
        col_win = True
        for j in range(3):
            if board[i][j] != player:
                row_win = False
            if board[j][i] != player:
                col_win = False
        if row_win or col_win:
            return True

    diagonal1_win = all(board[i][i] == player for i in range(3))
    diagonal2_win = all(board[i][2 - i] == player for i in range(3))
    
    if diagonal1_win or diagonal2_win:
        return True

    return False


def check_draw(board):
    for row in board:
        for cell in row:
            if cell == " ":
                return False  # If there is an empty cell, it is not a tie.
    return True

def minimax(board, depth, is_maximizing):
    if check_win(board, "O"):
        return 1
    if check_win(board, "X"):
        return -1
    if check_draw(board):
        return 0

    if is_maximizing:
        best_score = -float("inf")
        for i in range(3):
            for j in range(3):
                if board[i][j] == " ":
                    board[i][j] = "O"
                    score = minimax(board, depth + 1, False)
                    board[i][j] = " "
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = float("inf")
        for i in range(3):
            for j in range(3):
                if board[i][j] == " ":
                    board[i][j] = "X"
                    score = minimax(board, depth + 1, True)
                    board[i][j] = " "
                    best_score = min(score, best_score)
        return best_score

def get_computer_move(board):
    best_score = -float("inf")
    best_move = (-1, -1)
    for i in range(3):
        for j in range(3):
            if board[i][j] == " ":
                board[i][j] = "O"
                score = minimax(board, 0, False)
                board[i][j] = " "
                if score > best_score:
                    best_score = score
                    best_move = (i, j)
    return best_move

def on_click(row, col):
    global board, current_player, winner
    if board[row][col] == " " and not winner:
        board[row][col] = current_player
        buttons[row][col].config(text=current_player, state=tk.DISABLED)
        
        if check_win(board, current_player):
            messagebox.showinfo("Tic-Tac-Toe", f"{current_player} wins!")
            winner = current_player
        elif not check_draw(board):
            ai_move = get_computer_move(board)
            ai_row, ai_col = ai_move
            board[ai_row][ai_col] = "O"
            buttons[ai_row][ai_col].config(text="O", state=tk.DISABLED)
        if check_win(board, "O"):
                messagebox.showinfo("Tic-Tac-Toe", "Computer wins!")
                winner = "O"
        elif check_draw(board):
                messagebox.showinfo("Tic-Tac-Toe", "Draw!")


window = tk.Tk()
window.title("Tic-Tac-Toe")

#board
board = [[" " for _ in range(3)] for _ in range(3)]
buttons = []
for i in range(3):
    row_buttons = []
    for j in range(3):
        button = tk.Button(window, text=" ", font=("normal", 24), width=5, height=2, command=lambda i=i, j=j: on_click(i, j))
        button.grid(row=i, column=j)
        row_buttons.append(button)
    buttons.append(row_buttons)


current_player = "X"
winner = None

window.mainloop()
