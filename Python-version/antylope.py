from animal import Animal
import random

class Antylope(Animal):
    def __init__(self, x, y, world, oid=None, s=None, i=None, a=None, m=None):
        super().__init__(x, y, world, oid, str, i, a, m)
        self.sign = 'A'
        self.name = "Antylope"
        self.color = "red"
        self.str = 5
        self.ini = 5
        self.speciesId = 5
        self.avoided=False

    def MakeNewA(self, x, y):
        return Antylope(x, y, self.world)

    def Defended(self,attackingcreature):
        if self.str>attackingcreature.GetS():
            return True

        rand=random.Random()
        rnum2=rand.randint(0,1)
        if rnum2==0:
            self.avoided=True
            changex=0
            changey=0
            while True:
                rnum = rand.randint(0, 3)
                if rnum == 0:
                    changex = -1
                elif rnum == 1:
                    changex = 1
                elif rnum == 2:
                    changey = -1
                elif rnum == 3:
                    changey = 1
                if self.xPos + changex < self.world.GetW() and self.yPos + changey < self.world.GetH() and self.xPos + changex >= 0 and self.yPos + changey >= 0:
                    potential_collision = self.world.LookForCollision(self.xPos + changex, self.yPos + changey)
                    if potential_collision is None or (self.xPos+changex==attackingcreature.GetX() and self.yPos+changey==attackingcreature.GetY()):
                        self.xPos+=changex
                        self.yPos+=changey
                        return True
                else:
                    changey = 0
                    changex = 0
        return False

    def Win(self,othercreature):
        if self.avoided:
            print(f" and {self.name} ran away! It went to tile ({self.xPos}, {self.yPos})")
            self.avoided=False
        else:
            print(f" and {self.name} won! {othercreature.GetName()} was eaten")
            self.world.RmOrganism(othercreature.GetOId())
            self.world.AddLog(othercreature.GetLog())
            othercreature.ResetLog()
            othercreature.SetAge(-1)

    def TakeAction(self):
        if self.age!=-1 and not self.moved:
            changex = 0
            changey = 0
            rand = random.Random()

            while (True):
                rnum = rand.randint(0, 3)
                if rnum == 0:
                    changex = -1
                elif rnum == 1:
                    changex = 1
                elif rnum == 2:
                    changey = -1
                elif rnum == 3:
                    changey = 1

                rnum2=rand.randint(0,3)
                if rnum2 == 0:
                    changex += -1
                elif rnum2 == 1:
                    changex += 1
                elif rnum2 == 2:
                    changey += -1
                elif rnum2 == 3:
                    changey += 1

                if self.xPos + changex < self.world.GetW() and self.yPos + changey < self.world.GetH() and self.xPos + changex >= 0 and self.yPos + changey >= 0:
                    break
                else:
                    changey = 0
                    changex = 0

                potential_collision = self.world.LookForCollision(self.xPos + changex, self.yPos + changey)

                if potential_collision is not None:
                    self.Collision(potential_collision)

                if self.age != -1:
                    potential_collision = self.world.LookForCollision(self.xPos + changex, self.yPos + changey)
                    if potential_collision is None:
                        tmpx = self.xPos + changex
                        tmpy = self.yPos + changey
                        print(f"{self.name} moved from tile ({self.xPos}, {self.yPos}) to tile ({tmpx}, {tmpy})")
                        self.xPos += changex
                        self.yPos += changey
                self.moved = True
                self.avoided=False

                if self.age > 0:
                    self.age += 1
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
            if not defendingCreature.Defended(self):
                self.Win(defendingCreature)
            else:
                rand = random.Random()
                rnum3=rand.randint(0,1)
                if rnum3==0:
                    defendingCreature.Win(self)
                else:
                    print(f"{self.name} tries to run away, ")
                    rnum2=rand.randint(0,1)
                    if rnum2==0:
                        changeX = 0
                        changeY = 0
                        triedLeft = False
                        triedRight = False
                        triedUp = False
                        triedDown = False
                        while True:
                            rNum = random.randint(0, 3)

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
                                potential_collision = self.world.LookForCollision(self.xPos + changeX,self.yPos + changeY)
                                if potential_collision is None:
                                    self.avoided=True
                                    break
                            else:
                                changeX = 0
                                changeY = 0
                            if triedDown and triedRight and triedUp and triedLeft:
                                print(f"but has nowhere to run to")
                                break
                    if self.avoided:
                        print(f" and succeds!")
                        self.Win(defendingCreature)
                    else:
                        print(f" and fails!")
                        defendingCreature.Win(self)