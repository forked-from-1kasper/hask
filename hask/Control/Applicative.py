from hask.lang import build_instance
from hask.lang import List
from hask.lang import instance
from hask.Data.Functor import Functor
from hask.lang import sig, H, t, L
from hask.lang.infix import Infix

class Applicative(Functor):
    """
    A functor with application, providing operations to embed pure expressions
    (pure), and sequence computations and combine their results (ap).

    Dependencies:
        Functor

    Attributes:
        pure

    Minimal complete definition:
        pure
    """
    @classmethod
    def make_instance(self, cls, pure, ap):
        pure = pure ** (H[(Applicative, "f")]/ "a" >> t("f", "a"))
        ap = ap ** (H[(Applicative, "f")]/
                    t("f", H/ "a" >> "b") >> t("f", "a") >> t("f", "b"))
        build_instance(Applicative, cls, {"pure":pure, "ap":ap})
        return

@sig(H[(Applicative, "f")]/ t("f", H/ "a" >> "b") >> t("f", "a") >> t("f", "b"))
def appAp(f, x):
    """
    appAp :: Applicative f => f (a -> b) -> f a -> f b
    """
    return Applicative[x].ap(f, x)


@Infix
def ap(f, x):
    """
    (ap) :: Applicative f => f (a -> b) -> f a -> f b

    This is infix and non-curried version of `appAp`.
    """
    return Applicative[x].ap(f, x)


instance(Applicative, List).where(
    pure = lambda x: L[[x]],
    ap = lambda fs, xs: L[[f(x) for f in fs for x in xs]]
)
