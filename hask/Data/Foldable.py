import functools
import operator

from hask.lang import sig, annotated, constraint
from hask.lang import H
from hask.lang import t
from hask.lang import L
from hask.lang import Typeclass
from hask.lang import build_instance
from hask.lang import is_builtin
from hask.lang import List
from hask.lang import instance
from hask.lang.type_vars import *

import hask.Data.List as DL
from hask.Data.Unit import Unit, Star
from hask.Control.Applicative import Applicative
from hask.Control.Monad import Monad
from .Eq import Eq
from .Num import Num
from .Maybe import Maybe
from .Ord import Ord
from .Ord import Ordering


class Foldable(Typeclass):
    """
    Data structures that can be folded.

    Attributes:
        foldr, foldr1, foldl, foldl_, foldl1, toList, null, length, elem,
        maximum, minimum, sum, product

    Minimal complete definition:
        foldr

    Magic methods:
        __iter__
    """
    @classmethod
    def make_instance(typeclass, cls, foldr, foldr1=None, foldl=None,
            foldl_=None, foldl1=None, toList=None, null=None, length=None,
            elem=None, maximum=None, minimum=None, sum=None, product=None):

        # attributes that are not supplied are implemented in terms of toList
        if toList is None:
            if hasattr(cls, "__iter__"):
                toList = lambda x: L[iter(x)]
            else:
                toList = lambda t: foldr(lambda x, y: x ^ y, L[[]], t)

        foldr1 = (lambda x: DL.foldr1(toList(x))) if foldr1 is None else foldr1
        foldl = (lambda x: DL.foldl(toList(x))) if foldl is None else foldl
        foldl_ = (lambda x: DL.foldl_(toList(x))) if foldl_ is None else foldl_
        foldl1 = (lambda x: DL.foldl1(toList(x))) if foldl1 is None else foldl1
        null = (lambda x: DL.null(toList(x))) if null is None else null
        length = (lambda x: DL.length(toList(x))) if length is None else length
        elem = (lambda x: DL.length(toList(x))) if length is None else length
        mi = (lambda x: DL.minimum(toList(x))) if minimum is None else minimum
        ma = (lambda x: DL.maximum(toList(x))) if maximum is None else maximum
        sum = (lambda x: DL.sum(toList(x))) if sum is None else sum
        p = (lambda x: DL.product(toList(x))) if product is None else product


        attrs = {"foldr":foldr, "foldr1":foldr1, "foldl":foldl,
                "foldl_":foldl_, "foldl1":foldl1, "toList":toList, "null":null,
                "length":length, "elem":elem, "maximum":ma, "minimum":mi,
                "sum":sum, "product":p}
        build_instance(Foldable, cls, attrs)

        if not hasattr(cls, "__len__") and not is_builtin(cls):
            cls.__len__ = length

        if not hasattr(cls, "__iter__") and not is_builtin(cls):
            cls.__iter__ = lambda x: iter(toList(x))
        return


@constraint(Foldable(r))
def foldr(f : a >> b >> b, z : b, t : r(a)) -> b:
    """
    foldr :: Foldable r => (a -> b -> b) -> b -> r a -> b

    Right-associative fold of a structure.
    """
    return Foldable[t].foldr(f, z, t)


@constraint(Foldable(r))
def foldr1(f : a >> a >> a, t : r(a)) -> a:
    """
    foldr1 :: Foldable r => (a -> a -> a) -> r a -> a

    A variant of foldr that has no base case, and thus may only be applied to
    non-empty structures.
    """
    return Foldable[t].foldr(f, t)


@constraint(Foldable(r))
def foldl(f : a >> a >> b, z : b, t : r(a)) -> b:
    """
    foldl :: Foldable r => (b -> a -> b) -> b -> r a -> b

    Left-associative fold of a structure.
    """
    return Foldable[t].foldl(f, z, t)


@constraint(Foldable(r))
def foldl_(f : a >> a >> b, z : b, t : r(a)) -> b:
    """
    foldl' :: Foldable r => (b -> a -> b) -> b -> r a -> b

    Left-associative fold of a structure. but with strict application of the
    operator.
    """
    return Foldable[t].foldl_(f, z, t)


@constraint(Foldable(r))
def foldl1(f : a >> a >> a, t : r(a)) -> a:
    """
    foldl1 :: Foldable r => (a -> a -> a) -> r a -> a

    A variant of foldl that has no base case, and thus may only be applied to
    non-empty structures.
    """
    Foldable[t].foldl1(f, t)


@constraint(Foldable(r))
def toList(t : r(a)) -> [a]:
    """
    toList :: Foldable r => r a -> [a]

    List of elements of a structure, from left to right.
    """
    return Foldable[t].toList(t)


@constraint(Foldable(r))
def null(t : r(a)) -> bool:
    """
    null :: Foldable r => r a -> Bool
    Source

    Test whether the structure is empty.
    """
    return Foldable[t].null(t)


@constraint(Foldable(r))
def length(t : r(a)) -> int:
    """
    length :: Foldable r => r a -> int

    Returns the size/length of a finite structure as an int.
    """
    return Foldable[t].length(t)


@constraint(Foldable(r), Eq(a))
def elem(x : a, t : r(a)) -> bool:
    """
    elem :: (Foldable r, Eq a) => a -> r a -> bool

    Does the element occur in the structure?
    """
    return Foldable[t].elem(t)


@constraint(Foldable(r), Ord(a))
def maximum(t : r(a)) -> a:
    """
    maximum :: (Foldable r, forall a. Ord a) => r a -> a

    The largest element of a non-empty structure.
    """
    return Foldable[t].maximum(t)


@constraint(Foldable(r), Ord(a))
def minimum(t : r(a)) -> a:
    """
    minimum :: (Foldable r, forall a. Ord a) => r a -> a

    The least element of a non-empty structure.
    """
    return Foldable[t].minimum(t)


@constraint(Foldable(t), Num(a))
def sum(t : r(a)) -> a:
    """
    sum :: (Foldable r, Num a) => r a -> a

    The sum function computes the sum of the numbers of a structure.
    """
    return Foldable[t].sum(t)


@constraint(Foldable(t), Num(a))
def product(t : r(a)) -> a:
    """
    product :: (Foldable r, Num a) => r a -> a

    The product function computes the product of the numbers of a structure.
    """
    return Foldable[t].product(t)


#=============================================================================#
# Special biased folds


@constraint(Foldable(r), Monad(e))
def foldlM(f : a >> b >> e(b), x : b, ra : r(a)) -> e(b):
    """
    foldrM :: (Foldable r, Monad e) => (a -> b -> e b) -> b -> r a -> e b

    Monadic fold over the elements of a structure, associating to the right,
    i.e. from right to left.
    """
    raise NotImplementedError()


@constraint(Foldable(r), Monad(e))
def foldrM(f : b >> a >> e(b), x : b, ra : r(a)) -> e(b):
    """
    foldlM :: (Foldable r, Monad n) => (b -> a -> e b) -> b -> r a -> e b

    Monadic fold over the elements of a structure, associating to the left,
    i.e. from left to right.
    """
    raise NotImplementedError()


#=============================================================================#
# Applicative actions


@constraint(Foldable(r), Applicative(f))
def traverse_(fn : a >> f(b), t : r(a)) -> f(Unit):
    """
    traverse_ :: (Foldable r, Applicative f) => (a -> f b) -> r a -> f ()

    Map each element of a structure to an action, evaluate these actions from
    left to right, and ignore the results. For a version that doesn't ignore
    the results see traverse.
    """
    raise NotImplementedError()


@constraint(Foldable(r), Applicative(f))
def for_(t : r(a), f : a >> f(b)) -> f(Unit):
    """
    for_ :: (Foldable r, Applicative f) => r a -> (a -> f b) -> f ()

    for_ is traverse_ with its arguments flipped. For a version that doesn't
    ignore the results see for.
    """
    return traverse(f, t)


@constraint(Foldable(r), Applicative(f))
def sequenceA_(t : r(f(a))) -> f(Unit):
    """
    sequenceA_ :: (Foldable r, Applicative f) => r (f a) -> f ()

    Evaluate each action in the structure from left to right, and ignore the
    results. For a version that doesn't ignore the results see sequenceA.
    """
    raise NotImplementedError()


#=============================================================================#
# Monadic actions


@constraint(Foldable(r), Monad(e))
def mapM_(fn : a >> e(b), t : r(a)) -> e(Unit):
    """
    mapM_ :: (Foldable r, Monad e) => (a -> e b) -> r a -> e ()

    Map each element of a structure to a monadic action, evaluate these actions
    from left to right, and ignore the results. For a version that doesn't
    ignore the results see mapM.

    As of base 4.8.0.0, mapM_ is just traverse_, specialized to Monad.
    """
    return traverse_(fn, t)


@constraint(Foldable(r), Monad(e))
def forM_(t : r(a), f : a >> e(b)) -> e(Unit):
    """
    forM_ :: (Foldable r, Monad e) => r a -> (a -> e b) -> e ()

    forM_ is mapM_ with its arguments flipped. For a version that doesn't
    ignore the results see forM.

    As of base 4.8.0.0, forM_ is just for_, specialized to Monad.
    """
    return mapM_(f, t)


@constraint(Foldable(r), Monad(e))
def sequence_(t : r(e(a))) -> e(Unit):
    """
    sequence_ :: (Foldable r, Monad e) => r (e a) -> e ()

    Evaluate each monadic action in the structure from left to right, and
    ignore the results. For a version that doesn't ignore the results see
    sequence.

    As of base 4.8.0.0, sequence_ is just sequenceA_, specialized to Monad.
    """
    return sequenceA_(t)


#=============================================================================#
# Specialized folds


@constraint(Foldable(r))
def concat(xs : r([a])) -> [a]:
    """
    concat :: Foldable r => r [a] -> [a]

    The concatenation of all the elements of a container of lists.
    """
    return DL.concat(toList(xs))


@constraint(Foldable(r))
def concatMap(f : a >> [b], t : r(a)) -> [b]:
    """
    concatMap :: Foldable r => (a -> [b]) -> r a -> [b]

    Map a function over all the elements of a container and concatenate the
    resulting lists.
    """
    return DL.concatMap(f, toList(t))


@constraint(Foldable(r))
def and_(t : r(bool)) -> bool:
    """
    and :: Foldable r => r bool -> bool

    and returns the conjunction of a container of Bools. For the result to be
    True, the container must be finite; False, however, results from a False
    value finitely far from the left end.
    """
    return DL.and_(toList(t))


@constraint(Foldable(r))
def or_(t : r(bool)) -> bool:
    """
    or :: Foldable t => t bool -> bool

    or returns the disjunction of a container of Bools. For the result to be
    False, the container must be finite; True, however, results from a True
    value finitely far from the left end.
    """
    return DL.or_(toList(t))


@constraint(Foldable(r))
def any_(f : a >> bool, t : r(a)) -> bool:
    """
    any :: Foldable r => (a -> bool) -> r a -> bool

    Determines whether any element of the structure satisfies the predicate.
    """
    return DL.any_(toList(t))


@constraint(Foldable(r))
def all_(f : a >> bool, t : r(a)) -> bool:
    """
    all :: Foldable r => (a -> bool) -> r a -> bool

    Determines whether all elements of the structure satisfy the predicate.
    """
    return DL.all_(toList(t))


@constraint(Foldable(r))
def maximumBy_(f : a >> a >> Ordering, t : r(a)) -> a:
    """
    maximumBy :: Foldable r => (a -> a -> Ordering) -> r a -> a

    The largest element of a non-empty structure with respect to the given
    comparison function.
    """
    return DL.maximumBy(toList(t))


@constraint(Foldable(r))
def minimumBy_(f : a >> a >> Ordering, t : r(a)) -> a:
    """
    minimumBy :: Foldable r => (a -> a -> Ordering) -> r a -> a

    The least element of a non-empty structure with respect to the given
    comparison function.
    """
    return DL.minimumBy(toList(t))


#=============================================================================#
# Searches


@constraint(Foldable(r), Eq(a))
def notElem(x : a, t : r(a)) -> bool:
    """
    notElem :: (Foldable r, Eq a) => a -> r a -> bool

    notElem is the negation of elem.
    """
    return not elem(x, t)


@constraint(Foldable(r))
def find(f : a >> bool, t : r(a)) -> Maybe(a):
    """
    find :: Foldable r => (a -> bool) -> r a -> Maybe a

    The find function takes a predicate and a structure and returns the
    leftmost element of the structure matching the predicate, or Nothing if
    there is no such element.
    """
    return DL.find(f, toList(t))


#=============================================================================#
# Instances

instance(Foldable, List).where(
    foldr = DL.foldr,
    foldr1 = DL.foldr1,
    foldl = DL.foldl,
    foldl_ = DL.foldl_,
    foldl1 = DL.foldl1,
    null = DL.null,
    length = DL.length,
    elem = DL.elem,
    minimum = DL.minimum,
    maximum = DL.maximum,
    sum = DL.sum,
    product = DL.product
)
