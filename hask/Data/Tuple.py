from hask.lang import H, sig, annotated
from hask.lang.type_vars import *


@annotated
def fst(tup : (a, b)) -> a:
    """
    ``fst :: (a, b) -> a``

    Extract the first component of a pair.
    """
    x, _ = tup
    return x


@annotated
def snd(tup : (a, b)) -> b:
    """
    ``snd :: (a, b) -> b``

    Extract the second component of a pair.
    """
    _, y = tup
    return y


@annotated
def curry(tup_fn : H/ (a, b) >> c, x : a, y : b) -> c:
    """
    ``curry :: ((a, b) -> c) -> a -> b -> c``

    curry converts an uncurried function to a curried function.
    """
    return tup_fn((x, y))


@annotated
def uncurry(fn : a >> b >> c, tup : (a, b)) -> c:
    """
    ``uncurry :: (a -> b -> c) -> (a, b) -> c``

    uncurry converts a curried function to a function on pairs.
    """
    return fn(fst(tup), snd(tup))


@annotated
def swap(tup : (a, b)) -> (b, a):
    """
    ``swap :: (a, b) -> (b, a)``

    Swap the components of a pair.
    """
    a, b = tup
    return (b, a)
