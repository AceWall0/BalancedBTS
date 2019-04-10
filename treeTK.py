import tkinter as tk
import BalancedBSTSet as bst


WIDTH = 800
HEIGHT = 600
BASERADIUS = 100
COLOR1 = '#7F7'
COLOR2 = '#0A0'
COLORT = '#020'


def is_float(inp):
    if inp == '': return True
    try: float(inp)
    except ValueError: return False
    return True


class Application:
    def __init__(self, width=WIDTH, height=HEIGHT):
        self.root = tk.Tk()
        self.root.geometry(f'{width}x{height}')

        # Define widgets =============================================================================
        self.c = tk.Canvas(self.root, bg='white')
        self.frm_panel = tk.Frame(self.root, width=200, relief='groove', bd=2)
        self.frm_addrmv = tk.Frame(self.frm_panel, relief='groove', bd=2)

        vcmd = (self.root.register(is_float), '%P')
        self.ent_entry = tk.Entry(self.frm_addrmv,
                                  justify='center',
                                  font=('Calibri', 14),
                                  validate='key', validatecommand=vcmd,
                                  width=3)
        self.btn_add = tk.Button(self.frm_addrmv, text='Add', width=8, command=self.add_node)
        self.btn_remove = tk.Button(self.frm_addrmv, text='Remove', width=8, command=self.remove_node)
        # ---------------------------------------------------------------------------------------------

        # Position widgets ============================================================================
        self.c.pack(padx=0, pady=4, fill='both', expand=1, side='left')
        self.frm_panel.pack(padx=2, pady=6, fill='y', side='right')
        self.frm_addrmv.pack(fill='x', side='top', padx=2, pady=2)
        self.ent_entry.pack(fill='x', side='top', padx=4, pady=4)
        self.btn_add.pack(side='right', padx=4, pady=4)
        self.btn_remove.pack(side='left', padx=4, pady=4)


        self.tree = bst.BalancedBSTSet()
        self.c.bind('<Configure>', self.update)
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
                                         width=2, fill=COLOR1, outline=COLOR2)
        if node.parent:
            node.line = self.c.create_line(node.x,
                                           node.y,
                                           node.parent.x,
                                           node.parent.y,
                                           width=2, fill=COLOR2)
            self.c.tag_lower(node.line)

        node.text = self.c.create_text(node.x,
                                       node.y,
                                       text=str(node.data),
                                       font=('Calibri', int(50*self.scale), 'bold'),
                                       fill=COLORT)


    def add_node(self):
        try:
            key = float(self.ent_entry.get())
        except ValueError:
            self.ent_entry.delete(0, 'end')
            return

        self.tree.add(key)
        self.ent_entry.delete(0, 'end')
        self.update()


    def remove_node(self):
        try:
            key = float(self.ent_entry.get())
        except ValueError:
            self.ent_entry.delete(0, 'end')
            return

        self.tree.remove(key)
        self.ent_entry.delete(0, 'end')
        self.update()


    def update(self, *_):
        self.c.delete('all')
        height = self.tree.height()
        if height >= 0:
            self.scale = 1 / (height + 1)
            self.radius = BASERADIUS * self.scale
            self.ysep = self.c.winfo_height() * self.scale
            self._draw_tree(self.tree.root())

        self.c.update()


if __name__ == '__main__':
    Application()