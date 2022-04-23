from tkinter import font
import tkinter as tk
import numpy as np

# =============================================================================
'''In order to start the software, right click the window and press start!'''
'''I used a tutorial for the majority of the project, so it may be a bit clunky'''
# =============================================================================


# =============================================================================
# Puzzle object and methods. Sudoku algorithm essentially
# =============================================================================

class Sudoku():
    def __init__(self, puzzle):
        self.board = np.array(puzzle)

    def valid(self):
        '''Function that checks to make sure the given puzzle adheres to the
        rules of Sudoku.  It checks rows, columns, and 3x3 grids.'''
        for l in range(9):

            row = np.trim_zeros(np.sort((self.board[l, :]), axis=None))
            if len(row[:-1][row[1:] == row[:-1]]) != 0:
                print('\nERROR: Puzzle is invalid.  Repeated row value detected.')
                return False
            col = np.trim_zeros(np.sort((self.board[:, l]), axis=None))
            if len(col[:-1][col[1:] == col[:-1]]) != 0:
                print('\nERROR: Puzzle is invalid.  Repeated column value detected.')
                return False

        for a, b in [0, 3], [3, 6], [6, 9]:
            for c, d in [0, 3], [3, 6], [6, 9]:
                check = np.trim_zeros(np.sort(np.reshape(self.board[a:b, c:d], (1, 9)), axis=None))
                if len(check[:-1][check[1:] == check[:-1]]) != 0:
                    print('\nERROR: Puzzle is invalid.  Repeated 3x3 value detected.')
                    return False
        return True

    def full(self):
        '''Checks if board only contains the numbers 1-9.'''
        if 0 in self.board:
            return False
        else:
            return True

    def possibilities(self, i, j):
        '''Given a board location, return an array of possible legal entries'''
        row = np.trim_zeros(np.sort((self.board[i, :]), axis=None))
        col = np.trim_zeros(np.sort((self.board[:, j]), axis=None))
        for a, b in [0, 3], [3, 6], [6, 9]:
            for c, d in [0, 3], [3, 6], [6, 9]:
                if a <= i < b and c <= j < d:
                    grid = np.trim_zeros(np.sort(np.reshape(self.board[a:b, c:d], (1, 9)), axis=None))
                    break
            else:
                continue
            break
        taken = np.unique(np.concatenate((row, col, grid)))
        return np.setdiff1d(np.arange(1, 10, 1), taken)

    def solve(self):
        '''Backtracking Sudoku solving algorithm.  Recursively checks all
        possibilities at each board location, if there are no legal possibilities
        the location is reset and the algorithm backtracks.'''
        if self.full() == True:
            return self.board
        else:
            for i in range(9):
                for j in range(9):
                    if self.board[i, j] == 0:
                        break
                else:
                    continue
                break
            poss = self.possibilities(i, j)
            for n in poss:
                self.board[i, j] = n
                self.solve()
                if self.full() == True:
                    return self.board
            self.board[i, j] = 0


# =============================================================================
# Table object and methods
# Use colors bisque or grey69, or use alternative #D3D3D3 #ADD8E6
# =============================================================================

class SimpleTableInput(tk.Frame):
    def __init__(self, parent):
        '''On init creates a tkinter frame with a 9x9 grid of entry widgets.
        Also defines a variable to register a command for validation.'''
        tk.Frame.__init__(self, parent)

        '''Variable for input register validation see .validate(P) below'''
        vcmd = (self.register(self.validate), "%P")

        self.entry = {}
        f = font.Font(size=30, weight='normal')

        for row in range(9):
            for column in range(9):
                index = (row, column)
                if row in [0, 1, 2, 6, 7, 8] and column in [0, 1, 2, 6, 7, 8]:
                    e = tk.Entry(self, bg="#ADD8E6", font=f, validate="key", validatecommand=vcmd, justify="center")
                elif row in [3, 4, 5] and column in [3, 4, 5]:
                    e = tk.Entry(self, bg="#ADD8E6", font=f, validate="key", validatecommand=vcmd, justify="center")
                else:
                    e = tk.Entry(self, bg="#D3D3D3", font=f, validate="key", validatecommand=vcmd, justify="center")
                e.grid(row=row, column=column, stick="nsew")
                self.entry[index] = e

        self.grid_rowconfigure(9, weight=1)
        for col in range(9):
            self.grid_columnconfigure(col, weight=1)

    def validate(self, P):
        '''Perform input validation, only allows single digit integers.'''
        if P.strip() == "":
            return True
        if len(str(P)) > 1:
            self.bell()
            return False
        try:
            int(P)
        except ValueError:
            self.bell()
            return False
        return True

    def clear(self):
        '''Clears the entry table.'''
        for row in range(9):
            for column in range(9):
                index = (row, column)
                self.entry[index].delete(0, len(str(self.entry[index])))

    def pull(self):
        '''Return a list of lists, containing the data in the table.'''
        table = np.zeros((9, 9), dtype=int)
        for row in range(9):
            for col in range(9):
                index = (row, col)
                if self.entry[index].get() != '':
                    table[row][col] = int(self.entry[index].get())
        return table

    def fill(self, puzzle):
        '''Fills table with the given puzzle.'''
        for row in range(9):
            for column in range(9):
                if puzzle[row][column] != 0:
                    index = (row, column)
                    self.entry[index].insert(0, puzzle[row][column])

    def example(self, i):
        '''Sets up an automatically generated puzzle to be solved.'''
        if i == 0:
            x = np.array([[0, 0, 3, 0, 2, 0, 6, 0, 0], [9, 0, 0, 3, 0, 5, 0, 0, 1], [0, 0, 1, 8, 0, 6, 4, 0, 0],
                          [0, 0, 8, 1, 0, 2, 9, 0, 0], [7, 0, 0, 0, 0, 0, 0, 0, 8], [0, 0, 6, 7, 0, 8, 2, 0, 0],
                          [0, 0, 2, 6, 0, 9, 5, 0, 0], [8, 0, 0, 2, 0, 3, 0, 0, 9], [0, 0, 5, 0, 1, 0, 3, 0, 0]])
        elif i == 1:
            x = np.array([[4, 0, 5, 0, 0, 9, 0, 6, 0], [0, 0, 0, 0, 0, 0, 4, 3, 0], [0, 2, 0, 0, 6, 7, 0, 1, 8],
                          [0, 1, 4, 5, 0, 0, 0, 0, 0], [0, 0, 8, 0, 0, 0, 0, 0, 7], [0, 9, 0, 0, 0, 0, 1, 0, 6],
                          [0, 4, 3, 0, 0, 0, 0, 0, 0], [0, 0, 0, 9, 0, 0, 0, 0, 0], [0, 0, 0, 1, 0, 2, 3, 0, 0]])
        elif i == 2:
            x = np.array([[5, 0, 0, 0, 8, 0, 1, 6, 0], [3, 0, 0, 0, 9, 2, 0, 0, 8], [0, 0, 0, 5, 0, 0, 0, 4, 9],
                          [0, 0, 0, 0, 7, 0, 4, 0, 5], [0, 0, 0, 9, 3, 4, 0, 0, 0], [7, 0, 8, 0, 5, 0, 0, 0, 0],
                          [2, 6, 0, 0, 0, 1, 0, 0, 0], [4, 0, 0, 7, 2, 0, 0, 0, 3], [0, 5, 7, 0, 6, 0, 0, 0, 4]])
        self.fill(x)


# =============================================================================
# GUI Object, button widgets, and methods
# =============================================================================

class Sudoku_GUI(tk.Frame):
    def __init__(self, parent):
        '''On init creates the input table, adds buttons to the frame, and
        packs everything together.'''
        tk.Frame.__init__(self, parent)
        f = font.Font(size=25, weight='bold')
        self.table = SimpleTableInput(self)

        self.solve = tk.Button(self, font=f, text="Solve", command=self.on_solve)
        self.clear = tk.Button(self, font=f, text="Clear Grid", command=self.on_clear)
        self.example = tk.Button(self, font=f, text="Premad›e Sudoku", command=self.on_example)
        self.click_count = 0

        self.table.pack(side="top", fill="both", expand=True)
        self.solve.pack(side="left", expand=1)
        self.example.pack(side="left", expand=1)
        self.clear.pack(side="left", expand=1)

    def on_solve(self):
        '''Solve button'''
        if Sudoku(self.table.pull()).valid() == True:

            solved = Sudoku(self.table.pull()).solve()
            if Sudoku(solved) == None:
                print('ERROR: No Solution Found')
            if Sudoku(solved).valid() == True:
                print('\nSUCCESS: Valid solution has been found.')
                self.table.clear()
                self.table.fill(solved)
            else:
                print('ERROR: Invalid solution found')
                self.table.clear()
                self.table.fill(solved)

    def on_example(self):
        '''Example button.'''
        self.click_count = (self.click_count + 1) % 3
        self.table.clear()
        self.table.example(self.click_count)

    def on_clear(self):
        '''Clear button.'''
        self.table.clear()


# =============================================================================
# Window loop
# =============================================================================

root = tk.Tk()
root.title('Roddyw123s tutorial sudoku solver algorithm')
root.geometry('500x500')
root.resizable(width=False, height=False)
Sudoku_GUI(root).pack(side="top", fill="both", expand=True)
root.mainloop()