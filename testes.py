import tkinter as tk
import BalancedBSTSet as bst


WIDTH = 800
HEIGHT = 600
BASERADIUS = 100


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
        # self.tree.add(5)
        # self.tree.add(1)
        # self.tree.add(10)
        # self.tree.add(9)
        # self.tree.add(4)
        # self.tree.add(0)
        # self.tree.add(23)
        # self.tree.add(2)
        # self.tree.add(3)
        # self.tree.add(8)

        self.root.bind('<Configure>', self.update)
        self.root.mainloop()

    def _draw_tree(self, curr_node, level=1):
        if curr_node is None: return

        # the Y position of the node
        curr_node.y = level*self.ysep - self.ysep/2

        # the X position of the node
        if curr_node.parent is None:
            curr_node.x = self.c.winfo_width()/2
        elif curr_node.data < curr_node.parent.data:
            curr_node.x = curr_node.parent.x - self.c.winfo_width() / (2**level)
        else:
            curr_node.x = curr_node.parent.x + self.c.winfo_width() / (2**level)

        self._draw_node(curr_node)
        self._draw_tree(curr_node.left, level+1)
        self._draw_tree(curr_node.right, level+1)


    def _draw_node(self, node):
        node.circle = self.c.create_oval(node.x - self.radius,
                                         node.y - self.radius,
                                         node.x + self.radius,
                                         node.y + self.radius,
                                         fill='red')
        if node.parent:
            node.line = self.c.create_line(node.x, node.y, node.parent.x, node.parent.y)
            self.c.tag_lower(node.line)


    def add_node(self, key):
        self.tree.add(key)


    def update(self, _):
        self.c.delete('all')
        self.scale = 1 / (self.tree.height() + 1)
        self.radius = BASERADIUS * self.scale
        self.ysep = self.c.winfo_height() * self.scale
        self._draw_tree(self.tree.root())
        self.c.update()


if __name__ == '__main__':
    Application()