from sympy import *


def convolution_discrete(f:callable, g:callable, lower_limit:int = -50, upper_limit:int = 50):
    """Convolution of two discrete functions"""
    try:
        out = lambda n: sum(f(k)*g(n-k) for k in range(lower_limit, upper_limit))
    except TypeError:
        n = symbols("n")
        out = lambda t: sum(f.subs(n, k)*g.subs(n, t-k) for k in range(lower_limit, upper_limit))
    return out

def convolution_discrete_s(f, g, v=Symbol("n"), lower_limit:int = -200, upper_limit:int = 200):
    """Convolution of two discrete functions"""
    k = Symbol("k")
    return sum(f.subs(v, k)*g.subs(v, v-k) for k in range(lower_limit, upper_limit))

def convolution_s(f:callable, g:callable):
    """Symbolic convolution of two functions"""
    t, tau = symbols("t τ")
    return integrate(f(tau)*g(t-tau), (tau, -oo, oo))


def convolution_discretized(f:callable, g:callable, lower_limit:int = -50, upper_limit:int = 50, timestep:float = 0.01):
    """Convolution of two discrete functions"""
    return lambda t: sum(timestep*f(lower_limit+timestep*k)*g(t-(lower_limit+timestep*k)) for k in range(int((upper_limit-lower_limit)/timestep)+1))
