from hask.lang import deriving, data, d, Show, Eq
from hask.lang.adt_syntax import ADT, HKT

@ADT
class Unit(HKT(deriving=[Show, Eq])):
    Star : []
Star = Unit.Star