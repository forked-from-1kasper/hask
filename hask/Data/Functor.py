from hask.lang import TypedFunc, Typeclass, is_builtin
from hask.lang import build_instance, List
from hask.lang import L, H, sig, t
from hask.lang import instance, deriving, Show, data, d
from hask.Data.Function import const, comp
from hask.Data.Unit import Unit, Star
from hask.lang.infix import Infix
import builtins

class Functor(Typeclass):
    """
    The Functor class is used for types that can be mapped over. Instances of
    Functor should satisfy the following laws:

    fmap(id)  ==  id
    fmap(f * g)  ==  fmap(f * (fmap g))

    Attributes:
        fmap, __rmul__

    Minimal complete definition:
        fmap
    """
    @classmethod
    def make_instance(typeclass, cls, fmap):
        fmap = fmap ** \
            (H[(Functor, "f")]/ (H/ "a" >> "b") >> t("f", "a") >> t("f", "b"))
        if not is_builtin(cls):
            cls.__rmul__ = lambda x, f: fmap(f, x)
        build_instance(Functor, cls, {"fmap":fmap})
        return

@Infix
def map(f, x):
    """
    map :: Functor f => (a -> b) -> (f a -> f b)

    This is infix and non-curried version of `fmap`.
    Maps function over functor.
    """
    return Functor[x].fmap(f, x)

@sig(H[(Functor, "f")]/ (H/ "a" >> "b") >> t("f", "a") >> t("f", "b"))
def fmap(f, x):
    """
    fmap :: Functor f => (a -> b) -> (f a -> f b)

    Maps function over functor.
    """
    return Functor[x].fmap(f, x)

@sig(H[(Functor, "f")]/ t("f", "a") >> t("f", Unit))
def void(x):
    return fmap(const(Star), x)

instance(Functor, List).where(
    fmap = lambda fn, lst: L[builtins.map(fn, builtins.iter(lst))]
)

instance(Functor, TypedFunc).where(
    fmap = TypedFunc.__mul__
)