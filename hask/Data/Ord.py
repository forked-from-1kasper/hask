from hask.lang import Show, Read, Bounded, Ord
from hask.lang import sig, H, data, d
from hask.lang import deriving
from .Eq import Eq
from hask.lang.adt_syntax import ADT

@ADT(deriving=[Read, Show, Eq, Ord, Bounded])
class Ordering:
    """
    ``data Ordering = LT | EQ | GT deriving(Show, Eq, Ord, Bounded)``

    The `Ordering` datatype allows a single comparison
    to determine the precise ordering of two objects.
    """
    LT : []
    EQ : []
    GT : []
LT, EQ, GT = Ordering.enums


@sig(H[(Ord, "a")]/ "a" >> "a" >> "a")
def max(x, y):
    """
    ``max :: a -> a -> a``

    Maximum function.
    """
    return x if x >= y else y


@sig(H[(Ord, "a")]/ "a" >> "a" >> "a")
def min(x, y):
    """
    ``min :: a -> a -> a``

    Minumum function.
    """
    return x if x <= y else y


@sig(H[(Ord, "a")]/ "a" >> "a" >> Ordering)
def compare(x, y):
    """
    ``compare :: a -> a -> Ordering``

    Comparison function.
    """
    return EQ if x == y else (LT if x < y else GT)


@sig(H[(Ord, "a")]/ (H/ "a" >> "b") >> "b" >> "b" >> Ordering)
def comparing(p, x, y):
    """
    ``comparing :: Ord a => (b -> a) -> b -> b -> Ordering``

    comparing(p, x, y) = compare(p(x), p(y))

    Useful combinator for use in conjunction with the xxxBy family of functions
    from Data.List, for example:

    ... sortBy (comparing(fst)) ...
    """
    return compare(p(x), p(y))
