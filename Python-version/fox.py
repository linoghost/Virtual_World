from animal import Animal
import random

class Fox(Animal):
    def __init__(self, x, y, world, oid=None, s=None, i=None, a=None, m=None):
        super().__init__(x, y, world, oid, str, i, a, m)
        self.sign = 'F'
        self.name = "Fox"
        self.color = "orange"
        self.str = 3
        self.ini = 7
        self.speciesId = 3

    def MakeNewA(self, x, y):
        return Fox(x, y, self.world)

    def TakeAction(self):
        if self.age!=-1 and not self.moved:
            changeX = 0
            changeY = 0
            triedLeft = False
            triedRight = False
            triedUp = False
            triedDown = False

            while True:
                changeX = 0
                changeY = 0
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
                if self.xPos+changeX<self.world.GetW() and self.yPos+changeY<self.world.GetH() and self.xPos+ changeX>=0 and self.yPos+changeY>=0:
                    potential_collision = self.world.LookForCollision(self.xPos + changeX, self.yPos + changeY)
                    tmpx = self.xPos + changeX
                    tmpy = self.yPos + changeY
                    if potential_collision is not None:
                        if potential_collision.GetS()<=self.str:
                            self.Collision(potential_collision)

                            if self.age != -1:
                                potential_collision = self.world.LookForCollision(self.xPos + changeX, self.yPos + changeY)
                                if potential_collision is None:

                                    print(f"{self.name} moved from tile ({self.xPos}, {self.yPos}) to tile ({tmpx}, {tmpy})")
                                    self.log = f"{self.name} moved from tile ({self.xPos}, {self.yPos}) to tile ({tmpx}, {tmpy})"
                                    self.xPos += changeX
                                    self.yPos += changeY
                                    break
                    else:
                        print(f"{self.name} moved from tile ({self.xPos}, {self.yPos}) to tile ({tmpx}, {tmpy})")
                        self.log = f"{self.name} moved from tile ({self.xPos}, {self.yPos}) to tile ({tmpx}, {tmpy})"
                        self.xPos += changeX
                        self.yPos += changeY
                        break
                else:
                    changeX = 0
                    changeY = 0
                if triedDown and triedRight and triedUp and triedLeft:
                    print(f"{self.name} from tile ({self.xPos}, {self.yPos}) has nowhere safe to go!")
                    break
            self.moved=True
            if self.age > 0:
                self.age += 1


