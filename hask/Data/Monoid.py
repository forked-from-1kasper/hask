from hask.lang import Typeclass
from hask.lang import build_instance
from hask.lang import H, sig, constraint
from hask.lang.type_vars import *


class Monoid(Typeclass):
    """
    The class of monoids (types with an associative binary operation that has
    an identity)

    Attributes:
        mempty, mappend, mconcat

    Minimal complete definition:
        mempty, mappend, mconcat
    """
    @classmethod
    def make_instance(typeclass, cls, mempty, mappend, mconcat):
        attrs = {"mempty":mempty, "mappend":mappend, "mconcat":mconcat}
        build_instance(Monoid, cls, attrs)
        return


@constraint(Monoid(a))
def mappend(x : a, y : a) -> a:
    """
    mappend :: (Monoid m) => m -> m -> m

    An associative operation
    """
    return Monoid[x].mappend(x, y)


@constraint(Monoid(a))
def mconcat(xs : [a]) -> a:
    """
    mconcat :: (Monoid m) => [m] -> m

    Fold a list using the monoid.
    """
    return Monoid[xs[0]].mconcat(xs)
