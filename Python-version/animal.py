from organism import Organism
from abc import ABC, abstractmethod
import random

class Animal(Organism):
    def __init__(self, x, y, world, oid=None, s=None, i=None, a=None, m=None):
        super().__init__(x,y,world,oid,str,i,a,m)
        self.color="black"

    @abstractmethod
    def MakeNewA(self,x,y):
        pass

    def Win(self,othercreature):
        print(f" and  {self.name}  won! {othercreature.GetName()} was eaten\n")
        self.log = f"{self.log} and {self.name} won! {othercreature.GetName()} was eaten\n"
        self.world.RmOrganism(othercreature.GetOId())
        self.world.AddLog(othercreature.GetLog())
        othercreature.ResetLog()
        othercreature.SetAge(-1)

    def Defended(self,attackingcreature):
        if(attackingcreature.GetSId()==11):#jesli human
            if attackingcreature.Defended(self):
                return False
        if(self.str>attackingcreature.GetS()):
            return True
        return False

    def Procreate(self):
        triedLeft=False
        triedRight = False
        triedUp = False
        triedDown=False
        while(True):
            rand=random.Random()
            changeX=0
            changeY=0
            rNum=rand.randint(0,3)
            if rNum==0:
                if triedLeft:
                    continue
                else:
                    triedLeft=True
                changeX=-1
            elif rNum==1:
                if triedRight:
                    continue
                else:
                    triedRight=True
                changeX=1
            elif rNum==2:
                if triedUp:
                    continue
                else:
                    triedUp=True
                changeY=-1
            else:
                if triedDown:
                    continue
                else:
                    triedDown=True
                changeY=1
            if self.xPos+changeX<self.world.GetW() and self.yPos+changeY<self.world.GetH() and self.xPos+ changeX>=0 and self.yPos+changeY>=0:
                potential_collision = self.world.LookForCollision(self.xPos + changeX, self.yPos + changeY)
                if potential_collision is None:
                    newAnimal=self.MakeNewA(self.xPos+changeX,self.yPos +changeY)
                    self.world.AddOrganism(newAnimal)
                    tmpx=self.xPos+changeX
                    tmpy=self.yPos + changeY
                    print(f" and spawned offspring on tile({tmpx}, {tmpy})\n")
                    break
            if triedDown and triedRight and triedUp and triedLeft:
                print(f", but had no adjacent tiles to spawn offspring to\n")
                break


    def TakeAction(self):
        if self.age != -1 and not self.moved:
            changex=0
            changey=0
            rand=random.Random()

            while(True):
                rnum=rand.randint(0, 3)
                if rnum == 0:
                    changex=-1
                elif rnum == 1:
                    changex=1
                elif rnum == 2:
                    changey=-1
                elif rnum == 3:
                    changey=1
                if self.xPos+changex<self.world.GetW() and self.yPos+changey<self.world.GetH() and self.xPos+ changex>=0 and self.yPos+changey>=0:
                    break
                else:
                    changey=0
                    changex=0


            potential_collision = self.world.LookForCollision(self.xPos + changex, self.yPos + changey)

            if potential_collision is not None:
                self.Collision(potential_collision)

            if self.age != -1:
                potential_collision = self.world.LookForCollision(self.xPos + changex, self.yPos + changey)
                if potential_collision is None:
                    tmpx = self.xPos + changex
                    tmpy = self.yPos + changey
                    print(f"{self.name} moved from tile ({self.xPos}, {self.yPos}) to tile ({tmpx}, {tmpy})")
                    self.log=f"{self.name} moved from tile ({self.xPos}, {self.yPos}) to tile ({tmpx}, {tmpy})"
                    self.xPos+=changex
                    self.yPos+=changey
            self.moved=True

            self.world.AddLog(self.log)
            self.log=" "
            if self.age>0:
                self.age+=1

    def Collision(self,defendingCreature):

        if defendingCreature.GetSId() is self.speciesId:
            print(f"{self.name} from tile ({self.xPos}, {self.yPos}) encountered a mate on tile {defendingCreature.GetX()}, {defendingCreature.GetY()})",end="")
            self.log=f"{self.log} {self.name} from tile ({self.xPos}, {self.yPos}) encountered a mate on tile {defendingCreature.GetX()}, {defendingCreature.GetY()})"
            if defendingCreature.HasMoved():
                print(f", but the mate has already moved this turn\n")
                self.log=f"{self.log}, but the mate has already moved this turn\n "
            else:
                if isinstance(defendingCreature, Animal):
                    self.Procreate()
                    defendingCreatureCast=defendingCreature
                    print(f"{defendingCreatureCast.GetName()} on tile ({defendingCreatureCast.GetX()}, {defendingCreatureCast.GetY()}) tried to ",end="")
                    self.log=f"{self.log} {defendingCreatureCast.GetName()} on tile ({defendingCreatureCast.GetX()}, {defendingCreatureCast.GetY()}) tried to "
                    defendingCreatureCast.Procreate()
                    defendingCreature.SetHasMoved(True)
        else:
            print(f"{self.name} from tile ({self.xPos}, {self.yPos}) encountered a {defendingCreature.GetName()} on tile ({defendingCreature.GetX()}, {defendingCreature.GetY()})",end="")
            self.log=f"{self.log} {self.name} from tile ({self.xPos}, {self.yPos}) encountered a {defendingCreature.GetName()} on tile ({defendingCreature.GetX()}, {defendingCreature.GetY()})"
            if defendingCreature.Defended(self):
                defendingCreature.Win(self)
            else:
                self.Win(defendingCreature)

    def print(self):
        self.world.SetMap(self.xPos,self.yPos,self.sign,self.color)

