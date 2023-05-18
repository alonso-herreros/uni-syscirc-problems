from sympy import Symbol, Rel, nan

class Known(Symbol):
    def __new__(cls, name, value=None):
        obj = Symbol.__new__(cls, name)
        obj._value = value or Symbol(name)
        return obj

    def __init__(self, name:str, value=None):
        Symbol.__init__(name)
        self._value = value or Symbol(name)

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
        return Known.resolve(self.value, levels=-1, evalf=True)

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


def op_lr(rel:Rel, func):
    return rel.__class__(func(rel.lhs), func(rel.rhs))


def get_free_symbols(values):
    symbols = set()
    for v in values:
        try: symbols.update(v.free_symbols)
        except (TypeError, AttributeError): pass
    return symbols


def evaluate_on_range(f, time:list[float], var:Symbol=Symbol("t"), **kwargs):
    values = []
    try: f = Known.resolve(f, levels=-1, evalf=True)
    except TypeError: pass
    for i in time:
        try: val = f(i)
        except TypeError:
            kwargs.update({var: i})
            val = f.subs(kwargs)
        else: 
            try: val = val.subs(kwargs)
            except (TypeError, AttributeError): pass

        try: val = float(Known.resolve(val, levels=-1, evalf=True))
        except TypeError as e:
            try: raise TypeError(f"Could not evaluate {val} to float. Symbols left: {val.free_symbols}.") from e
            except TypeError: raise TypeError(f"Could not evaluate {val} to float.") from e


        values.append(val if val is not None and val != nan else 0)
    return values