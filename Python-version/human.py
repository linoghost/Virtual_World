from animal import Animal

class Human(Animal):
    def __init__(self, x, y, world, oid=0, s=None, i=None, a=None, m=None):
        super().__init__(x, y, world, oid, str, i, a, m)
        self.sign='Y'
        self.name="Human"
        self.color="#FF88FD"
        self.str=5
        self.ini=4
        self.speciesId=11
        self.cooldown=0
        self.power_left=0
        self.action=''
        self.change_x=0
        self.change_y = 0
        self.special_active=False
        self.moved=False

    def MakeNewA(self,x,y):
        return None

    def GetCd(self):
        return self.cooldown

    def SetCd(self,cd):
        self.cooldown=cd

    def GetP(self):
        return self.power_left

    def SetP(self,p):
        self.power_left=p

    def SetAction(self,ac):
        self.action=ac

    def TakeAction(self):

        if self.cooldown==10:
            print(f"Alzur's shield activated")
            self.special_active = True

        if self.action=='w':
            self.change_y-=1
        elif self.action=='s':
            self.change_y+=1
        elif self.action=='a':
            self.change_x-=1
        elif self.action=='d':
            self.change_x+=1

        if self.xPos + self.change_x < self.world.GetW() and self.yPos + self.change_y < self.world.GetH() and self.xPos + self.change_x >= 0 and self.yPos + self.change_y >= 0:
            potential_collision = self.world.LookForCollision(self.xPos + self.change_x, self.yPos + self.change_y)

            if potential_collision is not None:
                self.Collision(potential_collision)

            if self.age != -1:
                potential_collision = self.world.LookForCollision(self.xPos + self.change_x, self.yPos + self.change_y)
                if potential_collision is None:
                    tmpx = self.xPos + self.change_x
                    tmpy = self.yPos + self.change_y
                    print(f"{self.name} moved from tile ({self.xPos}, {self.yPos}) to tile ({tmpx}, {tmpy})")
                    self.log = f"{self.name} moved from tile ({self.xPos}, {self.yPos}) to tile ({tmpx}, {tmpy})"
                    self.xPos += self.change_x
                    self.yPos += self.change_y

            self.moved=True
            self.world.AddLog(self.log)
            self.log = " "
            if self.age > 0:
                self.age += 1
            if self.cooldown>0:
                self.cooldown-=1
            if self.power_left>0:
                self.power_left-=1
            self.change_x=0
            self.change_y=0
            if self.power_left==0:
                self.special_active=False

    def Win(self,othercreature):
        if not self.special_active:#zabezpieczenie, bo jak mamy aktywna tarcze to nie wygramy per se tylko odepchniemy
            print(f" and {self.name} won! {othercreature.GetName()} perished")
            self.world.RmOrganism(othercreature.GetOId())
            othercreature.ResetLog()
            othercreature.SetAge(-1)

    def Defended(self,attackingcreature):
        if self.special_active:
            attackingcreature.TakeAction()
            print(f" and {self.name} won! {attackingcreature.GetName()} was pushed back")
            return True
        if self.str>attackingcreature.GetS():
            return True
        return False

    def print(self):
        self.world.SetMap(self.xPos,self.yPos,self.sign,self.color)