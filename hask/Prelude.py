import math

from .lang import H, sig, t


#=============================================================================#
# Standard types, classes, and related functions
## Basic data types


from .Data.Maybe import Maybe, Just, Nothing, in_maybe, maybe
from .Data.Either import Either, Left, Right, in_either, either
from .Data.Ord import Ordering, LT, EQ, GT
from .Data.Unit import Unit, Star


### Tuples
from .Data.Tuple import fst, snd, curry, uncurry


#=============================================================================#
## Basic type classes
from .lang import Read, Show, show

from .Data.Eq import Eq
from .Data.Ord import Ord, max, min, compare

from .lang import Enum, fromEnum, succ, pred, enumFromThen
from .lang import enumFrom, enumFromThenTo, enumFromTo

from .lang import Bounded
from .Data.Functor import Functor, fmap, void

from .Control.Applicative import Applicative
from .Control.Monad import Monad
from .Data.Foldable import Foldable
from .Data.Traversable import Traversable


#=============================================================================#
# Numbers
### Numeric type classes
from .Data.Num import Num, abs, negate, signum, Fractional, recip

from .Data.Num import Integral, toRatio, Ratio, R, Rational, Floating

from .Data.Num import sqrt, log, pow, logBase, sin, tan, cos, exp
from .Data.Num import asin, atan, acos, sinh, tanh, cosh
from .Data.Num import asinh, atanh, acosh, atan2

from .Data.Num import Real, RealFloat, RealFrac, toRational

from .Data.Num import properFraction, truncate, round, ceiling, floor
from .Data.Num import isNaN, isInfinite, isNegativeZero


#=============================================================================#
# Numeric functions


@sig(H[(Num, "a")]/ "a" >> "a" >> "a")
def subtract(x, y):
    """
    subtract :: Num a => a -> a -> a

    the same as lambda x, y: y - x
    """
    return y - x


@sig(H[(Integral, "a")]/ "a" >> bool)
def even(x):
    """
    even :: Integral a => a -> Bool

    Returns True if the integral value is even, and False otherwise.
    """
    return x % 2 == 0


@sig(H[(Integral, "a")]/ "a" >> bool)
def odd(x):
    """
    odd :: Integral a => a -> Bool

    Returns True if the integral value is odd, and False otherwise.
    """
    return x % 2 == 1


@sig(H[(Integral, "a")]/ "a" >> "a" >> "a")
def gcd(x, y):
    """
    gcd :: Integral a => a -> a -> a

    gcd(x,y) is the non-negative factor of both x and y of which every common
    factor of x and y is also a factor; for example gcd(4,2) = 2, gcd(-4,6) =
    2, gcd(0,4) = 4. gcd(0,0) = 0. (That is, the common divisor that is
    "greatest" in the divisibility preordering.)
    """
    return math.gcd(x, y)


@sig(H[(Integral, "a")]/ "a" >> "a" >> "a")
def lcm(x, y):
    """
    lcm :: Integral a => a -> a -> a

    lcm(x,y) is the smallest positive integer that both x and y divide.
    """
    g = gcd(x, y)
    return 0 if g == 0 else (x * y) // g


#=============================================================================#
# Monads and functors


from .Data.Functor import Functor
from .Control.Applicative import Applicative
from .Control.Monad import Monad


@sig(H[(Monad, "m")]/ t("m", "a") >> t("m", Unit))
def sequence(xs):
    """
    sequence :: Monad m => [m a] -> m [a]

    Evaluate each action in the sequence from left to right, and collect the
    results.
    """
    raise NotImplementedError()


@sig(H[(Monad, "m")]/ t("m", "a") >> t("m", Unit))
def sequence_(xs):
    """
    sequence_ :: Monad m => [m a] -> m Unit

    Evaluate each action in the sequence from left to right, and ignore the
    results.
    """
    raise NotImplementedError()


def mapM(f, xs):
    """
    mapM :: Monad m => (a -> m b) -> [a] -> m [b]

    mapM(f) is equivalent to sequence * map(f)
    """
    return sequence(fmap(f, xs))


def mapM_(f, xs):
    """
    mapM_ :: Monad m => (a -> m b) -> [a] -> m ()

    mapM_(f) is equivalent to sequence_ * map(f)
    """
    return sequence_(fmap(f, xs))




#=============================================================================#
# Miscellaneous functions

from hask.Data.Function import id, const, flip, comp


@sig(H/ (H/ "a" >> bool) >> (H/ "a" >> "a") >> "a" >> "a")
def until(p, f, a):
    """
    until :: (a -> Bool) -> (a -> a) -> a -> a

    until(p, f, a) yields the result of applying f until p(a) holds.
    """
    while not p(a):
        a = f(a)
    return a


@sig(H/ "a" >> "a" >> "a")
def asTypeOf(a, b):
    """
    asTypeOf :: a -> a -> a

    asTypeOf is a type-restricted version of const. It is usually used as an
    infix operator, and its typing forces its first argument (which is usually
    overloaded) to have the same type as the second.
    """
    return a


@sig(H/ str >> "a")
def error(msg):
    """
    error :: str -> a

    error(msg) stops execution and displays an error message.
    """
    raise Exception(msg)


from .lang import undefined

# List operations
from .Data.List import map, filter, head, last, tail, init
from .Data.List import null, reverse, length, L

from .Data.List import foldl, foldl1, foldr, foldr1

## Special folds
from .Data.List import and_, or_, any, all, sum, product
from .Data.List import concat, concatMap, maximum, minimum

## Building lists
### Scans
from .Data.List import scanl, scanl1, scanr, scanr1

### Infinite lists
from .Data.List import iterate, repeat, replicate, cycle

## Sublists
from .Data.List import take, drop, splitAt, takeWhile, dropWhile, span, break_

## Searching lists
from .Data.List import elem, notElem, lookup

## Zipping and unzipping lists
from .Data.List import zip, zip3, zipWith, zipWith3, unzip, unzip3

## Functions on strings
from .Data.List import lines, words, unlines, unwords
