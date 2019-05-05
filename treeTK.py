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
import pickle
import json
import os
from tkinter import filedialog
from tkinter import messagebox


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
        self.filename = 'new tree.bst'
        self.path = None

        # Logic things
        self.tree = bst.BalancedBSTSet(True)
        self.selected = None
        self.__recently = False  # Used to resolve a conflict with double events.

        # ================== The window construction ======================
        self.root = window
        self.root.geometry(f'{width}x{height}')
        self.root.minsize(650, 510)
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.title(f'BSTSet Visualizer')
        self.root.bind('<Control-n>', self.__new)
        self.root.bind('<Control-s>', self.__save, add=True)
        self.root.bind('<Control-Alt-s>', self.__saveAs, add=True)
        self.root.bind('<Control-o>', self.__saveAs, add=True)

        # Menu ------------------------------------------------------------
        menubar = tk.Menu(self.root)

        # +=== File menu ---------------------------------------------------
        fileMenu = tk.Menu(menubar, tearoff=0)
        fileMenu.add_command(label='New', underline=0, accelerator='Ctrl+N', command=self.__new)
        fileMenu.add_command(label='Open...', underline=0, accelerator='Ctrl+O', command=self.__open)
        fileMenu.add_command(label='Save', underline=0, accelerator='Ctrl+S', command=self.__save)
        fileMenu.add_command(label='Save As...', underline=5, accelerator='Ctrl+Alt+S', command=self.__saveAs)
        fileMenu.add_separator()
        fileMenu.add_command(label='Exit', underline=0, accelerator='Alt+F4', command=root.quit)
        menubar.add_cascade(label='File', underline=0, menu=fileMenu)

        # +=== Themes ------------------------------------------------------
        # Loads the json with all the themes
        with open('themes.json') as f:
            themes = json.load(f)

        # Creates a Tk variable to use with the menu radio buttons, holding the current theme name being used.
        self._theme = tk.StringVar()

        # Sets the current theme name to be the first item in the json.
        self._theme.set(tuple(themes.keys())[0])

        # Loads only the colors in that particular theme.
        self._colors = themes[self._theme.get()]

        themeMenu = tk.Menu(menubar, tearoff=0)
        for theme in themes.keys():
            themeMenu.add_radiobutton(label=theme, variable=self._theme, value=theme, command=self.__changeTheme)
        menubar.add_cascade(label='Theme', underline=0, menu=themeMenu)

        # +=== About button menu -----------------------------------------------
        menubar.add_command(label='About', underline=0, command=self.__showAbout)
        self.root.config(menu=menubar)


        # The canvas widget -----------------------------------------------
        self.canvas = tk.Canvas(self.root, bg=themes[self._theme.get()]['bg'])
        self.canvas.bind('<Button-1>', self.__clickHandler)
        self.root.bind('<KeyPress>', self.__navigate, add=True)
        self.canvas.grid(row=0, column=0, sticky='nsew', padx=0, pady=4)

        # The right control panel -------------------------------------------------
        xpad = 4
        panel = ttk.Frame(self.root, width=100, borderwidth=1, relief='solid')
        panel.grid(row=0, column=1, sticky='ns', padx=xpad, pady=6)

        # +=== The config panel ---------------------------------------------------
        configFrame = ttk.LabelFrame(panel, text=' Config ')
        configFrame.pack(fill='x', padx=xpad, pady=4)

        self.autoBalVar = tk.BooleanVar()
        self.autoBalVar.set(True)
        autoBalCB = ttk.Checkbutton(
            configFrame,
            text='Auto balanced',
            variable=self.autoBalVar,
            command=self.__autoBalancedHandler)
        autoBalCB.pack(fill='x', padx=xpad, pady=2)


        # +=== +=== The Alpha config panel -----------------------------------------
        xpad = 2
        alphaFrame = ttk.LabelFrame(configFrame, text=' Alpha ')
        alphaFrame.pack(fill='x', padx=xpad, pady=2, ipady=2)

        topLabel = ttk.Label(alphaFrame, text='Numarator: ')
        topLabel.grid(row=0, column=0, padx=xpad, pady=1, sticky='w')

        bottomLabel = ttk.Label(alphaFrame, text='Denominator: ')
        bottomLabel.grid(row=1, column=0, padx=xpad, pady=1, sticky='w')

        self.topSpin = ttk.Spinbox(
            alphaFrame, command=self.__alphaHandler, width=3, increment=1, from_=1, to=50)
        self.topSpin.bind('<Key>', self.__alphaHandler)
        self.topSpin.set(self.tree.top)
        self.topSpin.grid(row=0, column=1, padx=xpad, pady=1, sticky='e')

        self.bottomSpin = ttk.Spinbox(
            alphaFrame, command=self.__alphaHandler, width=3, increment=1, from_=1, to=50)
        self.bottomSpin.bind('<Key>', self.__alphaHandler)
        self.bottomSpin.set(self.tree.bottom)
        self.bottomSpin.grid(row=1, column=1, padx=xpad, pady=1, sticky='e')

        self.alphaLabel1 = ttk.Label(alphaFrame, text='\u03B1: ')
        self.alphaLabel1.grid(row=2, column=0, padx=xpad, pady=2, sticky='e')

        self.alphaLabelValue = ttk.Label(alphaFrame, text=f'{self.tree.top / self.tree.bottom:.2f}')
        self.alphaLabelValue.grid(row=2, column=1, padx=xpad, pady=2)
        # +=== ------------------------------------------------------------------------------------

        # +=== Quick Action buttons -------------------------------------------------------------
        xpad = 4
        clearBtn = ttk.Button(panel, text='Clear', command=self.clear)
        clearBtn.pack(fill='x', padx=xpad, pady=2)

        rebalanceBtn = ttk.Button(panel, text='Rebalance', command=self.rebalance)
        rebalanceBtn.pack(fill='x', padx=xpad, pady=2)

        randomBtn = ttk.Button(panel, text='Add Random', command=self.addRandom)
        randomBtn.pack(fill='x', padx=xpad, pady=2)


        # +=== Node Action frame -----------------------------------------------------------------
        addRemoveFR = ttk.Frame(panel, borderwidth=1, relief='solid')
        addRemoveFR.pack(fill='x', side='top', padx=xpad, pady=8)

        vcmd = (self.root.register(_isFloatable), '%P')
        self.entry1 = ttk.Entry(
            addRemoveFR,
            justify='center',
            font=('Calibri', 12),
            validate='key', validatecommand=vcmd,
            width=3
        )
        self.entry1.bind('<KeyPress-Return>', self._add_remove)
        self.entry1.grid(row=0, column=1, padx=xpad, pady=4, sticky='we')

        selectBtn = ttk.Button(addRemoveFR, text='Select', width=8, command=self.selectNode)
        selectBtn.grid(row=0, column=0, padx=xpad, pady=4, sticky='ns')
        selectBtn.bind('<ButtonRelease>', self.__returnFocus)

        removeBtn = ttk.Button(addRemoveFR, text='Remove', width=8, command=self.removeNode)
        removeBtn.grid(row=1, column=0, padx=xpad, pady=4, sticky='ns')
        removeBtn.bind('<ButtonRelease>', self.__returnFocus)

        addBtn = ttk.Button(addRemoveFR, text='Add', width=8, command=self.addNode)
        addBtn.grid(row=1, column=1, padx=xpad, pady=4, sticky='ns')
        addBtn.bind('<ButtonRelease>', self.__returnFocus)

        # +=== Tree Info -----------------------------------------------------------------
        treeInfoFrame = ttk.LabelFrame(panel, text='Tree info')
        treeInfoFrame.pack(fill='x', padx=xpad)
        treeInfoFrame.grid_columnconfigure(0, weight=1)

        sizeLabel = ttk.Label(treeInfoFrame, text='Size:', anchor='e')
        sizeLabel.grid(row=0, column=0, padx=xpad, sticky='e')
        self.sizeValueLabel = ttk.Label(treeInfoFrame, text='', width=5)
        self.sizeValueLabel.grid(row=0, column=1, padx=xpad, sticky='e')

        heightLabel = ttk.Label(treeInfoFrame, text='Height:', anchor='e')
        heightLabel.grid(row=1, column=0, padx=xpad, sticky='e')
        self.heightValueLabel = ttk.Label(treeInfoFrame, text='', width=5)
        self.heightValueLabel.grid(row=1, column=1, padx=xpad, sticky='e')

        alphLabel = ttk.Label(treeInfoFrame, text='Alpha:', anchor='e')
        alphLabel.grid(row=3, column=0, padx=xpad, sticky='e')
        self.alphaValueLabel2 = ttk.Label(treeInfoFrame, text='0.67', width=5)
        self.alphaValueLabel2.grid(row=3, column=1, padx=xpad, sticky='e')

        # +=== Node Info -------------------------------------------------------------------
        nodeInfoFrame = ttk.LabelFrame(panel, text='Node info')
        nodeInfoFrame.pack(fill='x', padx=xpad, pady=4)
        nodeInfoFrame.grid_columnconfigure(0, weight=1)

        selectedLabel = ttk.Label(nodeInfoFrame, text='Node:', anchor='e')
        selectedLabel.grid(row=0, column=0, padx=xpad, sticky='e')
        self.selectedValue = ttk.Label(nodeInfoFrame, text='', width=5)
        self.selectedValue.grid(row=0, column=1, padx=xpad, sticky='e')

        nodeSizeLabel = ttk.Label(nodeInfoFrame, text='Size:', anchor='e')
        nodeSizeLabel.grid(row=1, column=0, padx=xpad, sticky='e')
        self.nodeSizeValue = ttk.Label(nodeInfoFrame, text='', width=5)
        self.nodeSizeValue.grid(row=1, column=1, padx=xpad, sticky='e')

        leftChildrenLabel = ttk.Label(nodeInfoFrame, text='Left children:', anchor='e')
        leftChildrenLabel.grid(row=2, column=0, padx=xpad, sticky='e')
        self.leftChildrenValue = ttk.Label(nodeInfoFrame, text='', width=5)
        self.leftChildrenValue.grid(row=2, column=1, padx=xpad, sticky='e')

        rightChildrenLabel = ttk.Label(nodeInfoFrame, text='Right children:', anchor='e')
        rightChildrenLabel.grid(row=3, column=0, padx=xpad, sticky='e')
        self.rightChildrenValue = ttk.Label(nodeInfoFrame, text='', width=5)
        self.rightChildrenValue.grid(row=3, column=1, padx=xpad, sticky='e')

        self.update()
        self.canvas.bind('<Configure>', self.__updateCanvas)


    ## Draws the tree recursivaly.
     #
     # @param curr_node The node from where to start to draw. Usually, you wanna start from the root.
     # @param level Used for the recursion to count each time the function goes down one level.
     # @note Note that all the visual information of the Node in the canvas is stored as the node property.
     #       Things like the x,y position, or the canvas objects Id's.
    def __drawTree(self, currNode, level=1):
        if currNode is None: return

        weight = 1/level
        ratio = weight/self._totalWeight

        baseRadius = self.canvas.winfo_height() / 3
        currNode.r = baseRadius * ratio

        if currNode.parent:
            currNode.y = currNode.parent.y + ratio*self.canvas.winfo_height() * 1.19
        else:
            currNode.y = ratio * self.canvas.winfo_height() / 2


        if currNode.parent is None:
            currNode.x = self.canvas.winfo_width()/2
        elif currNode.data < currNode.parent.data:
            currNode.x = currNode.parent.x - self.canvas.winfo_width() / (2 ** level)
        else:
            currNode.x = currNode.parent.x + self.canvas.winfo_width() / (2 ** level)

        self.__drawNode(currNode)
        self.__drawTree(currNode.left, level + 1)
        self.__drawTree(currNode.right, level + 1)


    ## Draw a Node in the canvas, with the text and the lines to the respective parents.
    def __drawNode(self, node):
        fillColor = self._colors['nodeFill']
        outlineColor = self._colors['nodeOutline']

        if node.counter == 0:
            fillColor = self._colors['leafFill']
            outlineColor = self._colors['leafOutline']

        elif not self.tree.isBalanced(node):
            fillColor = self._colors['uNodeFill']
            outlineColor = self._colors['uNodeOutline']

        outline = 2
        fontSize = int(node.r)
        if node is self.selected:
            node.r *= 1.2
            outline = 3
            fontSize = int(fontSize * 1.2)

        node.circle = self.canvas.create_oval(
            node.x - node.r, node.y - node.r,
            node.x + node.r, node.y + node.r,
            width=outline, fill=fillColor, outline=outlineColor, tags='node'
        )

        if node is self.selected:
            self.canvas.tag_raise(node.circle)

        if node.parent:
            node.line = self.canvas.create_line(
                node.x, node.y,
                node.parent.x,
                node.parent.y,
                width=2, fill=self._colors['nodeOutline']
            )
            self.canvas.tag_lower(node.line)

        node.text = self.canvas.create_text(
            node.x, node.y,
            text=f'{node.data:g}',
            fill=self._colors['text'],
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


    def __navigate(self, event):
        if event.keysym in ('Left', 'Right', 'Up', 'Down'):
            if self.selected is None:
                self.selectNode(self.tree.root())
                return

            if event.keysym == 'Left':
                if self.selected.left:
                    self.selectNode(self.selected.left)
                elif self.selected.parent:
                    if self.selected.parent.right is self.selected:
                        self.selectNode(self.selected.parent)
                return

            elif event.keysym == 'Right':
                if self.selected.right:
                    self.selectNode(self.selected.right)
                elif self.selected.parent:
                    if self.selected.parent.left is self.selected:
                        self.selectNode(self.selected.parent)
                return

            elif event.keysym == 'Up':
                if self.selected.parent:
                    self.selectNode(self.selected.parent)
                return

            elif event.keysym == 'Down':
                if self.selected.left and not self.selected.right:
                    self.selectNode(self.selected.left)
                elif self.selected.right and not self.selected.left:
                    self.selectNode(self.selected.right)
                return

        elif event.keysym == 'Delete':
            self.removeNode(self.selected.data)
        elif event.keysym == 'Insert':
            self.entry1.focus_set()


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
            outline=self._colors['selectedOutline']
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
            self.__markToSave()
            self.update()


    ## Removes the key node from the tree.
     # If no key is passed, then the number in the entry will be used.
    def removeNode(self, key=None):
        if key is None:
            entry = self.entry1.get()
            if entry and entry != '-':
                key = float(entry)
        if key is not '':
            self.tree.remove(key)
            self.entry1.delete(0, 'end')
            self.selected = None
            self.__markToSave()
            self.update()


    ## Add a random number into the tree.
     #
     # If the number choosed is already in the tree, it will try to add a random decimal to this number choosed and fit
     # it in the tree, until it succeed.
    def addRandom(self):
        range_ = 5
        key = r.randint(-range_, range_)
        while self.tree.add(key):
            range_ *= 2
            key = r.randint(-range_, range_)
        self.update()


    ## Clears the tree.
    def clear(self):
        for node in self.tree:
            self.tree.remove(node)
        self.__markToSave()
        self.update()


    ## Rebalances the whole tree.
    def rebalance(self):
        if not self.tree.isEmpty():
            self.tree.rebalance()
            self.__markToSave()
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
        self.alphaLabelValue['text'] = f'{alpha:.2f}'
        if 0.5 < alpha < 1:
            self.alphaLabel1['foreground'] = 'black'
            self.alphaLabelValue['foreground'] = 'black'
            self.alphaValueLabel2['text'] = f'{alpha:.2f}'
            self.tree.top = top
            self.tree.bottom = bottom
            self.__markToSave()
            self.update()
        else:
            self.alphaLabel1['foreground'] = 'red'
            self.alphaLabelValue['foreground'] = 'red'


    ## Marks the title of the window with an asterisk character to tell the user it is not saved.
    def __markToSave(self):
        if self.root.title()[-1] != '*':
            self.root.title(self.root.title() + '*')


    ## Updates everything
    def update(self, *_):
        self.__updateCanvas()

        self.autoBalVar.set(self.tree.selfBalanced)
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


    ## Updates only the canvas
    def __updateCanvas(self, *_):
        self.canvas.delete('all')
        self.canvas['bg'] = self._colors['bg']

        self._totalWeight = 0
        for n in range(1, self.tree.height() + 2):
            self._totalWeight += 1/n

        if self.tree.height() >= 0:
            self.__drawTree(self.tree.root())
        self.canvas.update_idletasks()


    ## Saves the tree in a 'pickled' .bst file.
    def __saveAs(self, *_):
        with filedialog.asksaveasfile(
                mode='wb',
                defaultextension='.bst',
                filetypes=[('Binary Search Tree', '*.bst')],
                initialfile=self.filename
                ) as f:
            pickle.dump(self.tree, f)
            self.root.title(f'[{f.name}] - BSTSet Visualizer')
            self.filename = os.path.basename(f.name)
            self.path = f.name


    # Saves the current file. If the application is not associated to any file, it asks to create one.
    def __save(self, *_):
        if self.path is None: self.__saveAs()
        else:
            with open(self.path, 'wb') as f:
                pickle.dump(self.tree, f)
                self.root.title(f'[{f.name}] - BSTSet Visualizer')


    ## Loads a .bst file
    def __open(self, *_):
        if self.tree.root():
            self.__askSave()

        with filedialog.askopenfile(
                defaultextension='.bst',
                filetypes=[('Binary Search Tree', '*.bst'), ('Any', '*')],
                initialfile='*.bst'
                ) as f:

            try:
                self.tree = pickle.load(f)
            except pickle.UnpicklingError:
                messagebox.showerror('error', 'Fail to open the file')
                return

            self.root.title(f'[{f.name}] - BSTSet Visualizer')
            self.filename = os.path.basename(f.name)
            self.path = f.name
            self.update()


    ## Creates a new tree.
    def __new(self, *_):
        if self.tree.root():
            self.__askSave()

        self.filename = 'new tree.bst'
        self.path = None
        self.tree = bst.BalancedBSTSet(True)
        self.selected = None
        self.root.title(f'BSTSet Visualizer')
        self.update()


    ## Asks to save the file
    def __askSave(self):
        if messagebox.askyesno(message='The current Tree is not saved. Do you wanna save it?'):
            self.__save()


    ## Opens the 'About' window
    def __showAbout(self):
        AboutWindow(self.root)

    def __changeTheme(self):
        with open('themes.json') as f:
            themes = json.load(f)
        self._colors = themes[self._theme.get()]
        self.update()

##
 # The information window about this program.
 #
 # @author Wallace Alves dos Santos
 # @since 05/05/2019
 #
class AboutWindow:
    def __init__(self, parent):
        self.root = tk.Toplevel(padx=20, pady=10)
        self.root.transient(parent)
        self.root.geometry('+500+100')
        self.root.focus_set()
        self.root.bind('<FocusOut>', lambda _: self.root.destroy())

        text1 = ttk.Label(self.root, anchor='center', justify='center', font=('Calibri', 16, 'bold'))
        text1['text'] = "Binary Search Tree Viewer\n"
        text1.pack()

        ttk.Separator(self.root).pack(fill='x')

        text2 = ttk.Label(self.root, anchor='center', justify='center', font=('Calibri', 11))
        text2['text'] = (
            "\nBuilt on May 5, 2019\n"
            "by Wallace Alves dos Santos (AceWall)"
        )
        text2.pack()

        text3 = ttk.Label(self.root, anchor='center', justify='center', text='acewall0@outlook.com\n')
        text3.pack()

        ttk.Separator(self.root).pack(fill='x')

        text4 = ttk.Label(self.root, wraplength=240)
        text4['text'] = (
            "\nThis is a college project of a binary tree "
            "complete with an user interface.\n\n"
            "This is my first 'finished' application ever! "
            "And even though is a pretty simple application, "
            "I tried to let everything pretty polished, and "
            "I hope if you are seeing this, you enjoy it.\n"
        )
        text4.pack()

        ttk.Separator(self.root).pack(fill='x')

        text5 = ttk.Label(self.root, wraplength=240)
        text5['text'] = (
            "\nYou can use it by the panel at the right or "
            "using the directional keys to navigate through "
            "the nodes and the delete or insert key to "
            "remove or delete nodes. You can also left or "
            "right click directly in to the nodes.\n"
        )
        text5.pack()

        closeButton = ttk.Button(self.root, text='Close', command=self.root.destroy)
        closeButton.pack()


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