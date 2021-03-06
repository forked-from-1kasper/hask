from hask.lang import sig, constraint
from hask.lang import H
from hask.lang import t
from hask.lang.type_vars import *


# Current implementation is just a wrapper around Python's Fraction. This is
# not a long-term solution (not extensible beyond builtin types) but it will do
# for now.

from .Num import Integral
from .Num import RealFrac
from .Num import Ratio
from .Num import R
from .Num import Rational
from .Num import toRatio
from .Num import toRational


@constraint(Integral(a))
def numerator(ratio : Ratio(a)) -> a:
    """
    ``numerator :: Integral a => Ratio a -> a``

    Extract the numerator of the ratio in reduced form: the numerator and
    denominator have no common factor and the denominator is positive.
    """
    return toRatio(ratio[0], ratio[1])[0]


@constraint(Integral(a))
def denominator(ratio : Ratio(a)) -> a:
    """
    ``denominator :: Integral a => Ratio a -> a``

    Extract the denominator of the ratio in reduced form: the numerator and
    denominator have no common factor and the denominator is positive.
    """
    return toRatio(ratio[0], ratio[1])[1]


@constraint(RealFrac(a))
def approxRational(x : a, epsilon : a) -> Rational:
    """
    ``approxRational :: RealFrac a => a -> a -> Rational``

    approxRational, applied to two real fractional numbers x and epsilon,
    returns the simplest rational number within epsilon of x. A rational number
    y is said to be simpler than another y' if

    abs(numerator(y)) <= abs(numerator(y_)) and
    denominator(y) <= denominator(y_)

    Any real interval contains a unique simplest rational; in particular, note
    that 0/1 is the simplest rational of all.
    """
    raise NotImplementedError()
