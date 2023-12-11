import tkinter as tk
import heapq     #priority queue using min binary heap
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
                return False  # IIf there is an empty cell, it is not a tie.
    return True

def get_heuristic(board):
    # Heuristic for the A* algorithm: the number of Xs minus the number of Os
    x_count = sum(row.count("X") for row in board)
    o_count = sum(row.count("O") for row in board)
    return x_count - o_count

def astar_search(board):
    frontier = [] #the queue
    initial_state = (board, 0, 0, "") #represents the state of the board, depth, cost, and move
    heapq.heappush(frontier, initial_state) #pushes initial state into queue

    while frontier:
        current_state = heapq.heappop(frontier)
        current_board, depth, cost, move = current_state

        if check_win(current_board, "O"):
            return move
        if check_draw(current_board):
            return move

        for i in range(3):
            for j in range(3):
                if current_board[i][j] == " ":
                    new_board = [row[:] for row in current_board]
                    new_board[i][j] = "O"
                    new_cost = get_heuristic(new_board) + depth + 1         #this is where the heuristic becomes efficient
                    new_move = move + f"{i}{j}"
                    heapq.heappush(frontier, (new_board, depth + 1, new_cost, new_move))  #where depth is incremented

def on_click(row, col):
    global board, current_player, winner
    if board[row][col] == " " and not winner:
        board[row][col] = current_player
        buttons[row][col].config(text=current_player, state=tk.DISABLED)
        
        if check_win(board, current_player):
            messagebox.showinfo("Tic-Tac-Toe", f"{current_player} wins!")
            winner = current_player
        elif not check_draw(board):
            ai_move = astar_search(board)
            ai_row, ai_col = int(ai_move[0]), int(ai_move[1])
            board[ai_row][ai_col] = "O"
            buttons[ai_row][ai_col].config(text="O", state=tk.DISABLED)
        if check_win(board, "O"):
                messagebox.showinfo("Tic-Tac-Toe", "Computer wins!")
                winner = "O"
        elif check_draw(board):
                messagebox.showinfo("Tic-Tac-Toe", "Draw!")


# Create the main window
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
