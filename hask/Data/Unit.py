from hask.lang import deriving, data, d, Show, Eq
from hask.lang.adt_syntax import ADT

@ADT(deriving=[Show, Eq])
class Unit:
    """
    ``data Unit = Star``

    The type containing one value.
    """
    Star : []
Star = Unit.Star