from organism import Organism
from abc import ABC, abstractmethod
import random

class Plant(Organism):
    def __init__(self, x, y, world, oid=None, s=None, i=None, a=None, m=None):
        super().__init__(x, y, world, oid, str, i, a, m)
        self.color="black"

        self.spread_count=1
        self.spread_chance=0

    @abstractmethod
    def MakeNewP(self,x,y):
        pass

    def print(self):
        self.world.SetMap(self.xPos, self.yPos, self.sign, self.color)

    def Win(self,othercreature):
        print(f" and {othercreature.GetName()} died while eating it! Both perished\n")
        self.log = f"{self.log} and {othercreature.GetName()} died while eating it! Both perished\n"
        self.world.RmOrganism(self.GetOId())
        self.world.RmOrganism(othercreature.GetOId())

        self.world.AddLog(othercreature.GetLog())
        self.world.AddLog(self.log)
        othercreature.ResetLog()
        othercreature.SetAge(-1)
        log=" "
        self.age=-1

    def Defended(self,attackingcreature):
        if (self.str > attackingcreature.GetS()):
            return True
        return False

    def TakeAction(self):
        if self.age!=-1 and not self.moved:
            spreads_attempted=0
            while(spreads_attempted!=self.spread_count):#tu moze byc blad bo spreadcount jest tu ustawiony na 0
                rand=random.Random()
                rnum=rand.randint(0,99)
                print(f"{self.name} from tile ({self.xPos}, {self.yPos}) tried spreading ",end="")
                self.log = f"{self.log} {self.name} from tile ({self.xPos}, {self.yPos}) tried spreading"
                if rnum>=(99-self.spread_chance):
                    self.Spread()
                else:
                    print(f", but failed\n")
                    self.log=f"{self.log}, but failed\n"
                spreads_attempted+=1
            self.age+=1

    def Spread(self):
        triedLeft = False
        triedRight = False
        triedUp = False
        triedDown = False
        while (True):
            rand = random.Random()
            changeX = 0
            changeY = 0
            rNum = rand.randint(0, 3)
            if rNum == 0:
                if triedLeft:
                    continue
                else:
                    triedLeft = True
                changeX = -1
            elif rNum == 1:
                if triedRight:
                    continue
                else:
                    triedRight = True
                changeX = 1
            elif rNum == 2:
                if triedUp:
                    continue
                else:
                    triedUp = True
                changeY = -1
            else:
                if triedDown:
                    continue
                else:
                    triedDown = True
                changeY = 1
            if self.xPos + changeX < self.world.GetW() and self.yPos + changeY < self.world.GetH() and self.xPos + changeX >= 0 and self.yPos + changeY >= 0:
                potential_collision = self.world.LookForCollision(self.xPos + changeX, self.yPos + changeY)
                if potential_collision is None:
                    new_plant=self.MakeNewP(self.xPos+changeX,self.yPos+changeY)
                    self.world.AddOrganism(new_plant)
                    tmpx = self.xPos + changeX
                    tmpy = self.yPos + changeY
                    print(f" and spread to tile({tmpx}, {tmpy})\n")
                    break
            if triedDown and triedRight and triedUp and triedLeft:
                print(f", but had no adjacent tiles to spread to\n")
                break


