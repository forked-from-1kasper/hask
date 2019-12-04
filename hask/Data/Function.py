from hask.lang import sig, annotated, H, d, data
from hask.lang.type_vars import *

@annotated
def id(x : a) -> a:
    """
    id :: a -> a

    Identity function.
    """
    return x


@annotated
def const(x : a, y : b) -> a:
    """
    const :: a -> b -> a

    Constant function.
    """
    return x


@annotated
def flip(f : a >> b >> c, y : b, x : a) -> c:
    """
    flip :: (a -> b -> c) -> b -> a -> c

    flip(f) takes its (first) two arguments in the reverse order of f.
    """
    return f(x, y)

@annotated
def comp(g : b >> c, f : a >> b, x : a) -> c:
    """
    comp :: (b -> c) -> (a -> b) -> (a -> c)

    Function composition.
    """
    return g(f(x))

@annotated
def revApp(x : a, f : a >> b) -> b:
    """
    revApp :: a -> (a -> b) -> b

    Reverse application operator.
    """
    return f(x)