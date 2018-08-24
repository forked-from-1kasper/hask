from hask.lang import deriving, data, d, Show, Eq
from hask.lang.adt_syntax import ADT, HKT

@ADT
class Unit(HKT(deriving=[Show, Eq])):
    """
    `data Unit = Star`

    The type containing one value.
    """
    Star : []
Star = Unit.Star