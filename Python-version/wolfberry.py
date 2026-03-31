from plant import Plant

class Wolfberry(Plant):
    def __init__(self, x, y, world, oid=None, s=None, i=None, a=None, m=None):
        super().__init__(x, y, world, oid, str, i, a, m)
        self.color = "cyan"
        self.sign = 'B'
        self.spread_count = 1
        self.spread_chance = 15
        self.str=10
        self.speciesId=9
        self.ini=0
        self.name="Wolfberry"

    def MakeNewP(self,x,y):
        return Wolfberry(x,y,self.world)

