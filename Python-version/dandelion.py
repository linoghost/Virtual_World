from plant import Plant

class Dandelion(Plant):
    def __init__(self, x, y, world, oid=None, s=None, i=None, a=None, m=None):
        super().__init__(x, y, world, oid, str, i, a, m)
        self.color = "yellow"
        self.sign = 'D'
        self.spread_count = 3
        self.spread_chance = 20
        self.str=0
        self.speciesId=8
        self.ini=0
        self.name="Dandelion"

    def MakeNewP(self,x,y):
        return Dandelion(x,y,self.world)