from hask.lang import Read, Show
from hask.lang import L, H, sig, t, data, d, caseof, m, p
from hask.lang import deriving, instance, typify

from .Eq import Eq
from .Ord import Ord
from .Functor import Functor
from hask.Control.Applicative import Applicative
from hask.Control.Monad import Monad

from hask.lang.adt_syntax import ADT
from hask.lang.annotations import annotated
from hask.lang.type_vars import *


@ADT(a, deriving=[Read, Show, Eq, Ord])
class Maybe:
    """
    ``data Maybe a = Nothing | Just a deriving(Show, Eq, Ord)``

    The Maybe type encapsulates an optional value.
    A value of type ``Maybe a`` either contains a value of type ``a``
    (represented as ``Just a``), or it is empty (represented as ``Nothing``).
    Using Maybe is a good way to deal with errors or exceptional cases
    without resorting to drastic measures such as error.

    The ``Maybe`` type is also a monad.
    It is a simple kind of error monad,
    where all errors are represented by ``Nothing``.
    A richer error monad can be built using the ``Either`` type.
    """
    Nothing : []
    Just : a
Nothing, Just = Maybe.enums

instance(Functor, Maybe).where(
    fmap = lambda f, x: ~(caseof(x)
                            | m(Just(m.a)) >> Just(f(p.a))
                            | m(Nothing)   >> Nothing)
)

instance(Applicative, Maybe).where(
    pure = Just,
    ap = lambda fs, xs: ~(caseof((fs, xs))
                            | m((Just(m.f), Just(m.x))) >> Just(p.f(p.x))
                            | m((Nothing, m.x)) >> Nothing)
)

instance(Monad, Maybe).where(
    bind = lambda x, f: ~(caseof(x)
                            | m(Just(m.a)) >> f(p.a)
                            | m(Nothing)   >> Nothing)
)


def in_maybe(fn):
    """
    Decorator for monadic error handling.

    If the decorated function raises an exception, return Nothing. Otherwise,
    take the result and wrap it in a Just.
    """
    def closure_in_maybe(*args, **kwargs):
        try:
            return Just(fn(*args, **kwargs))
        except:
            return Nothing
    return typify(fn, hkt=lambda x: t(Maybe, x))(closure_in_maybe)


@annotated
def maybe(default: b, f: a >> b, maybe_a: Maybe(a)) -> b:
    """
    ``maybe :: b -> (a -> b) -> Maybe a -> b``

    The maybe function takes a default value, a function, and a ``Maybe`` value.
    If the ``Maybe`` value is ``Nothing``, the function returns the default value.
    Otherwise, it applies the function to the value inside the ``Just`` and returns
    the result.
    """
    return default if maybe_a == Nothing else f(maybe_a[0])


@annotated
def isJust(a : Maybe(a)) -> bool:
    return not isNothing(a)


@annotated
def isNothing(a : Maybe(a)) -> bool:
    return ~(caseof(a)
                | m(Nothing)   >> True
                | m(Just(m.x)) >> False)


@annotated
def fromJust(x : Maybe(a)) -> a:
    if isJust(x):
        return x[0]
    raise ValueError("Cannot call fromJust on Nothing.")


@annotated
def listToMaybe(xs : [a]) -> Maybe(a):
    return ~(caseof(xs)
                | m(m.a ^ m.b) >> Just(p.a)
                | m(m.a)       >> Nothing)


@annotated
def maybeToList(xs : Maybe(a)) -> [a]:
    """
    ``maybeToList :: Maybe a -> [a]``

    The maybeToList function returns an empty list when given ``Nothing`` or a
    singleton list when not given ``Nothing``.
    """
    return ~(caseof(xs)
                | m(Nothing)   >> L[[]]
                | m(Just(m.x)) >> L[[p.x]])


@annotated
def catMaybes(xs : [Maybe(a)]) -> [a]:
    """
    ``catMaybes :: [Maybe a] -> [a]``

    The catMaybes function takes a list of Maybes and returns a list of all the
    ``Just`` values.
    """
    return L[(fromJust(item) for item in xs if isJust(item))]


@annotated
def mapMaybe(f : a >> Maybe(b), la : [a]) -> [b]:
    """
    ``mapMaybe :: (a -> Maybe b) -> [a] -> [b]``

    The mapMaybe function is a version of map which can throw out elements. In
    particular, the functional argument returns something of type ``Maybe b``. If
    this is ``Nothing``, no element is added on to the result list. If it is Just
    b, then b is included in the result list.
    """
    return L[(fromJust(b) for b in (f(a) for a in la) if isJust(b))]
