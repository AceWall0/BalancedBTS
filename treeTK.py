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
from colors import *


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
     #  @param root The window where the application is.
     #  @param width The window's width.
     #  @param height The window's heght.
     #
    def __init__(self, window: tk.Tk, width=800, height=600):
        # Constants and variables
        self.__BASERADIUS = 100
        self._theme = tk.StringVar()
        self._theme.set('dark')

        # Logic things
        self.tree = bst.BalancedBSTSet()
        self.selected = None
        self.__recently = False

        # ================== The window construction ======================
        self.root = window
        self.root.geometry(f'{width}x{height}')
        self.root.minsize(400, 400)
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        # Menu ------------------------------------------------------------
        self.menubar = tk.Menu(self.root)

        self.fileMenu = tk.Menu(self.menubar, tearoff=0)
        self.fileMenu.add_command(label='New')
        self.fileMenu.add_command(label='Open...')
        self.fileMenu.add_command(label='Save As...')
        self.menubar.add_cascade(label='File', menu=self.fileMenu)

        self.themeMenu = tk.Menu(self.menubar, tearoff=0)
        self.themeMenu.add_radiobutton(label='Light', variable=self._theme, value='light', command=self.update)
        self.themeMenu.add_radiobutton(label='Dark', variable=self._theme, value='dark', command=self.update)
        self.menubar.add_cascade(label='Theme', menu=self.themeMenu)

        self.root.config(menu=self.menubar)

        # The canvas widget -----------------------------------------------
        self.canvas = tk.Canvas(self.root, bg=themes[self._theme.get()]['bg'])
        self.canvas.bind('<Button-1>', self.__clickHandler)
        self.canvas.grid(row=0, column=0, sticky='nsew', padx=0, pady=4)

        # The right control panel -------------------------------------------------
        xpad = 4
        self.panel = ttk.Frame(self.root, width=100, borderwidth=1, relief='solid')
        self.panel.grid(row=0, column=1, sticky='ns', padx=xpad, pady=6)

        # +=== The config panel ---------------------------------------------------
        self.configFrame = ttk.LabelFrame(self.panel, text=' Config ')
        self.configFrame.pack(fill='x', padx=xpad, pady=4)

        self.autoBalVar = tk.BooleanVar()
        self.autoBalCB = ttk.Checkbutton(
            self.configFrame, text='Auto balanced', variable=self.autoBalVar, command=self.__autoBalancedHandler)
        self.autoBalCB.pack(fill='x', padx=xpad, pady=2)


        # +=== +=== The Alpha config panel -----------------------------------------
        xpad = 2
        self.alphaFrame = ttk.LabelFrame(self.configFrame, text=' Alpha ')
        self.alphaFrame.pack(fill='x', padx=xpad, pady=2, ipady=2)

        self.topLabel = ttk.Label(self.alphaFrame, text='Numarator: ')
        self.topLabel.grid(row=0, column=0, padx=xpad, pady=1, sticky='w')

        self.bottomLabel = ttk.Label(self.alphaFrame, text='Denominator: ')
        self.bottomLabel.grid(row=1, column=0, padx=xpad, pady=1, sticky='w')

        self.topSpin = ttk.Spinbox(
            self.alphaFrame, command=self.__alphaHandler, width=3, increment=1, from_=1, to=50)
        self.topSpin.bind('<Key>', self.__alphaHandler)
        self.topSpin.set(self.tree.top)
        self.topSpin.grid(row=0, column=1, padx=xpad, pady=1, sticky='e')

        self.bottomSpin = ttk.Spinbox(
            self.alphaFrame, command=self.__alphaHandler, width=3, increment=1, from_=1, to=50)
        self.bottomSpin.bind('<Key>', self.__alphaHandler)
        self.bottomSpin.set(self.tree.bottom)
        self.bottomSpin.grid(row=1, column=1, padx=xpad, pady=1, sticky='e')

        self.alphaLabel1 = ttk.Label(self.alphaFrame, text='\u03B1: ')
        self.alphaLabel1.grid(row=2, column=0, padx=xpad, pady=2, sticky='e')

        self.alphaLabel2 = ttk.Label(self.alphaFrame, text=f'{self.tree.top/self.tree.bottom:.2f}')
        self.alphaLabel2.grid(row=2, column=1, padx=xpad, pady=2)
        # +=== ------------------------------------------------------------------------------------

        # +=== Quick Action buttons -------------------------------------------------------------
        xpad = 4
        self.clearBtn = ttk.Button(self.panel, text='Clear', command=self.clear)
        self.clearBtn.pack(fill='x', padx=xpad, pady=2)

        self.rebalanceBtn = ttk.Button(self.panel, text='Rebalance', command=self.rebalance)
        self.rebalanceBtn.pack(fill='x', padx=xpad, pady=2)

        self.randomBtn = ttk.Button(self.panel, text='Add Random', command=self.addRandom)
        self.randomBtn.pack(fill='x', padx=xpad, pady=2)


        # +=== Node Action frame -----------------------------------------------------------------
        self.addRemoveFR = ttk.Frame(self.panel, borderwidth=1, relief='solid')
        self.addRemoveFR.pack(fill='x', side='top', padx=xpad, pady=8)
        # self.addRemoveFR.grid_columnconfigure(1, weight=1)


        vcmd = (self.root.register(_isFloatable), '%P')
        self.entry1 = ttk.Entry(
            self.addRemoveFR,
            justify='center',
            font=('Calibri', 12),
            validate='key', validatecommand=vcmd,
            width=3
        )
        self.entry1.bind('<KeyPress-Return>', self._add_remove)
        self.entry1.grid(row=0, column=1, padx=xpad, pady=4, sticky='we')

        self.selectBtn = ttk.Button(self.addRemoveFR, text='Select', width=8, command=self.selectNode)
        self.selectBtn.grid(row=0, column=0, padx=xpad, pady=4, sticky='ns')
        self.selectBtn.bind('<ButtonRelease>', self.__returnFocus)

        self.removeBtn = ttk.Button(self.addRemoveFR, text='Remove', width=8, command=self.removeNode)
        self.removeBtn.grid(row=1, column=0, padx=xpad, pady=4, sticky='ns')
        self.removeBtn.bind('<ButtonRelease>', self.__returnFocus)

        self.addBtn = ttk.Button(self.addRemoveFR, text='Add', width=8, command=self.addNode)
        self.addBtn.grid(row=1, column=1, padx=xpad, pady=4, sticky='ns')
        self.addBtn.bind('<ButtonRelease>', self.__returnFocus)

        # +=== Tree Info -----------------------------------------------------------------
        self.treeInfoFrame = ttk.LabelFrame(self.panel, text='Tree info')
        self.treeInfoFrame.pack(fill='x', padx=xpad)
        self.treeInfoFrame.grid_columnconfigure(0, weight=1)

        self.sizeLabel = ttk.Label(self.treeInfoFrame, text='Size:', anchor='e')
        self.sizeLabel.grid(row=0, column=0, padx=xpad, sticky='e')
        self.sizeValueLabel = ttk.Label(self.treeInfoFrame, text='', width=5)
        self.sizeValueLabel.grid(row=0, column=1, padx=xpad, sticky='e')

        self.heightLabel = ttk.Label(self.treeInfoFrame, text='Height:', anchor='e')
        self.heightLabel.grid(row=1, column=0, padx=xpad, sticky='e')
        self.heightValueLabel = ttk.Label(self.treeInfoFrame, text='', width=5)
        self.heightValueLabel.grid(row=1, column=1, padx=xpad, sticky='e')

        self.alphLabel = ttk.Label(self.treeInfoFrame, text='Alpha:', anchor='e')
        self.alphLabel.grid(row=3, column=0, padx=xpad, sticky='e')
        self.alphValueLabel = ttk.Label(self.treeInfoFrame, text='0.76', width=5)
        self.alphValueLabel.grid(row=3, column=1, padx=xpad, sticky='e')

        # +=== Node Info -------------------------------------------------------------------
        self.nodeInfoFrame = ttk.LabelFrame(self.panel, text='Node info')
        self.nodeInfoFrame.pack(fill='x', padx=xpad, pady=4)
        self.nodeInfoFrame.grid_columnconfigure(0, weight=1)

        self.selectedLabel = ttk.Label(self.nodeInfoFrame, text='Node:', anchor='e')
        self.selectedLabel.grid(row=0, column=0, padx=xpad, sticky='e')
        self.selectedValue = ttk.Label(self.nodeInfoFrame, text='', width=5)
        self.selectedValue.grid(row=0, column=1, padx=xpad, sticky='e')

        self.nodeSizeLabel = ttk.Label(self.nodeInfoFrame, text='Size:', anchor='e')
        self.nodeSizeLabel.grid(row=1, column=0, padx=xpad, sticky='e')
        self.nodeSizeValue = ttk.Label(self.nodeInfoFrame, text='', width=5)
        self.nodeSizeValue.grid(row=1, column=1, padx=xpad, sticky='e')

        self.leftChildrenLabel = ttk.Label(self.nodeInfoFrame, text='Left children:', anchor='e')
        self.leftChildrenLabel.grid(row=2, column=0, padx=xpad, sticky='e')
        self.leftChildrenValue = ttk.Label(self.nodeInfoFrame, text='', width=5)
        self.leftChildrenValue.grid(row=2, column=1, padx=xpad, sticky='e')

        self.rightChildrenLabel = ttk.Label(self.nodeInfoFrame, text='Right children:', anchor='e')
        self.rightChildrenLabel.grid(row=3, column=0, padx=xpad, sticky='e')
        self.rightChildrenValue = ttk.Label(self.nodeInfoFrame, text='', width=5)
        self.rightChildrenValue.grid(row=3, column=1, padx=xpad, sticky='e')

        self.canvas.bind('<Configure>', self.update)


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
        fillColor = themes[self._theme.get()]['nodeFill']
        outlineColor = themes[self._theme.get()]['nodeOutline']

        if node.counter == 0:
            fillColor = themes[self._theme.get()]['leafFill']
            outlineColor = themes[self._theme.get()]['leafOutline']

        elif not self.tree.isBalanced(node):
            fillColor = themes[self._theme.get()]['uNodeFill']
            outlineColor = themes[self._theme.get()]['uNodeOutline']

        radius = self.radius
        outline = 2
        fontSize = int(50*self.scale)
        if node is self.selected:
            radius *= 1.2
            outline = 3
            fontSize = int(fontSize * 1.2)

        node.circle = self.canvas.create_oval(
            node.x - radius, node.y - radius,
            node.x + radius, node.y + radius,
            width=outline, fill=fillColor, outline=outlineColor, tags='node'
        )

        if node is self.selected:
            self.canvas.tag_raise(node.circle)

        if node.parent:
            node.line = self.canvas.create_line(
                node.x, node.y,
                node.parent.x,
                node.parent.y,
                width=2, fill=themes[self._theme.get()]['nodeOutline']
            )
            self.canvas.tag_lower(node.line)

        node.text = self.canvas.create_text(
            node.x, node.y,
            text=f'{node.data:g}',
            fill=themes[self._theme.get()]['text'],
            font=('Calibri', fontSize, 'bold'),
            tags='node'
        )
        def handler(event, obj=node): return self.__clickHandler(event, obj)
        self.canvas.tag_bind(node.circle, '<Button>', handler)
        self.canvas.tag_bind(node.text, '<Button>', handler)


    ## Handles the clicks in the canvas.
     #
     # If there is a left click on a node, it will be selected. If it is a right click on a node, it will be removed.
     # If clicked outside any node, the node selected will be deselected.
    def __clickHandler(self, event, node=None):
        # As the handler fires twice when clicked on the element in the canvas (one for the canvas, one the element),
        # I needed to create this variable __recently to stop de function to run the second time in one click.

        if node:
            if event.num == 1: self.selectNode(node)
            elif event.num == 3: self.removeNode(node.data)
            self.__recently = True
            return

        if not self.__recently:
            self.selected = None
            self.update()
        self.__recently = False


    ## Gives back the focus to the entry widget.
    def __returnFocus(self, _):
        self.entry1.focus_set()


    ## Selects a node.
     #
     # If no node is passed, then the number in the entry will be used.
    def selectNode(self, node=None):
        if node is None:
            try:
                node = self.tree.findEntry(float(self.entry1.get()))
            except ValueError:
                node = None

        self.selected = node
        self.update()

        if self.selected is None: return

        self.canvas.itemconfigure(
            node.circle,
            outline=themes[self._theme.get()]['selectedOutline']
        )
        self.canvas.tag_raise(node.circle)
        self.canvas.tag_raise(node.text)


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
            self.selected = None
            self.update()

    ## Add a random number into the tree.
     #
     # If the number choosed is already in the tree, it will try to add a random decimal to this number choosed and fit
     # it in the tree, until it succeed.
    def addRandom(self):
        key = r.randint(-99, 99)
        while self.tree.add(key):
            key += r.randint(-99, 99)/100
        self.update()


    ## Clears the tree.
    def clear(self):
        for node in self.tree:
            self.tree.remove(node)
        self.update()


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
            self.alphValueLabel['text'] = f'{alpha:.2f}'
            self.tree.top = top
            self.tree.bottom = bottom
            self.update()
        else:
            self.alphaLabel1['foreground'] = 'red'
            self.alphaLabel2['foreground'] = 'red'


    ## Calculates all the scales and updates the canvas.
    def update(self, *_):
        self.canvas.delete('all')
        self.canvas['bg'] = themes[self._theme.get()]['bg']

        height = self.tree.height()
        if height >= 0:
            self.scale = 1 / (height + 1)
            self.radius = self.__BASERADIUS * self.scale
            self.ysep = self.canvas.winfo_height() * self.scale
            self.__drawTree(self.tree.root())

        self.sizeValueLabel['text'] = f'{self.tree.root().size if self.tree.root() else 0}'
        self.heightValueLabel['text'] = f'{self.tree.height()}'
        if self.selected:
            self.selectedValue['text'] = f'{self.selected.data}'
            self.nodeSizeValue['text'] = f'{self.selected.size}'
            self.leftChildrenValue['text'] = f'{self.selected.left.size if self.selected.left else 0}'
            self.rightChildrenValue['text'] = f'{self.selected.right.size if self.selected.right else 0}'
        else:
            self.selectedValue['text'] = 'None'
            self.nodeSizeValue['text'] = '0'
            self.leftChildrenValue['text'] = '0'
            self.rightChildrenValue['text'] = '0'

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
    root = tk.Tk()
    Application(root)
    root.mainloop()