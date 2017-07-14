from hask.lang import build_instance
from hask.lang import List
from hask.lang import instance
from hask.Data.Functor import Functor


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
    def make_instance(self, cls, pure):
        build_instance(Applicative, cls, {"pure":pure})
        return


instance(Applicative, List).where(
    pure = lambda x: L[[x]]
)
