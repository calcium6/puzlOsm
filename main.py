from math import ceil
import time
import tkinter as tk
from AStar import *
from Result import *
from Board import *

class PuzlGui(tk.Frame):
    def __init__(self):
        self.root = tk.Tk()
        self.label_time = None
        self.label_nodes = None
        self.label_depth = None
        self.moves = None
        self.tiles_set = 0
        self.board_size = 3
        self.current_board = {}
        self.result = None

        tk.Frame.__init__(self, self.root)
        self.pack(padx = 20, pady = 20)
        self.create_board()

    def turbosvarak(self):
        self.create_labels()
        self.create_listbox()
        self.create_buttons()

    def create_labels(self):
        self.label_time = tk.Label(self, text="Time: \n")
        self.label_time.grid(row=0, column=0)

        self.label_nodes = tk.Label(self, text="Nodes explored: \n")
        self.label_nodes.grid(row=1, column=0)

        self.label_depth = tk.Label(self, text="Depth: \n")
        self.label_depth.grid(row=2, column=0)

    def create_listbox(self):
        self.moves_list = tk.Listbox(self, width=20, height=15)
        self.moves_list.grid(row=0, rowspan=self.board_size, column=2, padx=20)
        self.moves_list.bind('<<ListboxSelect>>', self.item_selected)

    def create_buttons(self):
        self.button_solve = tk.Button(self, text="Solve", height=2, width=8, command=lambda: self.solve())
        self.button_solve.grid(row=3, column=0, pady=8)
        self.button_clear = tk.Button(self, text="Clear", height=2, width=8, command=lambda: self.clear())
        self.button_clear.grid(row=4, column=0, pady=8)

    def solveBasicBoard(self, start: list[list[int]], priorityFunc: bool) -> tuple[bool, str]: #priorityFunc(False = Hamming, True = Manhattan)
        startBoard = Board(start)
        goalBoard = Board([[1,2,3],[4,5,6],[7,8,0]])
        startTime = time.time()
        solvable = startBoard.isSolvable()
        endTime = time.time()
        if not solvable:
            return (False, "This board configuration is not solvable.", (endTime - startTime))
        astar = AStar(startBoard, goalBoard, priorityFunc)
        startTime = time.time()
        result = astar.run()
        endTime = time.time()
        #output = "Time: " + str("%2f" % ((endTime - startTime) * 1000)) + " ms\n"
        #output += result.toString()
        return (True, result,("%.3f" %  (endTime - startTime)))
    
    def chunk_into_n(self, lst, n):
        size = ceil(len(lst) / n)
        return list(
            map(lambda x: lst[x * size:x * size + size],
            list(range(n)))
        )
    
    def unsolvable(self):
        top= tk.Toplevel(self.root)
        top.title("Error")
        tk.Label(top, text= "Inputted board is unsolvable").place(x=0,y=0)

    def solve(self):
        if self.tiles_set < 9:
            return
        board_input = []
        nums = []
        for tile in self.current_board.values():
            tileNum = int(tile["text"])
            nums.append(tileNum)
        board_input = self.chunk_into_n(nums, self.board_size)
        print(board_input)
        self.result = self.solveBasicBoard(board_input, True)
        if not self.result[0]:
            self.unsolvable()
            return
        self.label_time["text"] = "Time: \n" + str(self.result[2]) + " s"
        self.label_nodes["text"] = "Nodes explored: \n" + str(self.result[1].nodesExplored)
        self.label_depth["text"] = "Depth: \n" + str(self.result[1].depth)
        self.moves_list.delete(0,tk.END)
        for move in self.result[1].solution:
            self.moves_list.insert(tk.END, move)

    def clear(self):
        for tile in self.current_board:
            self.current_board[tile]["text"] = ""
        self.tiles_set = 0
        self.moves_list.delete(0,tk.END)
        self.label_time["text"] = "Time: \n"
        self.label_nodes["text"] = "Nodes explored: \n"
        self.label_depth["text"] = "Depth: \n"
        self.result = None
        return

    def create_board(self):
        for row in range(self.board_size):
            for col in range(self.board_size):
                tile = tk.Button(self, bg="#eeeed2", activebackground="#baca44", text="", font=('arial 12 bold'), borderwidth=0, height=5, width=10)
                tile.grid(row=row, column=(col+3))
                pos = (row, col)
                self.current_board.setdefault(pos, tile)
                self.current_board[pos].config(command = lambda arg = pos: self.select(arg))

    def select(self, pos: tuple):
        if self.tiles_set < (self.board_size*self.board_size):
            if self.current_board[pos]["text"] == "":
                if self.tiles_set == ((self.board_size*self.board_size)-1):
                    self.current_board[pos]["text"] = str(0)
                else:
                    self.current_board[pos]["text"] = str(self.tiles_set+1)
                self.tiles_set += 1
        return
    
    def item_selected(self, event):
        selected_indices = self.moves_list.curselection()
        print(selected_indices[0])
        self.update_puzzle_from_step(selected_indices[0])

    def update_puzzle_from_step(self, index):
        for i in range(self.board_size):
            for j in range(self.board_size):
                self.current_board[(i,j)]["text"] = str(self.result[1].boards[index][i][j])

puzl = PuzlGui()
puzl.turbosvarak()
puzl.root.mainloop()
