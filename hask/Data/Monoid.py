from hask.lang import Typeclass
from hask.lang import build_instance
from hask.lang import H
from hask.lang import sig


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


@sig(H[(Monoid, "m")]/ "m" >> "m" >> "m")
def mappend(x, y):
    """
    mappend :: (Monoid m) => m -> m -> m

    An associative operation
    """
    return Monoid[x].mappend(x, y)


@sig(H[(Monoid, "m")]/ ["m"] >> "m")
def mconcat(xs):
    """
    mconcat :: (Monoid m) => [m] -> m

    Fold a list using the monoid.
    """
    return Monoid[xs[0]].mconcat(xs)
