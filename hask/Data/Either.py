from hask.lang import Read, Show
from hask.lang import H, t, d, caseof, m, p, sig, annotated
from hask.lang import data, deriving, instance, L, typify

from .Eq import Eq

from .Ord import Ord

from .Functor import Functor, fmap

from hask.Control.Applicative import Applicative
from hask.Control.Monad import Monad

from hask.lang.adt_syntax import ADT
from hask.lang.type_vars import *

@ADT(a, b, deriving=[Read, Show, Eq, Ord])
class Either:
    """
    `data Either a b = Left a | Right b deriving(Read, Show, Eq, Ord)`

    The Either type represents values with two possibilities:
    a value of type `Either a b` is either `Left a` or `Right b`.

    The Either type is sometimes used to represent a value which is
    either correct or an error; by convention, the `Left` constructor is used
    to hold an error value and the `Right` constructor is used
    to hold a correct value (mnemonic: “right” also means “correct”).
    """
    Left : a
    Right : b
Left, Right = Either.enums


instance(Functor, Either).where(
    fmap = lambda f, v: ~(caseof(v)
                            | m(Left(m.e))  >> Left(p.e)
                            | m(Right(m.ra)) >> Right(f(p.ra)))
)

instance(Applicative, Either).where(
    pure = Right,
    ap = lambda v, x: ~(caseof(v)
                          | m(Left(m.l)) >> Left(p.l)
                          | m(Right(m.r)) >> fmap(p.r, x))
)

instance(Monad, Either).where(
    bind = lambda v, f: ~(caseof(v)
                            | m(Left(m.e))  >> Left(p.e)
                            | m(Right(m.a)) >> f(p.a))
)


def in_either(fn):
    """
    Decorator for monadic error handling.
    If the decorated function raises an exception, return the exception inside
    Left. Otherwise, take the result and wrap it in Right.
    """
    def closure_in_either(*args, **kwargs):
        try:
            return Right(fn(*args, **kwargs))
        except Exception as e:
            return Left(e)
    return typify(fn, hkt=lambda x: t(Either, "aa", x))(closure_in_either)


@annotated
def either(fa : a >> c, fb : b >> c, e : Either(a, b)) -> c:
    """
    either :: (a -> c) -> (b -> c) -> Either a b -> c

    Case analysis for the Either type. If the value is Left(a), apply the first
    function to a; if it is Right(b), apply the second function to b.
    """
    return ~(caseof(e)
                | m(Left(m.a))  >> fa(p.a)
                | m(Right(m.b)) >> fb(p.b))


@annotated
def lefts(xs : [Either(a, b)]) -> [a]:
    """
    lefts :: [Either a b] -> [a]

    Extracts from a List of Either all the Left elements. All the Left elements
    are extracted in order.
    """
    return L[(x[0] for x in xs if isLeft(x))]


@annotated
def rights(xs : [Either(a, b)]) -> [b]:
    """
    rights :: [Either a b] -> [b]

    Extracts from a list of Either all the Right elements. All the Right
    elements are extracted in order.
    """
    return L[(x[0] for x in xs if isRight(x))]


@annotated
def isLeft(x : Either(a, c)) -> bool:
    """
    isLeft :: Either a b -> bool

    Return True if the given value is a Left-value, False otherwise.
    """
    return ~(caseof(x)
                | m(Right(m.x)) >> False
                | m(Left(m.x))  >> True)


@annotated
def isRight(x : Either(a, b)) -> bool:
    """
    isRight :: Either a b -> bool

    Return True if the given value is a Right-value, False otherwise.
    """
    return not isLeft(x)


@annotated
def partitionEithers(xs : [Either(a, b)]) -> ([a], [b]):
    """
    partitionEithers :: [Either a b] -> ([a], [b])

    Partitions a List of Either into two lists. All the Left elements are
    extracted, in order, to the first component of the output. Similarly the
    Right elements are extracted to the second component of the output.
    """
    return (lefts(xs), rights(xs))
