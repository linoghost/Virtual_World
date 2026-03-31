from animal import Animal
import random

class Cybersheep(Animal):
    def __init__(self, x, y, world, oid=None, s=None, i=None, a=None, m=None):
        super().__init__(x,y,world,oid,str,i,a,m)
        self.sign='C'
        self.name="Cybersheep"
        self.color="#5151A4"
        self.str=11
        self.ini=4
        self.speciesId=12
    def MakeNewA(self,x,y):
        return Cybersheep(x,y,self.world)

    def TakeAction(self):
        if self.age != -1 and not self.moved:
            changex = 0
            changey = 0
            rand = random.Random()
            moves_to_hogweed=self.world.GetH()*self.world.GetW()+1
            tmp_moves=0
            hogweed_copy=None
            for i in range(self.world.organismCount):
                if self.world.organisms[i]!=None and self.world.organisms[i].GetName()=="Hogweed":
                    tmp_moves+=abs(self.xPos-self.world.organisms[i].GetX())
                    tmp_moves += abs(self.yPos - self.world.organisms[i].GetY())
                    if moves_to_hogweed>tmp_moves:
                        hogweed_copy=self.world.organisms[i]
                        moves_to_hogweed=tmp_moves
                    tmp_moves=0
            if hogweed_copy!=None:
                #jak x jest wieksze niz nasze to idziemy na prawo
                #jak y jest wieksze niz nasze to idziemy na dol


                while(True):
                    rnum=rand.randint(0,1)
                    if rnum==0:
                        if hogweed_copy.GetX() > self.xPos:
                            changex+=1
                        else:
                            changex-=1
                    else:
                        if hogweed_copy.GetY() > self.xPos:
                            changey+=1
                        else:
                            changey-=1
                    if self.xPos + changex < self.world.GetW() and self.yPos + changey < self.world.GetH() and self.xPos + changex >= 0 and self.yPos + changey >= 0:
                        break
                    else:
                        changex = 0
                        changey = 0
            else:
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

            if self.age > 0:
                self.age += 1

    def Defended(self,attackingcreature):
        if(attackingcreature.GetSId()==11):#jesli human
            if attackingcreature.Defended(self):
                return False
        if(self.str>attackingcreature.GetS() or attackingcreature.GetSId()==10):#jak mamy hogweed to się nadal "defendniemy"
            return True
        return False

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
            if defendingCreature.GetName()=="Hogweed":
                self.Win(defendingCreature)
            elif defendingCreature.Defended(self):
                defendingCreature.Win(self)
            else:
                self.Win(defendingCreature)