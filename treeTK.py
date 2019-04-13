## @package treeTK.py
 #
 # TKinter binary tree.
 #
 # @author Wallace Alves dos Santos
 # @date 10/04/2019

# ===== Imports ===========================================
import tkinter as tk
import tkinter.ttk as ttk
import BalancedBSTSet as bst
import random as r


# ===== Constants =========================================
# Initial size for the window.
WIDTH = 800
HEIGHT = 600

BASERADIUS = 100  # Base radius for the nodes.

# Node colors -----
COLOR1A = '#5C5'  # Fill
COLOR1B = '#070'  # Outline

# Unbalanced colors
COLOR2A = 'pink'  # Fill
COLOR2B = 'red'   # Outline

# Leaf colors -----
COLOR3A = '#7F7'  # Fill
COLOR3B = '#3A3'  # Outline

COLORT = '#020'   # The node's text color
# -----------------------------------------------------------


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
        self.tree = bst.BalancedBSTSet()

        # Define widgets =============================================================================
        self.canvas = tk.Canvas(self.root, bg='white')
        self.canvas.tag_bind('node', '<Button>', self.__nodeClick)

        self.panel = ttk.Frame(self.root, width=100, borderwidth=1, relief='solid')

        self.configFrame = ttk.LabelFrame(self.panel, text=' Config ')
        self.autoBalVar = tk.BooleanVar()
        self.autoBalCB = ttk.Checkbutton(self.configFrame, text='Auto balanced',
                                         variable=self.autoBalVar, command=self.__autoBalancedHandler)

        # ...... Alpha Frame .........................................................................
        self.alphaFrame = ttk.LabelFrame(self.configFrame, text=' Alpha ')

        self.topLabel = ttk.Label(self.alphaFrame, text='Numarator: ')
        self.bottomLabel = ttk.Label(self.alphaFrame, text='Denominator: ')
        self.topSpin = ttk.Spinbox(self.alphaFrame, command=self.__alphaHandler,
                                   width=3, increment=1, from_=1, to=50)
        self.bottomSpin = ttk.Spinbox(self.alphaFrame, command=self.__alphaHandler,
                                      width=3, increment=1, from_=1, to=50)
        self.topSpin.bind('<Key>', self.__alphaHandler)
        self.bottomSpin.bind('<Key>', self.__alphaHandler)
        self.topSpin.set(self.tree.top)
        self.bottomSpin.set(self.tree.bottom)
        self.alphaLabel1 = ttk.Label(self.alphaFrame, text='\u03B1: ')
        self.alphaLabel2 = ttk.Label(self.alphaFrame, text=f'{self.tree.top/self.tree.bottom:.2f}')
        # .........................................................................................

        self.clearBtn = ttk.Button(self.panel, text='Clear', command=self.clear)
        self.rebalanceBtn = ttk.Button(self.panel, text='Rebalance', command=self.rebalance)
        self.randomBtn = ttk.Button(self.panel, text='Add Random', command=self.addRandom)

        # ..... Action Frame ......................................................................
        self.addRemoveFR = ttk.Frame(self.panel, borderwidth=1, relief='solid')
        vcmd = (self.root.register(_isFloatable), '%P')
        self.entry1 = ttk.Entry(self.addRemoveFR,
                                justify='center',
                                font=('Calibri', 14),
                                validate='key', validatecommand=vcmd,
                                width=3)
        self.entry1.bind('<KeyPress-Return>', self._add_remove)

        self.infoBtn = ttk.Button(self.addRemoveFR, text='?', width='1')
        self.addBtn = ttk.Button(self.addRemoveFR, text='Add', width=8, command=self.addNode)
        self.removeBtn = ttk.Button(self.addRemoveFR, text='Remove', width=8, command=self.removeNode)
        # ...........................................................................................

        # Position widgets ============================================================================
        self.canvas.pack(fill='both', expand=1, side='left', padx=0, pady=4)

        xpad = 4
        self.panel.pack(fill='y', side='right', padx=xpad, pady=6)
        self.configFrame.pack(fill='x', padx=xpad, pady=4)
        self.autoBalCB.pack(fill='x', padx=xpad, pady=2)

        xpad = 2
        self.alphaFrame.pack(fill='x', padx=xpad, pady=2, ipady=2)
        self.topLabel.grid(row=0, column=0, padx=xpad, pady=1, sticky='w')
        self.bottomLabel.grid(row=1, column=0, padx=xpad, pady=1, sticky='w')
        self.topSpin.grid(row=0, column=1, padx=xpad, pady=1, sticky='e')
        self.bottomSpin.grid(row=1, column=1, padx=xpad, pady=1, sticky='e')
        self.alphaLabel1.grid(row=2, column=0, padx=xpad, pady=2, sticky='e')
        self.alphaLabel2.grid(row=2, column=1, padx=xpad, pady=2)

        xpad = 4
        self.clearBtn.pack(fill='x', padx=xpad, pady=2)
        self.rebalanceBtn.pack(fill='x', padx=xpad, pady=2)
        self.randomBtn.pack(fill='x', padx=xpad, pady=2)

        self.addRemoveFR.pack(fill='x', side='top', padx=xpad, pady=8)
        self.addRemoveFR.grid_columnconfigure(1, weight=1)
        self.infoBtn.grid(row=0, column=0, padx=xpad, pady=4, sticky='ns')
        self.entry1.grid(row=0, column=1, columnspan=3, padx=xpad, pady=4, sticky='we')
        self.removeBtn.grid(row=1, column=0, columnspan=2, padx=xpad, pady=4)
        self.addBtn.grid(row=1, column=2, columnspan=2, padx=xpad, pady=4)

        self.canvas.bind('<Configure>', self.update)
        self.root.mainloop()


    ## Draws the tree recursivaly.
     #
     # @param curr_node The node from where to start to draw. Usually, you wanna start from the root.
     # @param level Used for the recursion to count each time the function goes down one level.
     # @note Note that all the visual information of the Node in the canvas is stored as the node property.
     #       Things like the x,y position, or the canvas objects Id's.
    def __drawTree(self, currNode, level=1):
        if currNode is None: return

        # The Y position of the node.
        currNode.y = level * self.ysep - self.ysep / 2

        # The X position of the node.
        if currNode.parent is None:
            currNode.x = self.canvas.winfo_width() / 2
        elif currNode.data < currNode.parent.data:
            currNode.x = currNode.parent.x - self.canvas.winfo_width() / (2 ** level)
        else:
            currNode.x = currNode.parent.x + self.canvas.winfo_width() / (2 ** level)

        self.__drawNode(currNode)
        self.__drawTree(currNode.left, level + 1)
        self.__drawTree(currNode.right, level + 1)


    ## Draw a Node in the canvas, with the text and the lines to the respective parents.
    def __drawNode(self, node):
        fillColor = COLOR1A
        outlineColor = COLOR1B

        if node.counter == 0:
            fillColor = COLOR3A
            outlineColor = COLOR3B

        if not self.tree.isBalanced(node):
            fillColor = COLOR2A
            outlineColor = COLOR2B

        node.circle = self.canvas.create_oval(node.x - self.radius, node.y - self.radius,
                                              node.x + self.radius, node.y + self.radius,
                                              width=2, fill=fillColor, outline=outlineColor)
        if node.parent:
            node.line = self.canvas.create_line(node.x, node.y, node.parent.x, node.parent.y, width=2, fill=COLOR1B)
            self.canvas.tag_lower(node.line)

        node.text = self.canvas.create_text(node.x, node.y, text=f'{node.data:g}', fill=COLORT,
                                            font=('Calibri', int(50*self.scale), 'bold'))

        def handler(event, obj=node): return self.__nodeClick(event, obj)
        self.canvas.tag_bind(node.circle, '<Button>', handler)
        self.canvas.tag_bind(node.text, '<Button>', handler)


    ## Adds the key node into the tree.
     # If no key is passed, then the number in the entry will be used.
    def addNode(self, key=None):
        if key is None:
            entry = self.entry1.get()
            if entry and entry != '-':
                key = float(entry)
        if key:
            self.tree.add(key)
            self.entry1.delete(0, 'end')
            self.update()
        self.entry1.focus_set()

    ## Removes the key node from the tree.
     # If no key is passed, then the number in the entry will be used.
    def removeNode(self, key=None):
        if key is None:
            entry = self.entry1.get()
            if entry and entry != '-':
                key = float(entry)
        if key:
            self.tree.remove(key)
            self.entry1.delete(0, 'end')
            self.update()
        self.entry1.focus_set()


    ## Add a random number into the tree.
    def addRandom(self):
        key = r.randint(-99, 99)
        while self.tree.add(key):
            key += r.randint(-99, 99)/100
        self.update()


    ## Clears the tree.
    def clear(self):
        self.canvas.delete('all')
        for node in self.tree:
            self.tree.remove(node)
        self.canvas.update()


    ## Rebalances the whole tree.
    def rebalance(self):
        if not self.tree.isEmpty():
            self.tree.rebalance()
            self.update()


    ## Called when the Enter key is pressed in the Entry.
     # Add the node from the entry in the tree if it is not in the tree yet. Remove from the tree otherwise.
    def _add_remove(self, _):
        entry = self.entry1.get()
        if entry and entry != '-':
            key = float(entry)
            if key in self.tree:
                self.removeNode(key)
            else:
                self.addNode(key)


    ## Called when the Auto Balanced checkbox is changed
     # Changes the property "selfBalanced" from the bst object.
    def __autoBalancedHandler(self):
        self.tree.selfBalanced = self.autoBalVar.get()
        if self.autoBalVar.get():
            self.tree.rebalance()
            self.update()

    ## Called when the Spinbox are changed.
     # Handles the top and bottom properties in the tree and the color of the alpha label
    def __alphaHandler(self):
        top = float(self.topSpin.get())
        bottom = float(self.bottomSpin.get())
        alpha = top/bottom
        self.alphaLabel2['text'] = f'{alpha:.2f}'
        if 0.5 < alpha < 1:
            self.alphaLabel1['foreground'] = 'black'
            self.alphaLabel2['foreground'] = 'black'
            self.tree.top = top
            self.tree.bottom = bottom
            self.update()
        else:
            self.alphaLabel1['foreground'] = 'red'
            self.alphaLabel2['foreground'] = 'red'


    ## Handles the clicks on the nodes.
    def __nodeClick(self, event, node):
        if event.num == 1: self.removeNode(node.data)
        elif event.num == 3: print(repr(node))


    ## Calculates all the scales and updates the canvas.
    def update(self, *_):
        self.canvas.delete('all')
        height = self.tree.height()
        if height >= 0:
            self.scale = 1 / (height + 1)
            self.radius = BASERADIUS * self.scale
            self.ysep = self.canvas.winfo_height() * self.scale
            self.__drawTree(self.tree.root())
        self.canvas.update()


# ====== Functions ===========================================================
##
 # Used to validate the keys in the entry. Allow only entries that can be converted to a float number.
def _isFloatable(inp):
    if inp == '' or inp == '-': return True
    try: float(inp)
    except ValueError: return False
    return True


# ===== Main Application ======================================================
if __name__ == '__main__':
    Application()