from plant import Plant

class Guarana(Plant):
    def __init__(self, x, y, world, oid=None, s=None, i=None, a=None, m=None):
        super().__init__(x, y, world, oid, str, i, a, m)
        self.color = "gray"
        self.sign = 'U'
        self.spread_count = 1
        self.spread_chance = 25
        self.str=0
        self.speciesId=7
        self.ini=0
        self.name="Guarana"

    def MakeNewP(self,x,y):
        return Guarana(x,y,self.world)

    def Defended(self,attackingcreature):
        new_strength=attackingcreature.GetS()+3
        attackingcreature.SetS(new_strength)
        print(f", which is granting strength upon being eaten")
        if self.str>attackingcreature.GetS():
            return True
        return False