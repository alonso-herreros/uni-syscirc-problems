from sympy import re, Abs
from .symbolics import Known

class Component:
    def __init__(self, param=1, freq=0, name:str=None, V=None, I=None):
        self.param = param
        self.freq = freq
        self.name = name or f"{self.__class__.__name__}{id(self)}"
        self._V = self._I = self._Z = None
        self.V = V
        self.I = I
        
    def __repr__(self):
        return f"{self.name} = {self.param}"
    def __str__(self):
        return self.__repr__()
        
    @property
    def Z(self):
        return Known(f"Z_{self.name}", self.Z_calc(self.param, self.freq))

    @property
    def V(self):
        if self._V == None: V_ = self._I*self.Z if self._I!=None else None
        else: V_ = self._V
        return Known(f"V_{self.name}", V_)
    @V.setter
    def V(self, V_):
        if self._I!=None:
            raise Exception("Cannot specify both V and I")
        self._V = V_
    @property
    def v(self): return re(self.V)
    @property
    def vp(self): return Abs(self.V)**2

    @property
    def I(self):
        if self._I == None: I_ = self._V/self.Z if self._V!=None else None
        else: I_ = self._I
        return Known(f"I_{self.name}", I_)
    @I.setter
    def I(self, I_):
        if self._V!=None:
            raise Exception("Cannot specify both V and I")
        self._I = I_
    @property
    def i(self): return re(self.I)
    @property
    def ip(self): return Abs(self.I)**2


class Resistor(Component):
    def __init__(self, R, name:str=None, V:float=None, I:float=None):
        super().__init__(param=R, freq=0, name=name, V=V, I=I)

    @staticmethod
    def Z_calc(R, freq=0): return R


class Inductor(Component):
    def __init__(self, L, freq=0, name:str=None, V:float=None, I:float=None):
        super().__init__(param=L, freq=freq, name=name, V=V, I=I)

    @staticmethod
    def Z_calc(L, freq): return 1j*L*freq


class Capacitor(Component):
    def __init__(self, C:float, freq=0, name:str=None, V:float=None, I:float=None):
        super().__init__(param=C, freq=freq, name=name, V=V, I=I)

    @staticmethod
    def Z_calc(C, freq): return -1j/(C*freq)