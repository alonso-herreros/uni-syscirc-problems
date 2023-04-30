from sympy import Symbol, Piecewise
from .symbolics import get_free_symbols, evaluate_on_range


def u(t:float):
    """Unit step function"""
    try:
        return 1 if t>=0 else 0
    except TypeError:
        return Piecewise((1, t>=0), (0, True)).subs(t, t)
    
def delta(t:float):
    """Dirac delta function"""
    try:
        return 1 if t==0 else 0
    except TypeError:
        return Piecewise((1, Symbol("t")==0), (0, True)).subs(Symbol("t"), t)


def equivalent_test(f:callable, g:callable, T:list[float] = [-10, 10], timestep:float=0.5, **kwargs):
    nsamples = int((T[1]-T[0])/timestep + 0.99)
    time = [T[0]+timestep*i for i in range(nsamples)]

    fvals = evaluate_on_range(f, time, **kwargs)
    gvals = evaluate_on_range(g, time, **kwargs)

    try:
        return all(abs(fval-gval) < 1e-10 for fval, gval in zip(fvals, gvals))
    except TypeError as e:
        raise TypeError(f"There may free symbols left in the function: {get_free_symbols(fvals).update(get_free_symbols(gvals))}") from e
