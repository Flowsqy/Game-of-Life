# Groupe: Florian Mouro
from random import *
from tkinter import *


class GridManager:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.grid = [[0 for _ in range(y)] for _ in range(x)]
        self.tore = False

    def clear(self):
        self.grid = [[0 for _ in range(self.y)] for _ in range(self.x)]

    def random(self):
        self.grid = [[randint(0, 1) for _ in range(self.y)] for _ in range(self.x)]

    def print_grid(self):
        for x_line in self.grid:
            for y_elem in x_line:
                print(y_elem, end="")
            print()

    def next_state_tore(self, x, y):
        grid = self.grid
        previous_x = x - 1
        previous_y = y - 1
        x_length = len(grid)
        y_length = len(grid[x])
        if x + 1 == x_length:
            previous_x -= x_length
        if y + 1 == y_length:
            previous_y -= y_length
        alive = grid[x][y] == 1
        cells = 0
        if alive:
            cells -= 1
        for current_x in range(previous_x, previous_x + 3):
            for current_y in range(previous_y, previous_y + 3):
                cells += grid[current_x][current_y]
        if alive:
            if cells == 2 or cells == 3:
                return 1
            else:
                return 0
        else:
            if cells == 3:
                return 1
            else:
                return 0

    def next_state_classic(self, x, y):
        grid = self.grid
        x_length = len(grid)
        y_length = len(grid[x])
        alive = grid[x][y] == 1
        cells = 0
        if alive:
            cells -= 1
        for current_x in range(x - 1, x + 2):
            if 0 <= current_x < x_length:
                for current_y in range(y - 1, y + 2):
                    if 0 <= current_y < y_length:
                        cells += grid[current_x][current_y]
        if alive:
            if 4 > cells > 1:
                return 1
            else:
                return 0
        else:
            if cells == 3:
                return 1
            else:
                return 0

    def next_grid(self):
        grid = self.grid
        new_grid = []
        for x in range(len(grid)):
            new_line = []
            for y in range(len(grid[x])):
                if self.tore:
                    new_line.append(self.next_state_tore(x, y))
                else:
                    new_line.append(self.next_state_classic(x, y))
            new_grid.append(new_line)
        return new_grid

    def next_gen(self):
        self.grid = self.next_grid()


class Window:

    def __init__(self, window_width, window_height, canvas_width, canvas_height, grid_manager):
        window = Tk()
        window.geometry(str(window_width) + "x" + str(window_height))
        window.title("Jeu de la vie")
        window.resizable(False, False)

        canvas = Canvas(window, width=canvas_width, height=canvas_height)
        canvas.bind("<Button-1>", self.toggle_square)
        canvas.pack(side=LEFT)

        frame = Frame(window)
        frame.pack()

        random_button = Button(frame, text="Configuration aléatoire", command=self.random_fill)
        random_button.grid(column=0, row=0)

        next_button = Button(frame, text="Génération suivante", command=self.next_gen)
        next_button.grid(column=0, row=1)

        auto_button = Button(frame, text="Automatique", command=self.toggle_loop)
        auto_button.grid(column=0, row=2)

        clear_button = Button(frame, text="Nettoyer", command=self.clear_grid)
        clear_button.grid(column=0, row=3)

        tore_button = Button(frame, text="Tore", command=self.toggle_tore)
        tore_button.grid(column=0, row=4)

        auto_label = Label(frame, text="Automatique: Non")
        auto_label.grid(column=0, row=5)

        tore_label = Label(frame, text="Tore: Non")
        tore_label.grid(column=0, row=6)

        self.window = window
        self.canvas = canvas
        self.auto_label = auto_label
        self.tore_label = tore_label
        self.grid_manager = grid_manager
        self.x_size = canvas_width / grid_manager.x
        self.y_size = canvas_height / grid_manager.y
        self.auto = False

    def start(self):
        self.draw_grid()
        self.window.mainloop()

    def draw_grid(self):
        grid = self.grid_manager.grid
        self.canvas.delete("all")
        for x in range(len(grid)):
            for y in range(len(grid[x])):
                self.draw_square(x, y, self.x_size, self.y_size, grid[x][y] == 1)

    def draw_square(self, x, y, x_size, y_size, state):
        color = "WHITE"
        if state:
            color = "RED"
        self.canvas.create_rectangle(x * x_size, y * y_size, (x + 1) * x_size, (y + 1) * y_size, fill=color)

    def random_fill(self):
        self.grid_manager.random()
        self.draw_grid()

    def next_gen(self):
        self.grid_manager.next_gen()
        self.draw_grid()

    def toggle_square(self, event):
        if self.auto:
            return
        x_size = self.x_size
        y_size = self.y_size
        grid = self.grid_manager.grid
        x = int(event.x // x_size)
        y = int(event.y // y_size)
        if x >= len(grid) or y >= len(grid[x]):
            return
        state = grid[x][y] == 1
        if state:
            grid[x][y] = 0
        else:
            grid[x][y] = 1
        self.draw_square(x, y, x_size, y_size, not state)

    def toggle_loop(self):
        self.auto = not self.auto
        state = "Non"
        if self.auto:
            state = "Oui"
        self.auto_label.config(text="Automatique: " + state)
        self.auto_loop()

    def auto_loop(self):
        if self.auto:
            self.next_gen()
            self.window.after(100, self.auto_loop)

    def clear_grid(self):
        self.grid_manager.clear()
        self.draw_grid()
        if self.auto:
            self.toggle_loop()

    def toggle_tore(self):
        self.grid_manager.tore = not self.grid_manager.tore
        state = "Non"
        if self.grid_manager.tore:
            state = "Oui"
        self.tore_label.config(text="Tore: " + state)


if __name__ == '__main__':
    grid_data = GridManager(20, 20)
    main_window = Window(720, 480, 480, 480, grid_data)
    main_window.draw_grid()
    main_window.start()
