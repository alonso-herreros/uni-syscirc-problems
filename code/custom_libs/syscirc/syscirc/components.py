from sympy import re

class Component:
    def __init__(self, type:str, parameter:float, ω:float=0, name:str=None):
        self.type = type
        self.parameter = parameter
        self.ω = ω
        self.name = name or f"{type}{parameter}"

    @property
    def V(self): return self.V if self.V!=None else self.I*self.Z if self.I!=None else None
    @V.setter
    def V(self, V): self.V = V
    @property
    def v(self): return re(self.V)

    @property
    def I(self): return self.I if self.I!=None else self.V/self.Z if self.V!=None else None
    @I.setter
    def I(self, I): self.I = I
    @property
    def i(self): return re(self.I)


class Resistor(Component):
    def __init__(self, R:float, name:str=None):
        super().__init__("R", R, name=name)

    @property
    def Z(self): return Resistor.Z(self.parameter)
    @staticmethod
    def Z(R): return R


class Inductor(Component):
    def __init__(self, L:float, ω:float=0, name:str=None):
        super().__init__("L", L, ω, name=name)

    @property
    def Z(self): return Inductor.Z(self.parameter, self.ω)
    @staticmethod
    def Z(L, ω): return 1j*L*ω


class Capacitor(Component):
    def __init__(self, C:float, ω:float=0, name:str=None):
        super().__init__("C", C, ω, name=name)

    @property
    def Z(self): return Capacitor.Z(self.parameter, self.ω)
    @staticmethod
    def Z(C, ω): return -1j/(C*ω)