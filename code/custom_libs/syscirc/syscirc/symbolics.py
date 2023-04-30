from sympy import Symbol, nan

class Known(Symbol):
    def __new__(cls, name, value):
        obj = Symbol.__new__(cls, name)
        obj._value = value
        return obj

    def __init__(self, name:str, value):
        Symbol.__init__(name)
        self._value = value

    @property
    def value(self): return self._value
    @value.setter
    def value(self, value):
        self._value = value
    
    def __repr__(self):
        return f"{self.name} = {self.value}"
    def __str__(self):
        return self.name
    def __float__(self):
        return self.evalf()
    
    def evalf(self):
        return self.update(self.value, -1, True)

    def update(self, expr, levels:int=1, evalf:bool=False):
        return Known.resolve(expr, [self], levels, evalf)
    
    @staticmethod
    def resolve(expr, knowns=[], levels:int=1, evalf:bool=False, exclude=[]):
        knowns = [knowns] if not isinstance(knowns, list) else knowns
        exclude = [exclude] if not isinstance(exclude, list) else exclude
        if evalf:
            try: return float(expr)
            except TypeError: pass

        if levels == 0 or levels < -100:
            return expr

        changed = False
        for s in expr.free_symbols:
            if (knowns and s not in knowns) or (exclude and s in exclude): continue
            try:
                expr = expr.subs(s, s.value)
                changed = s != s.value
            except AttributeError: pass
        return Known.resolve(expr, knowns, changed*(levels-1), evalf)

    
def get_free_symbols(values):
    symbols = set()
    for v in values:
        try: symbols.update(v.free_symbols)
        except (TypeError, AttributeError): pass
    return symbols


def evaluate_on_range(f, time:list[float], var:Symbol=Symbol("t"), **kwargs):
    values = []
    for i in time:
        try: val = f(i)
        except TypeError:
            kwargs.update({var: i})
            val = f.subs(kwargs)
        else: 
            try: val = val.subs(kwargs)
            except (TypeError, AttributeError): pass

        try: val = val.evalf()
        except (TypeError, AttributeError): pass

        values.append(val if val is not None and val != nan else 0)
    return values