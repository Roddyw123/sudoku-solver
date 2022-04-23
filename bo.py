import tkinter as tk
from tkinter import Entry, IntVar, Tk

sq = []
bo = []
#OPTIONAL (DELETE IF NEEDED)
def quit_frame():
    main.destroy()

def SquareCreate():
    global t
    global data
    for j in range(0, 9):
        for i in range(0, 9):
            data = IntVar()
            t = tk.Entry(main, textvariable=data, justify="center", font=("Arial", 16))
            ixtra = 0
            jxtra = 0
            if i > 2:
                ixtra = 4
            if i > 5:
                ixtra = 8
            if j > 2:
                jxtra = 4
            if j > 5:
                jxtra = 8
            t.place(x=i * 40 + 70 + ixtra, y=j * 40 + 80 + jxtra, width=40, height=40)
            t.delete(0)
            sq.append(data)
    return sq


def readin():
    for r in range(0, 9):
        row = []
        for c in range(0, 9):
            sq.append(sq[r * 9 + c].get())
        bo.append(row)
    return bo


def solve(bo):
    find = find_empty(bo)
    if not find:
        print("Sudoku solved.")
        return True
    else:
        row, col = find

    for i in range(1, 10):
        if valid(bo, i, (row, col)):
            bo[row][col] = i

            if solve(bo):
                return True

            bo[row][col] = 0

    return False

def valid(bo, num, pos):
    # Check row
    for i in range(len(bo[0])):
        if bo[pos[0]][i] == num and pos[1] != i:
            return False

    # Check column
    for i in range(len(bo)):
        if bo[i][pos[1]] == num and pos[0] != i:
            return False

    # Check box
    box_x = pos[1] // 3
    box_y = pos[0] // 3

    for i in range(box_y * 3, box_y * 3 + 3):
        for j in range(box_x * 3, box_x * 3 + 3):
            if bo[i][j] == num and (i, j) != pos:
                return False

    return True

def find_empty(bo):
    for i in range(len(bo)):
        for j in range(len(bo[0])):
            if bo[i][j] == 0:
                return (i, j)  # row, col

    return None

# mainprogramm
main = tk.Tk()
main.geometry("500x540")
main.resizable(width=0, height=0)
l = tk.Label(main, text="RODDYW123")
l["font"] = "Arial"
l.place(x=150, y=0)
button1 = tk.Button(main, text="Exit", command=quit_frame)
button1.place(x=50, y=450)
button2 = tk.Button(main, text="Solve", command=readin)
button2.place(x=150, y=450)
SquareCreate()
Square = SquareCreate()
main.mainloop()