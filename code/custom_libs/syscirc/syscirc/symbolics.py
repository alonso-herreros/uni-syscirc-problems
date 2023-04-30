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
    
    def __repr__(self):
        return f"{self.name} = {self.value}"
    def __str__(self):
        return f"{self.name} = {self.value}"
    def __float__(self):
        return float(self.value)
    
    def evalf(self): return self.value

    def update(self, expr):
        return expr.subs(self, self.value)
    
    @staticmethod
    def updateAll(expression):
        for s in expression.free_symbols:
            if isinstance(s, Known):
                expression = s.update(expression)
        return expression

    
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