import tkinter as tk
from tkinter import ttk, messagebox, filedialog, simpledialog
import json


class SudokuSolverGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku Solver")
        self.root.geometry("600x600")
        self.create_widgets()

    def create_widgets(self):
        self.style = ttk.Style()

        # Light shades of blue
        self.style.configure("Grid.TFrame", background="#F0F8FF")
        self.style.configure("TButton", background="#ADD8E6", foreground="black")
        self.style.map("TButton", background=[("active", "#87CEEB")], foreground=[("active", "black")])

        # Frame for the Sudoku grid
        self.grid_frame = ttk.Frame(self.root, padding="10", style="Grid.TFrame")
        self.grid_frame.grid(row=0, column=0, columnspan=9)

        self.entries = []
        for i in range(9):
            row_entries = []
            for j in range(9):
                entry = ttk.Entry(self.grid_frame, width=2, font=("Helvetica", 20), justify="center")
                entry.grid(row=i, column=j, padx=1, pady=1, ipadx=10, ipady=10)  # Adjust cell dimensions

                # Determine background color based on cell position
                bg_color = self.get_cell_background_color(i, j)
                entry.configure(background=bg_color, foreground="black")  # Light shade of blue for background
                row_entries.append(entry)
            self.entries.append(row_entries)

        # Frame for the buttons
        self.button_frame = ttk.Frame(self.root, padding="10")
        self.button_frame.grid(row=1, column=0, columnspan=9, pady=10)

        # Adding buttons
        self.solve_button = ttk.Button(self.button_frame, text="Solve", command=self.solve)
        self.solve_button.grid(row=0, column=0, padx=5)

        self.reset_button = ttk.Button(self.button_frame, text="Reset Cell", command=self.reset_cell)
        self.reset_button.grid(row=0, column=1, padx=5)

        self.reset_all_button = ttk.Button(self.button_frame, text="Reset All", command=self.reset_all)
        self.reset_all_button.grid(row=0, column=2, padx=5)

        self.save_button = ttk.Button(self.button_frame, text="Save", command=self.save_puzzle)
        self.save_button.grid(row=0, column=3, padx=5)

        self.load_button = ttk.Button(self.button_frame, text="Load", command=self.load_puzzle)
        self.load_button.grid(row=0, column=4, padx=5)

        self.hint_button = ttk.Button(self.button_frame, text="Hint", command=self.hint)
        self.hint_button.grid(row=0, column=5, padx=5)

        self.generate_button = ttk.Button(self.button_frame, text="Generate", command=self.generate_puzzle)
        self.generate_button.grid(row=0, column=6, padx=5)

    def get_cell_background_color(self, i, j):
        # Determine the background color based on the cell position
        if (i // 3) % 2 == 0:
            if (j // 3) % 2 == 0:
                return "#B0E0E6"  # Light blue
            else:
                return "#87CEEB"  # Dark blue
        else:
            if (j // 3) % 2 == 0:
                return "#87CEEB"  # Dark blue
            else:
                return "#B0E0E6"  # Light blue

    def get_board(self):
        board = []
        for row_entries in self.entries:
            row = []
            for entry in row_entries:
                val = entry.get()
                if val.isdigit():
                    row.append(int(val))
                else:
                    row.append(0)
            board.append(row)
        return board

    def set_board(self, board):
        for i, row_entries in enumerate(self.entries):
            for j, entry in enumerate(row_entries):
                if board[i][j] != 0:
                    entry.delete(0, tk.END)
                    entry.insert(0, str(board[i][j]))
                else:
                    entry.delete(0, tk.END)

    def solve(self):
        board = self.get_board()
        if self.sudoku_solver(board):
            self.set_board(board)
            messagebox.showinfo("Sudoku Solver", "Sudoku solved successfully!")
        else:
            messagebox.showerror("Sudoku Solver", "No solution exists for the given Sudoku.")

    def sudoku_solver(self, board):
        empty = self.find_empty_location(board)
        if not empty:
            return True  # Puzzle solved

        row, col = empty

        for num in range(1, 10):
            if self.is_safe(board, row, col, num):
                board[row][col] = num

                if self.sudoku_solver(board):
                    return True

                board[row][col] = 0

        return False

    def find_empty_location(self, board):
        for i in range(9):
            for j in range(9):
                if board[i][j] == 0:
                    return (i, j)
        return None

    def is_safe(self, board, row, col, num):
        for i in range(9):
            if board[row][i] == num or board[i][col] == num:
                return False

        box_start_row, box_start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(3):
            for j in range(3):
                if board[box_start_row + i][box_start_col + j] == num:
                    return False

        return True

    def reset_cell(self):
        selected_entry = self.root.focus_get()
        if selected_entry in [entry for row in self.entries for entry in row]:
            selected_entry.delete(0, tk.END)

    def reset_all(self):
        for row_entries in self.entries:
            for entry in row_entries:
                entry.delete(0, tk.END)

    def hint(self):
        board = self.get_board()
        empty = self.find_empty_location(board)
        if empty:
            row, col = empty
            for num in range(1, 10):
                if self.is_safe(board, row, col, num):
                    self.entries[row][col].delete(0, tk.END)
                    self.entries[row][col].insert(0, str(num))
                    messagebox.showinfo("Sudoku Solver", f"Hint: Try {num} at cell ({row + 1}, {col + 1})")
                    return
            messagebox.showerror("Sudoku Solver", "No valid numbers found for the empty cell.")
        else:
            messagebox.showinfo("Sudoku Solver", "No empty cells available for hints.")

    def save_puzzle(self):
        puzzle = self.get_board()
        file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if file_path:
            with open(file_path, 'w') as file:
                json.dump(puzzle, file)
            messagebox.showinfo("Sudoku Solver", "Puzzle saved successfully!")

    def load_puzzle(self):
        file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if file_path:
            with open(file_path, 'r') as file:
                puzzle = json.load(file)
            self.set_board(puzzle)
            messagebox.showinfo("Sudoku Solver", "Puzzle loaded successfully!")

    def generate_puzzle(self):
        difficulty = simpledialog.askstring("Sudoku Solver", "Enter difficulty (easy, medium, hard):")
        if difficulty:
            puzzle = self.create_puzzle(difficulty)
            self.set_board(puzzle)
            messagebox.showinfo("Sudoku Solver", f"{difficulty.capitalize()} puzzle generated!")

    def create_puzzle(self, difficulty):
        # Here, we could implement a method to generate puzzles of different difficulty levels.
        # For simplicity, we'll use a pre-defined puzzle.
        easy_puzzle = [
            [5, 3, 0, 0, 7, 0, 0, 0, 0],
            [6, 0, 0, 1, 9, 5, 0, 0, 0],
            [0, 9, 8, 0, 0, 0, 0, 6, 0],
            [8, 0, 0, 0, 6, 0, 0, 0, 3],
            [4, 0, 0, 8, 0, 3, 0, 0, 1],
            [7, 0, 0, 0, 2, 0, 0, 0, 6],
            [0, 6, 0, 0, 0, 0, 2, 8, 0],
            [0, 0, 0, 4, 1, 9, 0, 0, 5],
            [0, 0, 0, 0, 8, 0, 0, 7, 9]
        ]
        medium_puzzle = [
            [0, 0, 0, 0, 7, 0, 0, 3, 0],
            [0, 0, 6, 0, 0, 5, 0, 0, 0],
            [3, 5, 9, 8, 0, 0, 0, 7, 4],
            [2, 6, 0, 0, 0, 0, 7, 0, 0],
            [0, 0, 4, 3, 6, 9, 8, 0, 0],
            [0, 0, 8, 0, 0, 0, 0, 6, 2],
            [9, 4, 0, 0, 0, 8, 5, 1, 2],
            [0, 0, 0, 9, 0, 0, 3, 0, 0],
            [0, 2, 0, 0, 5, 0, 0, 0, 0]
        ]
        hard_puzzle = [
            [8, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 3, 6, 0, 0, 0, 0, 0],
            [0, 7, 0, 0, 9, 0, 2, 0, 0],
            [0, 5, 0, 0, 0, 7, 0, 0, 0],
            [0, 0, 0, 0, 4, 5, 7, 0, 0],
            [0, 0, 0, 1, 0, 0, 0, 3, 0],
            [0, 0, 1, 0, 0, 0, 0, 6, 8],
            [0, 0, 8, 5, 0, 0, 0, 1, 0],
            [0, 9, 0, 0, 0, 0, 4, 0, 0]
        ]
        if difficulty == 'easy':
            return easy_puzzle
        elif difficulty == 'medium':
            return medium_puzzle
        elif difficulty == 'hard':
            return hard_puzzle
        else:
            return easy_puzzle


if __name__ == "__main__":
    root = tk.Tk()
    app = SudokuSolverGUI(root)
    root.mainloop()
