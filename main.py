import tkinter as tk
import random

class TicTacToe:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Tic Tac Toe")
        self.window.geometry("400x500")
        self.current_player = "X"
        self.board = ["" for _ in range(9)]
        self.game_mode = None
        self.difficulty = "Easy"
        self.history = []
        self.future_moves = []
        self.create_menu()

    def create_menu(self):
        self.menu_frame = tk.Frame(self.window)
        self.menu_frame.pack()
        
        tk.Label(self.menu_frame, text="Tic Tac Toe", font=("Arial", 20)).pack(pady=10)
        
        tk.Button(self.menu_frame, text="Player vs Player", font=("Arial", 14), command=lambda: self.start_game("PVP")).pack(pady=5)
        tk.Button(self.menu_frame, text="Player vs Computer", font=("Arial", 14), command=self.choose_difficulty).pack(pady=5)
    
    def choose_difficulty(self):
        self.menu_frame.destroy()
        self.difficulty_frame = tk.Frame(self.window)
        self.difficulty_frame.pack()
        
        tk.Label(self.difficulty_frame, text="Choose Difficulty", font=("Arial", 18)).pack(pady=10)
        tk.Button(self.difficulty_frame, text="Easy", font=("Arial", 14), command=lambda: self.start_game("PVC", "Easy")).pack(pady=5)
        tk.Button(self.difficulty_frame, text="Medium", font=("Arial", 14), command=lambda: self.start_game("PVC", "Medium")).pack(pady=5)
        tk.Button(self.difficulty_frame, text="Difficult", font=("Arial", 14), command=lambda: self.start_game("PVC", "Difficult")).pack(pady=5)
    
    def start_game(self, mode, difficulty=None):
        self.game_mode = mode
        if difficulty:
            self.difficulty = difficulty
        if hasattr(self, 'difficulty_frame'):
            self.difficulty_frame.destroy()
        self.create_board()
    
    def create_board(self):
        self.menu_frame.destroy()
        self.buttons = []
        self.board_frame = tk.Frame(self.window)
        self.board_frame.pack()
        
        for i in range(9):
            btn = tk.Button(self.board_frame, text="", font=("Arial", 24), width=5, height=2, command=lambda i=i: self.make_move(i))
            btn.grid(row=i//3, column=i%3)
            self.buttons.append(btn)
        
        self.status_label = tk.Label(self.window, text=f"Player {self.current_player}'s Turn", font=("Arial", 14))
        self.status_label.pack(pady=10)
        
        self.undo_button = tk.Button(self.window, text="Undo", font=("Arial", 12), command=self.undo_move)
        self.undo_button.pack(side=tk.LEFT, padx=10)
        
        self.redo_button = tk.Button(self.window, text="Redo", font=("Arial", 12), command=self.redo_move)
        self.redo_button.pack(side=tk.RIGHT, padx=10)
        
        self.back_button = tk.Button(self.window, text="Back", font=("Arial", 12), command=self.go_back)
        self.back_button.pack(pady=10)
    
    def make_move(self, index):
        if self.board[index] == "" and not self.check_winner():
            self.history.append((index, self.board[index]))
            self.future_moves.clear()
            self.board[index] = self.current_player
            self.buttons[index].config(text=self.current_player)
            
            if self.check_winner():
                self.status_label.config(text=f"{self.current_player} Wins!")
                return
            elif "" not in self.board:
                self.status_label.config(text="It's a Draw!")
                return
            
            self.current_player = "O" if self.current_player == "X" else "X"
            self.status_label.config(text=f"Player {self.current_player}'s Turn")
            
            if self.game_mode == "PVC" and self.current_player == "O":
                self.computer_move()
    
    def computer_move(self):
        empty_cells = [i for i, val in enumerate(self.board) if val == ""]
        if empty_cells:
            if self.difficulty == "Easy":
                move = random.choice(empty_cells)
            elif self.difficulty == "Medium":
                move = self.medium_ai(empty_cells)
            else:
                move = self.hard_ai(empty_cells)
            self.make_move(move)
    
    def medium_ai(self, empty_cells):
        return random.choice(empty_cells) if random.random() > 0.5 else self.best_move(empty_cells)
    
    def hard_ai(self, empty_cells):
        return self.best_move(empty_cells)
    
    def best_move(self, empty_cells):
        for move in empty_cells:
            self.board[move] = "O"
            if self.check_winner():
                self.board[move] = ""
                return move
            self.board[move] = ""
        return random.choice(empty_cells)
    
    def check_winner(self):
        win_conditions = [(0,1,2), (3,4,5), (6,7,8), (0,3,6), (1,4,7), (2,5,8), (0,4,8), (2,4,6)]
        for a, b, c in win_conditions:
            if self.board[a] == self.board[b] == self.board[c] and self.board[a] != "":
                for btn in [self.buttons[a], self.buttons[b], self.buttons[c]]:
                    btn.config(bg="lightgreen")
                return True
        return False
    
    def undo_move(self):
        if self.history:
            last_move = self.history.pop()
            index, _ = last_move
            self.future_moves.append((index, self.board[index]))
            self.board[index] = ""
            self.buttons[index].config(text="")
            self.current_player = "O" if self.current_player == "X" else "X"
            self.status_label.config(text=f"Player {self.current_player}'s Turn")
    
    def redo_move(self):
        if self.future_moves:
            next_move = self.future_moves.pop()
            index, value = next_move
            self.history.append((index, self.board[index]))
            self.board[index] = value
            self.buttons[index].config(text=value)
            self.current_player = "O" if self.current_player == "X" else "X"
            self.status_label.config(text=f"Player {self.current_player}'s Turn")
    
    def go_back(self):
        self.board_frame.destroy()
        self.status_label.destroy()
        self.undo_button.destroy()
        self.redo_button.destroy()
        self.back_button.destroy()
        self.create_menu()
    
    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    game = TicTacToe()
    game.run()
