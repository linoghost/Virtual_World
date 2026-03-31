from abc import ABC, abstractmethod


class Organism:
    def __init__(self, x, y, world, oid=None, s=None, i=None, a=None, m=None):
        #te inne argumenty są do loadowania mapki
        self.xPos = x
        self.yPos = y
        self.world = world
        self.str = s
        self.ini = i
        self.age = 0
        self.oId = oid
        self.moved = False
        self.speciesId=0
        self.log=" "
        self.name=" "
        self.color=""#tu sb cos n bedzie zgadzac
        self.sign=""


    @abstractmethod
    def Win(self,othercreature):
        pass
    @abstractmethod
    def Defended(self,attackingcreature):
        pass
    @abstractmethod
    def TakeAction(self):
        pass
    @abstractmethod
    def print(self):
        pass

    def GetS(self):
        return self.str

    def SetS(self, strength):
        self.str=strength

    def GetI(self):
        return self.ini

    def GetX(self):
        return self.xPos

    def GetY(self):
        return self.yPos

    def GetSId(self):
        return self.speciesId

    def GetOId(self):
        return self.oId

    def SetOId(self, oid):
        self.oId=oid

    def GetAge(self):
        return self.age

    def SetAge(self, a):
        self.age=a

    def HasMoved(self):
        return self.moved

    def SetHasMoved(self, m):
        self.moved=m

    def GetLog(self):
        return self.log

    def ResetLog(self):
        self.log=" "

    def GetName(self):
        return self.name






