from organism import Organism
from plant import Plant

class Grass(Plant):
    def __init__(self, x, y, world, oid=None, s=None, i=None, a=None, m=None):
        super().__init__(x, y, world, oid, str, i, a, m)
        self.color = "green"
        self.sign = 'G'
        self.spread_count = 1
        self.spread_chance = 35
        self.str=0
        self.speciesId=6
        self.ini=0
        self.name="Grass"

    def MakeNewP(self,x,y):
        return Grass(x,y,self.world)