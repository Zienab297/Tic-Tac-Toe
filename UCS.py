import tkinter as tk
from tkinter import messagebox
import heapq

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
                return False  #If there is an empty cell, it is not a tie.
    return True

def get_initial_moves(board):
    moves = []
    for i in range(3):
        for j in range(3):
            if board[i][j] == " ":
                moves.append((i, j))
    return moves

def ucs_search(board, player):
    queue = [(0, board, player)]
    while queue:
        cost, current_board, current_player = heapq.heappop(queue)
        if check_win(current_board, player):
            return current_board
        if check_draw(current_board):
            continue
        moves = get_initial_moves(current_board)
        next_player = "X" if current_player == "O" else "O"
        for move in moves:
            new_board = [row[:] for row in current_board]
            new_board[move[0]][move[1]] = current_player
            heapq.heappush(queue, (cost + 1, new_board, next_player))

    #If there is no winning move, return the current board
    return board

def on_click(row, col):
    global board, current_player, winner
    if board[row][col] == " " and not winner:
        board[row][col] = current_player
        buttons[row][col].config(text=current_player, state=tk.DISABLED)
        
        if check_win(board, current_player):
            messagebox.showinfo("Tic-Tac-Toe", f"{current_player} wins!")
            winner = current_player
        elif not check_draw(board):
            ai_board = ucs_search(board, "O")
            for i in range(3):
                for j in range(3):
                    if ai_board[i][j] != board[i][j]:
                        ai_row, ai_col = i, j
            board[ai_row][ai_col] = "O"
            buttons[ai_row][ai_col].config(text="O", state=tk.DISABLED)
        if check_win(board, "O"):
                messagebox.showinfo("Tic-Tac-Toe", "Computer wins!")
                winner = "O"
        elif check_draw(board):
                messagebox.showinfo("Tic-Tac-Toe", "Draw!")


window = tk.Tk()
window.title("Tic-Tac-Toe")

# board
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
