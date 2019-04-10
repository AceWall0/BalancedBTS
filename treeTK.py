## @package treeTK.py
 #
 # TKinter binary tree.
 #
 # @author Wallace Alves dos Santos
 # @date 10/04/2019

# ===== Imports ===========================================
import tkinter as tk
import tkinter.ttk as tkk
import BalancedBSTSet as bst


# ===== Constants =========================================
# Initial size for the window.
WIDTH = 800
HEIGHT = 600

# Base radius for the nodes.
# Note that this is only a arbitrary number. The actual radius is calculed based on the height of the tree.
# TODO ...and on the size of the window.
BASERADIUS = 100
COLOR1 = '#7F7'  # The node's fill color
COLOR2 = '#0A0'  # The node's outline color
COLORT = '#020'  # The node's text color


# ===== Classes =====================================================
##
 # Graphical user interface for the BalancedBSTSet implementation.
 #      To run:
 #          - python treeTK.py
 #
 # @author Wallace Alves dos Santos
 # @since 10/04/2019
 #
class Application:
    ##
     #  Constructs the application
     #
     #  @param width The window's width.
     #  @param height The window's heght.
     #
    def __init__(self, width=WIDTH, height=HEIGHT):
        self.root = tk.Tk()
        self.root.geometry(f'{width}x{height}')
        self.root.minsize(400, 400)

        # Define widgets =============================================================================
        self.c = tk.Canvas(self.root, bg='white')
        self.frm_panel = tkk.Frame(self.root, width=100)
        self.frm_addrmv = tkk.Frame(self.frm_panel, relief='groove', borderwidth=2)

        vcmd = (self.root.register(_is_floatable), '%P')
        self.ent_entry = tkk.Entry(self.frm_addrmv,
                                   justify='center',
                                   font=('Calibri', 14),
                                   validate='key', validatecommand=vcmd,
                                   width=3)
        self.btn_add = tkk.Button(self.frm_addrmv, text='Add', width=8, command=self.add_node)
        self.btn_remove = tkk.Button(self.frm_addrmv, text='Remove', width=8, command=self.remove_node)
        # ---------------------------------------------------------------------------------------------

        # Position widgets ============================================================================
        self.c.pack(fill='both', expand=1, side='left', padx=0, pady=4)

        self.frm_panel.pack(fill='y', side='right', padx=2, pady=6)

        self.frm_addrmv.pack(fill='x', side='top', padx=2, pady=2)
        self.ent_entry.pack(fill='x', side='top', padx=4, pady=4)
        self.btn_add.pack(fill='x', side='right', expand=1, padx=4, pady=4)
        self.btn_remove.pack(fill='x', side='right', expand=1, padx=4, pady=4)


        self.tree = bst.BalancedBSTSet()
        self.c.bind('<Configure>', self.update)
        self.root.mainloop()


    ## Draws the tree recursivaly.
     #
     # @param curr_node The node from where to start to draw. Usually, you wanna start from the root.
     # @param level Used for the recursion to count each time the function goes down one level.
     # @note Note that all the visual information of the Node in the canvas is stored as the node property.
     #       Things like the x,y position, or the canvas objects Id's.
     #
    def __draw_tree(self, curr_node, level=1):
        if curr_node is None: return

        # The Y position of the node.
        curr_node.y = level*self.ysep - self.ysep/2

        # The X position of the node.
        if curr_node.parent is None:
            curr_node.x = self.c.winfo_width()/2
        elif curr_node.data < curr_node.parent.data:
            curr_node.x = curr_node.parent.x - self.c.winfo_width() / (2**level)
        else:
            curr_node.x = curr_node.parent.x + self.c.winfo_width() / (2**level)

        self._draw_node(curr_node)
        self.__draw_tree(curr_node.left, level + 1)
        self.__draw_tree(curr_node.right, level + 1)


    ## Draw a Node in the canvas, with the text and the lines to the respective parents.
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
                                       text=f'{node.data:g}',
                                       font=('Calibri', int(50*self.scale), 'bold'),
                                       fill=COLORT)


    ## Takes the data in the Entry, add it as a node and clears the Entry.
    def add_node(self):
        entry = self.ent_entry.get()
        if entry:
            key = float(entry)
            self.tree.add(key)
            self.ent_entry.delete(0, 'end')
            self.update()


    ## Takes the data in the Entry, remove the corresponding node and clears the Entry.
    def remove_node(self):
        entry = self.ent_entry.get()
        if entry:
            key = float(entry)
            self.tree.remove(key)
            self.ent_entry.delete(0, 'end')
            self.update()


    ## Calculates all the scales and updates the canvas.
    def update(self, *_):
        self.c.delete('all')
        height = self.tree.height()
        if height >= 0:
            self.scale = 1 / (height + 1)
            self.radius = BASERADIUS * self.scale
            self.ysep = self.c.winfo_height() * self.scale
            self.__draw_tree(self.tree.root())
        self.c.update()


# ====== Functions ===========================================================
##
 # Used to validate the keys in the entry. Allow only entries that can be converted to a float number.
def _is_floatable(inp):
    if inp == '': return True
    try: float(inp)
    except ValueError: return False
    return True


# ===== Main Application ======================================================
if __name__ == '__main__':
    Application()