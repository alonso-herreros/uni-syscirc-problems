from matplotlib import pyplot as plt
from sympy import Symbol
from .symbolics import get_free_symbols, evaluate_on_range


def plotdiscr(funcs:list[callable], T:list[int], vars=Symbol("n", integer=True), **kwargs):
    time = range(T[0], T[1]+1)

    if not isinstance(funcs, list):
        funcs = [funcs]
    for i in range(len(funcs)):
        _plotdiscr_single(funcs[i], time, var=vars[i] if i<len(vars) else vars[0], **kwargs)

    plt.axhline(0, color='black', linewidth=0.8)
    plt.grid(linewidth=0.5)
    plt.show()


def _plotdiscr_single(f:callable, time:list[int], var:Symbol, **kwargs):
    values = evaluate_on_range(f, time, var=var, **kwargs)

    try:
        plt.stem(time, values)
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
        raise TypeError(f"There may free symbols left in the function: {get_free_symbols(values)}. ") from e



def plotcont(funcs:list[callable], T:list[float], timestep:float=0.01, vars=Symbol("t", real=True), nsamples:int=None, **kwargs):
    if nsamples==None:
        nsamples = int(((T[1]-T[0]))/timestep + 1.5)
    else:
        timestep = (T[1]-T[0])/(nsamples-1)
    time = [T[0]+timestep*i for i in range(nsamples)]

    if not isinstance(funcs, list):
        funcs = [funcs]
    if not isinstance(vars, list):
        vars = [vars]
    for i in range(len(funcs)):
        _plotcont_single(funcs[i], time, var=vars[i] if i<len(vars) else vars[0], **kwargs)

    plt.axhline(0, color='black', linewidth=0.7)
    plt.axvline(0, color='black', linewidth=0.7)
    plt.grid(linewidth=0.5)
    plt.show()


def _plotcont_single(f:callable, time:list[float], var:Symbol, **kwargs):

    values = evaluate_on_range(f, time, var=var, **kwargs)

    try:
        plt.plot(time, values)
    except TypeError as e:
        raise TypeError(f"There may free symbols left: {get_free_symbols(values)} in the function, {get_free_symbols(time)} in the time.") from e

