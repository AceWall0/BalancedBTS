import tkinter as tk
import BalancedBSTSet as bst


WIDTH = 800
HEIGHT = 600
RADIUS = 15
YDIST = 80


class Application:
    def __init__(self, width=WIDTH, height=HEIGHT):
        self.root = tk.Tk()
        self.root.geometry(f'{width}x{height}')

        # Define widgets
        self.c = tk.Canvas(self.root, bg='white')
        self.frame = tk.Frame(self.root, width=150, relief='sunken', bd=1)
        self.label1 = tk.Label(self.frame, text="Hello world")
        self.entry1 = tk.Entry(self.frame)
        self.button1 = tk.Button(self.frame, text="Do something", bd=1)

        # Position widgets
        self.c.pack(padx=0, pady=4, fill='both', expand=1, side='left')
        self.frame.pack(padx=4, pady=4, fill='y', side='right')
        self.label1.pack(fill='x', padx=4, pady=2)
        self.entry1.pack(fill='x', padx=4, pady=2)
        self.button1.pack(fill='x', padx=4, pady=2)

        # Creates tree
        self.tree = bst.BalancedBSTSet()
        self.tree.add(5)
        self.tree.add(1)
        self.tree.add(10)
        self.tree.add(9)
        self.tree.add(4)
        self.tree.add(0)
        self.tree.add(23)
        self.tree.add(2)
        self.tree.add(3)
        self.tree.add(8)

        self.root.bind('<Configure>', self.update)
        self.root.mainloop()

    def _draw_tree(self, curr_node, level=1):
        if curr_node is None: return

        # If it has no parent, place it at the center
        if curr_node.parent is None:
            curr_node.x = self.c.winfo_width()/2

        # Otherwise, place it on the parent's position deslocated by the proper division on the screen.
        elif curr_node.data < curr_node.parent.data:
            curr_node.x = curr_node.parent.x - self.c.winfo_width() / (2*level)
        else:
            curr_node.x = curr_node.parent.x + self.c.winfo_width() / (2*level)

        self._draw_node(level*YDIST, curr_node)
        self._draw_tree(curr_node.left, level + 1)
        self._draw_tree(curr_node.right, level + 1)


    def _draw_node(self, y, node):
        node.y = y-RADIUS
        node.circle = self.c.create_oval(node.x-RADIUS,
                                         node.y-RADIUS,
                                         node.x+RADIUS,
                                         node.y+RADIUS,
                                         fill='red', outline='')

    def add_node(self, key):
        self.tree.add(key)

    def update(self, _):
        self.c.delete('all')
        self._draw_tree(self.tree.root())
        self.c.update()


if __name__ == '__main__':
    Application()