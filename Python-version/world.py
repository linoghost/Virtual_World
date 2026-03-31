import tkinter as tk
from tkinter import font
from tkinter import scrolledtext
from tkinter import simpledialog
import random
from imports import *  # what


class World:

    def __init__(self, root, width=20, height=20):
        self.width = width
        self.height = height
        self.max_size = height * width
        self.organisms = [None] * self.max_size
        self.organismCount = 0

        self.command=''
        self.player = None
        self.root = root
        self.root.bind('<KeyRelease>', self.key_released)
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

        self.cbuttons = []
        command_texts = ["end turn", "special", "save", "load"]
        for text in command_texts:
            btn = tk.Button(self.command_panel, text=text, font=("Arial", 10),
                            command=lambda t=text: self.actionPerformed(t))
            btn.pack(side='left', expand=True, fill='both')
            self.cbuttons.append(btn)

        self.add_panel = tk.Frame(root, bg='#969696')
        self.add_panel.pack(side='right', fill='y')

        self.addbuttons = []
        addbutton_data = [("S", "white"), ("W", "#d3d3d3"), ("F", "orange"), ("T", "blue"),
                          ("A", "red"), ("G", "green"), ("D", "yellow"), ("B", "cyan"),
                          ("U", "gray"), ("H", "#a9a9a9"), ("C", "#5151A4")]
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

        self.StartGame()

    def grid_button_action(self, r, c):
        if isinstance(self.buttons[r][c], tk.Button) and self.buttons[r][c].cget(
                'text') == "" and self.SpawnSign is not None:
            self.PCommand(c, r, self.SpawnSign)

    def add_button_action(self, text):
        self.SpawnSign = text

    def SetMap(self, x, y, sign, color):
        self.buttons[y][x].config(bg=color, text=sign)

    def GetH(self):
        return self.height

    def GetW(self):
        return self.width

    def SetH(self, height):
        self.height = height

    def SetW(self, width):
        self.width = width

    def AddLog(self, log):
        self.logs[self.logcount] = log
        self.logcount += 1

    def AddOrganism(self, newOrganism):
        if newOrganism is not None:
            self.organisms[self.organismCount]=newOrganism
            newOrganism.SetOId(self.organismCount)
            self.organismCount += 1

    def RmOrganism(self, id):
        if self.player!=None and id==self.player.GetOId():
            self.player=None
            print(f"You died.")
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
                self.print()
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
        elif key == 'f' and self.player is not None and self.player.GetCd() == 0:
            #print(f"chuj!")
            self.player.SetCd(10)
            self.player.SetP(5)
            self.print()
        elif key == 't':
            self.ResolveTurn()

    def StartGame(self):

        self.player=Human(self.width//2,self.height//2,self,0)
        self.AddOrganism(self.player)
        toadd=(self.height*self.width//100)
        rand = random.Random()
        for i in range(toadd):
            for j in range(17):
                while (True):
                    rX = rand.randint(0, self.width - 1)
                    rY = rand.randint(0, self.height - 1)
                    if self.LookForCollision(rX, rY) == None:
                        if j<2:
                            self.organisms[self.organismCount]=Sheep(rX, rY, self, self.organismCount)
                        elif j<4:
                            self.organisms[self.organismCount] = Wolf(rX, rY, self, self.organismCount)
                        elif j < 6:
                            self.organisms[self.organismCount] = Fox(rX, rY, self, self.organismCount)
                        elif j<8:
                            self.organisms[self.organismCount] = Turtle(rX, rY, self, self.organismCount)
                        elif j<10:
                            self.organisms[self.organismCount] = Grass(rX, rY, self,self.organismCount)
                        elif j<11:
                            self.organisms[self.organismCount] = Antylope(rX, rY, self, self.organismCount)
                        elif j<12:
                            self.organisms[self.organismCount] = Guarana(rX, rY, self, self.organismCount)
                        elif j<13:
                            self.organisms[self.organismCount] = Dandelion(rX, rY, self, self.organismCount)
                        elif j<14:
                            self.organisms[self.organismCount] = Wolfberry(rX, rY, self, self.organismCount)
                        elif j<15:
                            self.organisms[self.organismCount] = Hogweed(rX, rY, self,self.organismCount)
                        else:
                            self.organisms[self.organismCount] = Cybersheep(rX, rY, self, self.organismCount)

                        self.organismCount += 1
                    break
        self.print()
        self.sort()
        self.ResolveTurn()

    def sort(self):
        tmp = self.organismCount
        for i in range(tmp):
            if self.organisms[i] is None:
                for i2 in range(tmp - 1, i, -1):
                    if self.organisms[i2] is not None:
                        self.organisms[i] = self.organisms[i2]
                        self.organisms[i2] = None
                        break

        tmp = 0
        while tmp < len(self.organisms) and self.organisms[tmp] is not None:
            tmp += 1
        self.organismCount = tmp

        for i in range(self.organismCount - 1, 0, -1):
            for i2 in range(self.organismCount - 1, self.organismCount - 1 - i, -1):
                if self.organisms[i2].GetI() > self.organisms[i2 - 1].GetI():
                    swapTmp = self.organisms[i2]
                    self.organisms[i2] = self.organisms[i2 - 1]
                    self.organisms[i2 - 1] = swapTmp
                elif self.organisms[i2].GetI() == self.organisms[i2 - 1].GetI():
                    if self.organisms[i2].GetAge() > self.organisms[i2 - 1].GetAge():
                        swapTmp = self.organisms[i2]
                        self.organisms[i2] = self.organisms[i2 - 1]
                        self.organisms[i2 - 1] = swapTmp

        for i in range(self.organismCount):
            self.organisms[i].SetOId(i)

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
                if self.player!=None and i==self.player.GetOId():
                    self.player.SetAction(self.command)
                    self.player.TakeAction()
                else:
                    self.organisms[i].TakeAction()

        self.sort()
        for i in range(self.organismCount):
            if self.organisms[i].GetAge() == 0:
                self.organisms[i].SetAge(1)
            self.organisms[i].SetHasMoved(False)
            self.print()

        log_frame = tk.Toplevel()
        log_frame.title("logs")
        log_area = scrolledtext.ScrolledText(log_frame)
        log_area.pack(fill='both', expand=True)
        log_frame.focus_force()

        log_frame.after(100, lambda: log_frame.destroy())

    def Save(self):
        name = simpledialog.askstring("Save File", "Please enter the name for the save file:")

        with open(name, 'w') as file:
            file.write(f"{self.width} {self.height}\n")
            count = 0

            for i in range(self.organismCount):
                if self.organisms[i] != None:
                    count += 1
            file.write(f"{self.organismCount}\n")
            for i in range(self.organismCount):
                if self.organisms[i] != None:
                    if self.organisms[i].HasMoved():
                        moved=1
                    else:
                        moved=0
                    file.write(f"{self.organisms[i].GetSId()} {self.organisms[i].GetS()} {self.organisms[i].GetI()} {self.organisms[i].GetX()} {self.organisms[i].GetY()} {self.organisms[i].GetAge()} {self.organisms[i].GetOId()} {moved}\n")
            if self.player!=None:
                file.write(f"{self.player.GetCd()} {self.player.GetP()}")

    def Load(self):
        name = simpledialog.askstring("Load File", "Please enter the name of the savefile to load:")
        if name is None:
            return

        with open(name, 'r') as file:

            self.width, self.height = map(int, file.readline().split())

            self.organisms = [None] * self.max_size
            self.map = []
            #print(f"{self.organismCount}")
            self.organismCount = int(file.readline().strip())
           # print(f"{self.organismCount}")
            for i in range(self.organismCount):
                species, str, ini, x, y, age, oId, moved = map(int, file.readline().split())
                moved = bool(moved)
                if species == 1:
                    self.organisms[i] = Sheep(x,y,self,oId,str, ini, age,  moved)
                elif species==2:
                    self.organisms[i] = Wolf(x, y, self, oId, str, ini, age, moved)
                elif species==3:
                    self.organisms[i] = Fox(x, y, self, oId, str, ini, age, moved)
                elif species==4:
                    self.organisms[i] = Antylope(x, y, self, oId, str, ini, age, moved)
                elif species==5:
                    self.organisms[i] = Antylope(x, y, self, oId, str, ini, age, moved)
                elif species==6:
                    self.organisms[i] = Grass(x,y,self,oId,str, ini, age,  moved)
                elif species==7:
                    self.organisms[i] = Guarana(x, y, self, oId, str, ini, age, moved)
                elif species==8:
                    self.organisms[i] = Dandelion(x, y, self, oId, str, ini, age, moved)
                elif species==9:
                    self.organisms[i] = Wolfberry(x, y, self, oId, str, ini, age, moved)
                elif species==10:
                    self.organisms[i] = Hogweed(x,y,self,oId,str, ini, age,  moved)
                elif species==12:
                    self.organisms[i] = Cybersheep(x, y, self, oId, str, ini, age, moved)
                else:
                    self.player=Human(x,y,self,oId,str, ini, age,  moved)
                    self.organisms[i] = self.player
            if self.player!=None:
                cd,p=map(int, file.readline().split())
                self.player.SetCd(cd)
                self.player.SetP(p)

        self.print()

    def print(self):
        for i in range(self.width):
            for j in range(self.height):
                self.buttons[j][i].config(bg='#969696', text='')

        for i in range(len(self.organisms)):
            if self.organisms[i] is not None:
                self.organisms[i].print()


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

    def PCommand(self, x, y, s):
        self.print()
        if s == "S":
            self.organisms[self.organismCount] = Sheep(x, y, self,self.organismCount)
            self.SetMap(x,y,'S',"white")
            self.organismCount+=1
        if s=='G':
            self.organisms[self.organismCount] = Grass(x, y, self, self.organismCount)
            self.SetMap(x, y, 'G', "green")
            self.organismCount += 1
        if s=='H':
            self.organisms[self.organismCount] = Hogweed(x, y, self, self.organismCount)
            self.SetMap(x, y, 'H', "#a9a9a9")
            self.organismCount += 1
        if s=='C':
            self.organisms[self.organismCount] = Cybersheep(x, y, self, self.organismCount)
            self.SetMap(x, y, 'C', "#5151A4")
            self.organismCount += 1
        if s=='W':
            self.organisms[self.organismCount] = Wolf(x, y, self, self.organismCount)
            self.SetMap(x, y, 'W', "#d3d3d3")
            self.organismCount += 1
        if s=='F':
            self.organisms[self.organismCount] = Fox(x, y, self, self.organismCount)
            self.SetMap(x, y, 'F', "orange")
            self.organismCount += 1
        if s=='A':
            self.organisms[self.organismCount] = Antylope(x, y, self, self.organismCount)
            self.SetMap(x, y, 'A', "red")
            self.organismCount += 1
        if s=='T':
            self.organisms[self.organismCount] = Turtle(x, y, self, self.organismCount)
            self.SetMap(x, y, 'T', "blue")
            self.organismCount += 1
        if s=='D':
            self.organisms[self.organismCount] = Dandelion(x, y, self, self.organismCount)
            self.SetMap(x, y, 'D', "yellow")
            self.organismCount += 1
        if s=='U':
            self.organisms[self.organismCount] = Guarana(x, y, self, self.organismCount)
            self.SetMap(x, y, 'U', "gray")
            self.organismCount += 1
        if s=='B':
            self.organisms[self.organismCount] = Wolfberry(x, y, self, self.organismCount)
            self.SetMap(x, y, 'B', "cyan")
            self.organismCount += 1



