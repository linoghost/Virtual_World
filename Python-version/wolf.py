from animal import Animal

class Wolf(Animal):
    def __init__(self, x, y, world, oid=None, s=None, i=None, a=None, m=None):
        super().__init__(x, y, world, oid, str, i, a, m)
        self.sign = 'W'
        self.name = "Wolf"
        self.color = "#d3d3d3"
        self.str = 9
        self.ini = 5
        self.speciesId = 2

    def MakeNewA(self, x, y):
        return Wolf(x, y, self.world)