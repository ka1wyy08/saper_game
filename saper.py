import tkinter as tk
import random


class Minesweeper:
    def __init__(self, master, width=10, height=10, mines=10):
        self.master = master
        self.width, self.height, self.mines = width, height, mines
        self.buttons = {}
        self.board = [[0] * width for _ in range(height)]
        self.game_over = False

        self.setup_board()
        self.create_widgets()

    def setup_board(self):
        mine_positions = set()
        while len(mine_positions) < self.mines:
            pos = (random.randint(0, self.height - 1), random.randint(0, self.width - 1))
            if pos not in mine_positions:
                mine_positions.add(pos)
                self.board[pos[0]][pos[1]] = -1

        for r in range(self.height):
            for c in range(self.width):
                if self.board[r][c] == -1:
                    continue
                count = sum((self.board[r + dr][c + dc] == -1)
                            for dr in [-1, 0, 1] for dc in [-1, 0, 1]
                            if 0 <= r + dr < self.height and 0 <= c + dc < self.width)
                self.board[r][c] = count

    def create_widgets(self):
        for r in range(self.height):
            for c in range(self.width):
                button = tk.Button(self.master, text='', width=3,
                                   command=lambda r=r, c=c: self.reveal(r, c))
                button.grid(row=r, column=c)
                self.buttons[(r, c)] = button

    def reveal(self, r, c):
        if self.game_over or self.buttons[(r, c)]['state'] == 'disabled':
            return

        if self.board[r][c] == -1:
            self.buttons[(r, c)].config(text='*', bg='red')
            self.game_over = True
            print("Game Over!")
            return

        count = self.board[r][c]
        self.buttons[(r, c)].config(text=str(count), state='disabled')

        if count == 0:
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    if (dr != 0 or dc != 0) and (0 <= r + dr < self.height) and (0 <= c + dc < self.width):
                        self.reveal(r + dr, c + dc)


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Сапёр")
    Minesweeper(root)
    root.mainloop()
