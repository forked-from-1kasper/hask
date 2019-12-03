__version__ = "0.0.2"


#=============================================================================#
# Module imports


import hask.lang
import hask.Data
import hask.Data.Char
import hask.Data.Either
import hask.Data.Eq
import hask.Data.Foldable
import hask.Data.Functor
import hask.Data.List
import hask.Data.Maybe
import hask.Data.Monoid
import hask.Data.Num
import hask.Data.Ord
import hask.Data.Ratio
import hask.Data.String
import hask.Data.Traversable
import hask.Data.Tuple
import hask.Data.Void
import hask.Control.Applicative
import hask.Control.Monad

from hask.Data.Functor import fmap, map
from hask.Control.Monad import bind, chain, mbind, bindIgnore
from hask.Control.Applicative import ap, appAp

import hask.System.IO
import hask.System.Environment
from hask.System.IO import IO, putStr, putStrLn, getLine, print

from .Python.builtins import *


#=============================================================================#
# Core language

## Typeclass instance declaration
from hask.lang import instance

## Operator sections
from hask.lang import __ as _

## Guard expressions
from hask.lang import guard, c, otherwise, NoGuardMatchException

## Lists/list comprehensions
from hask.lang import L

## ADT creation
from hask.lang import data, d, deriving

## Type signatures
from hask.lang import sig, annotated, constraint, H, t, func, TypeSignatureError

## Pattern matching
from hask.lang import caseof, p, m, IncompletePatternError

## REPL tools
from hask.lang import _t as showType
from hask.lang import _i as info

## Type system/typeclasses
from hask.lang import typeof, has_instance, Typeclass, Hask


#=============================================================================#
# Other imports

# Basic Typeclasses
from hask.Prelude import Read, Show, Eq, Ord, Enum, Bounded, Num, Real
from hask.Prelude import Integral, Fractional, Floating, RealFrac, RealFloat
from hask.Prelude import Traversable, Functor, Applicative, Monad, Foldable


# Standard types
from hask.Prelude import Maybe, Just, Nothing, in_maybe
from hask.Prelude import Either, Left, Right, in_either
from hask.Prelude import Ordering, LT, EQ, GT
from hask.Prelude import Unit, Star