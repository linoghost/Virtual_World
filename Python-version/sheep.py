from animal import Animal

class Sheep(Animal):
    def __init__(self, x, y, world, oid=None, s=None, i=None, a=None, m=None):
        super().__init__(x,y,world,oid,str,i,a,m)
        self.sign='S'
        self.name="Sheep"
        self.color="white"
        self.str=4
        self.ini=4
        self.speciesId=1
    def MakeNewA(self,x,y):
        return Sheep(x,y,self.world)


