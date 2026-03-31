import tkinter as tk
from tkinter import font
from tkinter import scrolledtext
from tkinter import simpledialog
import random
from imports import *


class World:

    def __init__(self, root, height, width):
        self.height = height
        self.width = width
        self.organisms = []
        self.organismCount = 0

        self.player = None
        self.root = root
        self.log_area = tk.Text(root, height=10, width=50)
        self.logcount = 0
        self.SpawnSign = None  # Initialize SpawnSign

        self.buttons = [[None for _ in range(width)] for _ in range(height)]
        self.logs = ["" for _ in range(height * width * 2)]

        self.root.title("Virtual World")
        self.root.geometry("800x800")
        self.root.configure(bg='#323232')

        self.textfield = tk.Label(root, text="Virtual World", bg='#e1e1e1', fg='black', font=("Arial", 40),
                                  anchor="center")
        self.textfield.pack(fill='x')

        self.command_panel = tk.Frame(root, bg='#969696')
        self.command_panel.pack(side='bottom', fill='x')

        self.cbuttons = [tk.Button(root) for _ in range(4)]
        self.addbuttons = [tk.Button(root) for _ in range(10)]
        # self.cbuttons = []
        command_texts = ["end turn", "special", "save", "load"]
        for text in command_texts:
            btn = tk.Button(self.command_panel, text=text, font=("Arial", 10),
                            command=lambda t=text: self.button_action(t))
            btn.pack(side='left', expand=True, fill='both')
            self.cbuttons.append(btn)

        self.add_panel = tk.Frame(root, bg='#969696')
        self.add_panel.pack(side='right', fill='y')

        # self.addbuttons = []
        addbutton_data = [("S", "white"), ("W", "#d3d3d3"), ("F", "orange"), ("T", "blue"),
                          ("A", "red"), ("G", "green"), ("D", "yellow"), ("B", "cyan"),
                          ("U", "gray"), ("H", "#a9a9a9")]
        for text, color in addbutton_data:
            btn = tk.Button(self.add_panel, text=text, font=("Arial", 10),
                            command=lambda t=text: self.add_button_action(t))
            btn.configure(bg=color)
            btn.pack(fill='both')
            self.addbuttons.append(btn)

        self.button_panel = tk.Frame(root, bg='#969696')
        self.button_panel.pack(expand=True, fill='both')

        self.buttons = [[None for _ in range(width)] for _ in range(height)]
        for i in range(height):
            for j in range(width):
                btn = tk.Button(self.button_panel, font=("Arial", 9, 'bold'),
                                command=lambda r=i, c=j: self.grid_button_action(r, c))
                btn.grid(row=i, column=j, sticky='nsew')
                self.buttons[i][j] = btn

        for i in range(height):
            self.button_panel.grid_rowconfigure(i, weight=1)
        for j in range(width):
            self.button_panel.grid_columnconfigure(j, weight=1)

    def grid_button_action(self, r, c):
        if isinstance(self.buttons[r][c], tk.Button) and self.buttons[r][c].cget(
                'text') == "" and self.SpawnSign is not None:
            self.PCommand(r, c, self.SpawnSign)

    def add_button_action(self, text):
        self.SpawnSign = text

    def button_action(self, text):
        if text == "end turn":
            self.ResolveTurn()
        elif text == "special":
            if self.player is not None and not self.player.moved and self.player.GetCd() == 0:
                self.player.SetCd(10)
                self.player.SetP(5)
                self.Print()
        elif text == "save":
            try:
                self.Save()
            except IOError as ex:
                raise RuntimeError(ex)
        elif text == "load":
            try:
                self.Load()
            except FileNotFoundError as ex:
                raise RuntimeError(ex)

    def set_map(self, x, y, sign, color):
        self.button = self.buttons[y][x]

    def getH(self):
        return self.height

    def getW(self):
        return self.width

    def setH(self, height):
        self.height = height

    def setW(self, width):
        self.width = width

    def addlog(self, log):
        self.logs[self.logcount] = log
        self.logcount += 1

    def AddOrganism(self, newOrganism):
        if newOrganism is not None:
            self.organisms.append(newOrganism)
            newOrganism.SetOId(self.organismCount)
            self.organismCount += 1

    def RmOrganism(self, id):
        if (self.player == self.organisms[id]):
            self.player = None
        tmp = self.organisms[id]  # do sprawdzenia czy potrzebne na 100%
        self.organisms[id] = None

    def actionPerformed(self, text):
        if text == "end turn":
            self.ResolveTurn()
        elif text == "special":
            if self.player is not None and not self.player.moved and self.player.GetCd() == 0:
                # jak n jestesmy dead ani sie nie ruszylismy (umiejetnosc uruchamiana przed ruchem)
                # i jesli mamy cooldown =0
                self.player.SetCd(10)
                self.player.SetP(5)
                self.Print()
        elif text == "save":
            try:
                self.Save()
            except IOError as ex:
                raise RuntimeError(ex)
        elif text == "load":
            try:
                self.Load()
            except FileNotFoundError as ex:
                raise RuntimeError(ex)

    def key_released(self, event):
        key = event.keysym.lower()
        # zeby np jak user ma caps locka wlaczonego to nadal na
        # spokojnie obslugiwalo jako ten sam przycisk

        if key in ('w', 'up'):
            self.command = 'w'
            self.ResolveTurn()
        elif key in ('d', 'right'):
            self.command = 'd'
            self.ResolveTurn()
        elif key in ('s', 'down'):
            self.command = 's'
            self.ResolveTurn()
        elif key in ('a', 'left'):
            self.command = 'a'
            self.ResolveTurn()
        elif key == 'q' and self.player is not None and self.player.GetP() > 0:
            self.command = 'q'
            self.ResolveTurn()
        elif key == 'e' and self.player is not None and self.player.GetP() > 0:
            self.command = 'e'
            self.ResolveTurn()
        elif key == 'z' and self.player is not None and self.player.GetP() > 0:
            self.command = 'z'
            self.ResolveTurn()
        elif key == 'c' and self.player is not None and self.player.GetP() > 0:
            self.command = 'c'
            self.ResolveTurn()
        elif key == 'f' and self.player is not None and not self.player.moved and self.player.GetCd() == 0:
            self.player.SetCd(10)
            self.player.SetP(5)
            self.Print()
        elif key == 't':
            self.ResolveTurn()

    def StartGame(self):
        toBeAdded = 1 + (self.height + self.width // 60)
        rand = random.Random()
        # for i in range(toBeAdded):
        for j in range(15):
            while (True):
                rX = rand.randint(0, self.width - 1)
                rY = rand.randint(0, self.height - 1)
                if self.LookForCollision(rX, rY) == None:
                    self.organisms[self.organismCount] = Sheep(rX, rY, self)
                self.organismCount += 1

    def sort(self):
        tmp = self.organismCount
        for i in range(tmp):
            if self.organisms[i] == None:
                for j in range(tmp - 1, i, -1):
                    if self.organisms[j] != None:
                        self.organisms[i] = self.organisms[j]
                        self.organisms[j] = None
                        break
        tmp = 0
        while (self.organisms[tmp] != None):
            tmp += 1
        self.organismCount = tmp

        for i in range(self.organismCount - 1, 0, -1):
            for j in range(self.organismCount - 1, self.organismCount - 1 - i, -1):
                if self.organisms[j].GetI() > self.organisms[j - 1].GetI():
                    swaptmp = self.organisms[j]
                    self.organisms[j] = self.organisms[j - 1]
                    self.organisms[j - 1] = swaptmp

                elif self.organisms[j].GetI() == self.organisms[j - 1].GetI():
                    if self.organisms[j].GetAge() > self.organisms[j - 1].GetAge():
                        swaptmp = self.organisms[j]
                        self.organisms[j] = self.organisms[j - 1]
                        self.organisms[j - 1] = swaptmp

        for i in range(self.organismCount):
            self.organisms[i].SetOid(i)  # nadanie nowego organism id

    def LookForCollision(self, x, y):
        for i in range(self.organismCount):
            if self.organisms[i] != None:
                if self.organisms[i].GetX() == x and self.organisms[i].GetY() == y:
                    return self.organisms[i]
        return None

    def ResolveTurn(self):
        for i in range(self.logcount):
            self.logs[i] = ""
        self.logcount = 0
        for i in range(self.organismCount):
            if self.organisms[i] != None and not self.organisms[i].HasMoved():
                # dodac playera
                self.organisms[i].TakeAction()
        self.sort()
        for i in range(self.organismCount):
            if self.organisms[i].GetAge() == 0:
                self.organisms[i].SetAge(1)
            self.organisms[i].SetHasMoved(False)
            self.Print()

        log_frame = tk.Toplevel()
        log_frame.title("logs")
        log_area = scrolledtext.ScrolledText(log_frame)
        log_area.pack(fill='both', expand=True)
        log_frame.focus_force()

        log_frame.after(100, lambda: log_frame.destroy())

    def Save(self):
        name = simpledialog.askstring("Save File", "Please enter the name for the save file:")
        if name:
            with open(name, 'w') as file:
                file.write(f"{self.width} {self.height}\n")
        count = 0

        for i in range(self.organismCount):
            if self.organisms[i] != None:
                count += 1
        file.write(f"{count}\n")
        for i in range(self.organismCount):
            if self.organisms[i] != None:
                file.write(
                    f"{self.organisms[i].GetSId()} {self.organisms[i].GetS()} {self.organisms[i].GetI()} {self.organisms[i].GetX()} {self.organisms[i].GetY} {self.organisms[i].GetAge()} {self.organisms[i].GetOId()}\n")

    def Load(self):
        name = simpledialog.askstring("Load File", "Please enter the name of the savefile to load:")
        if name is None:
            return

        with open(name, 'r') as file:

            self.width, self.height = map(int, file.readline().split())

            self.organisms = []
            self.map = []

            self.organismCount = int(file.readline().strip())

            for i in range(self.organismCount):
                species, str_, ini, x, y, age, oId, moved = map(int, file.readline().split())
                moved = bool(moved)
                if species == 1:
                    self.organisms[i] = Sheep(str_, ini, x, y, age, oId, moved, self)

        self.Print()

    def Print(self):
        for i in range(self.width):
            for j in range(self.height):
                self.buttons[j][i].config(bg='#969696', text='')

        for i in range(self.organismCount):
            if self.organisms[i] is not None:
                self.organisms[i].Print()

        # if self.player is not None:
        #     if self.player.GetP() > 0:
        #         self.cbuttons[1].config(text="active " + str(self.player.GetP()))
        #     elif self.player.GetCd() > 0:
        #         self.cbuttons[1].config(text="cooldown " + str(self.player.GetCd()))
        #     else:
        #         self.cbuttons[1].config(text="special")
        # else:
        #     self.cbuttons[1].config(text="")

        for i in range(self.logcount):
            if self.logs[i] != "":
                self.log_area.insert(tk.END, self.logs[i])

    def PCommand(self,x,y,s):
        self.Print()
        if s=="S":
            self.organisms[self.organismCount]=Sheep(x,y,self)