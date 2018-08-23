from hask.lang import sig, H, d, data

@sig(H/ "a" >> "a")
def id(a):
    """
    id :: a -> a

    Identity function.
    """
    return a


@sig(H/ "a" >> "b" >> "a")
def const(a, b):
    """
    const :: a -> b -> a

    Constant function.
    """
    return a


@sig(H/ (H/ "a" >> "b" >> "c") >> "b" >> "a" >> "c")
def flip(f, b, a):
    """
    flip :: (a -> b -> c) -> b -> a -> c

    flip(f) takes its (first) two arguments in the reverse order of f.
    """
    return f(a, b)

@sig(H/ (H/ "b" >> "c") >> (H/ "a" >> "b") >> "a" >> "c")
def comp(g, f, x):
    """
    comp :: (b -> c) -> (a -> b) -> (a -> c)

    Function composition.
    """
    return g(f(x))

@sig(H/ "a" >> (H/ "a" >> "b") >> "b")
def revApp(x, f):
    """
    revApp :: a -> (a -> b) -> b

    Reverse application operator.
    """
    return f(x)