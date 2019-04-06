import tkinter as tk
import BalancedBSTSet as bst


WIDTH = 800
HEIGHT = 600


class Application:
    def __init__(self, width=WIDTH, height=HEIGHT):
        self.root = tk.Tk()
        self.root.geometry(f'{width}x{height}')

        self.c = tk.Canvas(self.root, bg='white')
        self.c.pack(padx=0, pady=4, fill='both', expand=1, side='left')

        self.frame = tk.Frame(self.root, width=150, relief='sunken', bd=1)
        self.frame.pack(padx=4, pady=4, fill='y', side='right')

        self.label1 = tk.Label(self.frame, text="Hello world")
        self.label1.pack(fill='x', padx=4, pady=2)

        self.entry1 = tk.Entry(self.frame)
        self.entry1.pack(fill='x', padx=4, pady=2)

        self.button1 = tk.Button(self.frame, text="Do something", bd=1)
        self.button1.pack(fill='x', padx=4, pady=2)

        self.root.bind('<Configure>', self.update)
        self.root.mainloop()

    @property
    def canvas_size(self):
        return self.c.winfo_width(), self.c.winfo_height()

    def update(self, a):
        self.c.update()


if __name__ == '__main__':
    Application()