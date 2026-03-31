from plant import Plant
import random

class Hogweed(Plant):
    def __init__(self, x, y, world, oid=None, s=None, i=None, a=None, m=None):
        super().__init__(x, y, world, oid, str, i, a, m)
        self.color = "#a9a9a9"
        self.sign = 'H'
        self.spread_count = 1
        self.spread_chance = 1
        self.str=99
        self.speciesId=10
        self.ini=0
        self.name="Hogweed"

    def MakeNewP(self,x,y):
        return Hogweed(x,y,self.world)

    def TakeAction(self):
        if self.age>0:#jak n ded
            spreads_attempted = 0
            while (spreads_attempted != self.spread_count):
                rand = random.Random()
                rnum = rand.randint(0, 99)
                print(f"{self.name} from tile ({self.xPos}, {self.yPos}) tried spreading ", end="")
                if rnum >= (99 - self.spread_chance):
                    self.Spread()
                else:
                    print(f", but failed")
                spreads_attempted += 1
            self.age += 1
            print(f"{self.name} from tile ({self.xPos}, {self.yPos}) is killing animals around it!")
            for changex in range(-1,2):
                for changey in range(-1,2):
                    if (changey==0 and changex!=0) or (changey!=0 and changex==0):
                        if self.xPos + changex < self.world.GetW() and self.yPos + changey < self.world.GetH() and self.xPos + changex >= 0 and self.yPos + changey >= 0:
                            potential_collision = self.world.LookForCollision(self.xPos + changex, self.yPos + changey)

                            if potential_collision is not None and potential_collision.GetI()!=0 and potential_collision.GetSId()!=12:#tylko dla zwierzac hence 0 (i 12 dla cyberowcy)

                                tmpx = self.xPos + changex
                                tmpy = self.yPos + changey
                                print(f"{potential_collision.GetName()} from tile ({tmpx}, {tmpy}) perished")
                                self.world.RmOrganism(potential_collision.GetOId())
        self.age+=1



