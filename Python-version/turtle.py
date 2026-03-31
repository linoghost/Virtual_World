from animal import Animal
import random

class Turtle(Animal):
    def __init__(self, x, y, world, oid=None, s=None, i=None, a=None, m=None):
        super().__init__(x, y, world, oid, str, i, a, m)
        self.sign = 'T'
        self.name = "Turtle"
        self.color = "blue"
        self.str = 2
        self.ini = 1
        self.speciesId = 4
        self.deflected=False

    def MakeNewA(self, x, y):
        return Turtle(x, y, self.world)

    def TakeAction(self):
        if self.age != -1 and not self.moved:
            changex=0
            changey=0
            rand=random.Random()
            rnum=rand.randint(0,99)
            if rnum<25:

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

            else:
                print(f" {self.name} from tile ({self.xPos}, {self.yPos}) stayed in place")

        self.moved=True
        self.world.AddLog(self.log)
        self.log=" "
        if self.age>0:
            self.age+=1

    def Win(self,othercreature):
        if self.deflected:
            print(f" and {self.name} won! {othercreature.GetName()} was pushed back")
            self.deflected=False
        else:
            print(f" and {self.name} won! {othercreature.GetName()} was eaten")
            self.world.RmOrganism(othercreature.GetOId())
            self.world.AddLog(othercreature.GetLog())
            othercreature.ResetLog()
            othercreature.SetAge(-1)

    def Defended(self,attackingcreature):
        if attackingcreature.GetS()<5:
            self.deflected=True
            return True
        return False
