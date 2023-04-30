from matplotlib import pyplot as plt
from sympy import *


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


def plotdiscr(funcs:list[callable], T:list[int], vars:list[Symbol]=[Symbol("t")], label:str="none", **kwargs):
    time = range(T[0], T[1]+1)

    if not isinstance(funcs, list):
        funcs = [funcs]
    for i in range(len(funcs)):
        _plotdiscr_single(funcs[i], time, var=vars[i] if i<len(vars) else Symbol("t"), label=label, **kwargs)

    plt.axhline(0, color='black', linewidth=0.8)
    plt.grid(linewidth=0.5)
    plt.show()


def _plotdiscr_single(f:callable, time:list[int], var:Symbol=Symbol("t"), label:str="none", **kwargs):
    values = _evaluate_on_range(f, time, var=var, **kwargs)

    try:
        plt.stem(time, values, label=label)
        lims = (min(values), max(values))
        for i, v in zip(time, values):
            v_off = (lims[1]-lims[0])/40 * (1 if v >= 0 else -1)
            h_off = 0
            if v+v_off < lims[0] or v+v_off > lims[1]:
                v_off = -2.5*v_off
                h_off = -0.1 if i+h_off > min(time) else 0.1
            h_align = 'center' if h_off == 0 else 'right' if h_off<0 else 'left'
            v_align = 'bottom' if v >= 0 else 'top'
            font_scaling = 14/len(time)
            font_size = 10 * (1 if font_scaling >= 1 else font_scaling if font_scaling > 0.5 else 0.5)
            plt.text(i+h_off, v + v_off, v if type(v)==int else f'{v:.2f}', ha = h_align, va= v_align, fontsize=font_size)

    except TypeError as e:
        raise TypeError(f"There may free symbols left in the function: {_get_free_symbols(values)}. ") from e



def plotcont(funcs:list[callable], T:list[float], timestep:float, vars:list[Symbol]=[Symbol("t")], label:str="none", **kwargs):
    nsamples = int(((T[1]-T[0]))/timestep + 1.5)
    time = [T[0]+timestep*i for i in range(nsamples)]

    if not isinstance(funcs, list):
        funcs = [funcs]
    for i in range(len(funcs)):
        _plotcont_single(funcs[i], time, var=vars[i] if i<len(vars) else Symbol("t"), label=label, **kwargs)

    plt.axhline(0, color='black', linewidth=0.7)
    plt.axvline(0, color='black', linewidth=0.7)
    plt.grid(linewidth=0.5)
    plt.show()


def _plotcont_single(f:callable, time:list[float], var:Symbol=Symbol("t"), label:str="none", **kwargs):

    values = _evaluate_on_range(f, time, var=var, **kwargs)

    try:
        plt.plot(time, values)
    except TypeError as e:
        raise TypeError(f"There may free symbols left in the function: {_get_free_symbols(values)}") from e


def _evaluate_on_range(f, time:list[float], var:Symbol=Symbol("t"), **kwargs):
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


def _get_free_symbols(values):
    symbols = set()
    for v in values:
        try: symbols.update(v.free_symbols)
        except (TypeError, AttributeError): pass
    return symbols


def equivalent_test(f:callable, g:callable, T:list[float] = [-10, 10], timestep:float=0.5, **kwargs):
    nsamples = int((T[1]-T[0])/timestep + 0.99)
    time = [T[0]+timestep*i for i in range(nsamples)]

    fvals = _evaluate_on_range(f, time, **kwargs)
    gvals = _evaluate_on_range(g, time, **kwargs)

    try:
        return all(abs(fval-gval) < 1e-10 for fval, gval in zip(fvals, gvals))
    except TypeError as e:
        raise TypeError(f"There may free symbols left in the function: {_get_free_symbols(fvals).update(_get_free_symbols(gvals))}") from e
