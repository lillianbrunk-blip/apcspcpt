import tkinter as tk
import random

GRID_SIZE = 3
CANVAS_SIZE = 300

# This code was generated uning ChatGPT
class ColorGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Find the Different Color")
        self.root.geometry("320x380")
        self.root.resizable(False, False)

        self.score = 0
        self.high_score = 0
        self.level = 1

        self.info = tk.Label(root, font=("Arial", 14))
        self.info.pack(pady=10)

        self.canvas = tk.Canvas(root, width=CANVAS_SIZE, height=CANVAS_SIZE, bg="white")
        self.canvas.pack()

        self.canvas.bind("<Button-1>", self.handle_click)

        self.end_label = tk.Label(root, font=("Arial", 18))
        self.retry_btn = tk.Button(root, text="Try Again", command=self.start_game)

        self.correct_index = 0
        self.cells = []

        self.start_game()

    def start_game(self):
        self.score = 0
        self.level = 1
        self.end_label.pack_forget()
        self.retry_btn.pack_forget()
        self.canvas.pack()
        self.info.pack()
        self.next_level()

    def generate_colors(self):
        base = [random.randint(80, 200) for _ in range(3)]
        diff_amount = max(40 - self.level * 3, 5)

        diff = base.copy()
        i = random.randint(0, 2)
        diff[i] = max(0, min(255, diff[i] + random.choice([-diff_amount, diff_amount])))

        return tuple(base), tuple(diff)

    def draw_grid(self):
        self.canvas.delete("all")
        self.cells.clear()

        base, diff = self.generate_colors()
        self.correct_index = random.randint(0, 8)

        cell_size = CANVAS_SIZE // GRID_SIZE

        for i in range(9):
            row = i // GRID_SIZE
            col = i % GRID_SIZE

            x1 = col * cell_size
            y1 = row * cell_size
            x2 = x1 + cell_size
            y2 = y1 + cell_size

            color = diff if i == self.correct_index else base
            hex_color = "#%02x%02x%02x" % color

            rect = self.canvas.create_rectangle(
                x1, y1, x2, y2,
                fill=hex_color,
                outline="black"
            )
            if rect not in self.cells:
                self.cells.append(rect)

    def update_info(self):
        self.info.config(
            text=f"Level: {self.level}   Score: {self.score}   High Score: {self.high_score}"
        )

    def next_level(self):
        self.update_info()
        self.draw_grid()

    def handle_click(self, event):
        cell_size = CANVAS_SIZE // GRID_SIZE
        col = event.x // cell_size
        row = event.y // cell_size
        index = row * GRID_SIZE + col

        if index == self.correct_index:
            self.score += self.level
            self.level += 1
            self.next_level()
        else:
            self.end_game(False)

    def end_game(self, win):
        if self.score > self.high_score:
            self.high_score = self.score

        self.canvas.pack_forget()
        self.info.pack_forget()

        message = "You Win! 🎉" if win else "You Lost 😢"
        self.end_label.config(text=message)

        self.end_label.pack(pady=20)
        self.retry_btn.pack(pady=10)
        
if __name__ == "__main__":
    root = tk.Tk()
    game = ColorGame(root)
    root.mainloop()