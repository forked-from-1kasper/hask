# Hask

[![Build Status](https://travis-ci.org/forked-from-1kasper/hask.svg?branch=master)](https://travis-ci.org/forked-from-1kasper/hask)
[![Coverage Status](https://coveralls.io/repos/github/forked-from-1kasper/hask/badge.svg?branch=master)](https://coveralls.io/github/forked-from-1kasper/hask?branch=master)

Hask is a pure-Python, zero-dependencies library that mimics most of the core
language tools from Haskell, including:

* Full Hindley-Milner type system (with typeclasses) that will typecheck any
  function decorated with a Hask type signature
* Easy creation of new algebraic data types and new typeclasses, with
  Haskell-like syntax
* Pattern matching with `case` expressions
* Automagical function currying/partial application and function composition
* Efficient, immutable, lazily evaluated `List` type with Haskell-style list
  comprehensions
* All your favorite syntax and control flow tools, including operator sections,
  monadic error handling, guards, and more
* Python port of (some of) the standard libraries from Haskell's `base`,
  including:
  * Algebraic datatypes from the Haskell `Prelude`, including `Maybe` and
    `Either`
  * Typeclasses from the Haskell `base` libraries, including `Functor`,
    `Applicative`, `Monad`, `Enum`, `Num`, and all the rest
  * Standard library functions from `base`, including all functions from
    `Prelude`, `Data.List`, `Data.Maybe`, and more
* Monadic, lazy I/O *(WIP)*

Features not yet implemented, but coming soon:

* Better support for polymorphic return values/type defaulting
* Better support for lazy evaluation (beyond just the `List` type and pattern matching)
* More of the Haskell standard library (`Control.*` libraries, QuickCheck, and more)

**Note that all of this is still very much pre-alpha, and some things may be buggy!**

## Installation

1) `git clone https://github.com/forked-from-1kasper/hask`

2) `python3 setup.py install`

To run the tests: `python3 tests.py`.

### Python 2 support

No, use [original hask](https://github.com/billpmurphy/hask).

## “Why did you make this?”

I wanted to cram as much of Haskell into Python as possible while still being
100% compatible with the rest of Python, just to see if any useful ideas came
out of the result. Also, it was fun!

Contributions, forks, and extensions to this experiment are always welcome!
Feel free to submit a pull request, open an issue, or email me. In the spirit
of this project, abusing the Python language as much as possible is encouraged.

## Features

Hask is a grab-bag of features that add up to one big pseudo-Haskell functional
programming library. The rest of this README lays out the basics.

I recommend playing around in the REPL while going through the examples. You

To import all the language features: `from hask import *`
To import the Prelude: `from hask import Prelude`
To import a `base` library, e.g. `Data.List`: `from hask import Data.List`

### The List type and list comprehensions

Hask provides the `List` type, a lazy and statically-typed list, similar to
Haskell's standard list type.

To create a new `List`, just put the elements inside `L[` and `]` brackets, or
wrap an existing iterable inside `L[ ]`.

```python
>>> L[1, 2, 3]
L[1, 2, 3]

>>> my_list = ["a", "b", "c"]
>>> L[my_list]
L['a', 'b', 'c']

>>> L[(x**2 for x in range(1, 11))]
L[1 ... ]
```

To add elements to the front of a List, use `^`, the cons operator.  To combine
two lists, use `+`, the concatenation operator.

```python
>>> 1 ^ L[2, 3]
L[1, 2, 3]

>>> "goodnight" ^ ("sweet" ^ ("prince" ^ L[[]]))
L["goodnight", "sweet", "prince"]

>>> "a" ^ L[1.0, 10.3]  # type error

>>> L[1, 2] + L[3, 4]
L[1, 2, 3, 4]
```

Lists are always evaluated lazily, and will only evaluate list elements as
needed, so you can use infinite Lists or put never-ending generators inside of
a `List`. (Of course, you can still blow up the interpreter if you try to
evaluate the entirety of an infinite List, e.g. by trying to find the length of
the List with `len`.)

One way to create infinite lists is via list comprehensions. As in Haskell,
there are four basic type of list comprehensions:

```python
# list from 1 to infinity, counting by ones
L[1, ...]

# list from 1 to infinity, counting by twos
L[1, 3, ...]

# list from 1 to 20 (inclusive), counting by ones
L[1, ..., 20]

# list from 1 to 20 (inclusive), counting by fours
L[1, 5, ..., 20]
```

List comprehensions can be used on ints, longs, floats, one-character strings,
or any other instance of the `Enum` typeclass (more on this later).

Hask provides all of the Haskell functions for List manipulation (`take`,
`drop`, `takeWhile`, etc.), or you can also use Python-style indexing.

```python
>>> L[1, ...]
L[1 ...]


>>> from hask.Data.List import take
>>> take(5, L["a", "b", ...])
L['a', 'b', 'c', 'd', 'e']


>>> L[1,...][5:10]
L[6, 7, 8, 9, 10]


>>> from hask.Data.List import map
>>> from hask.Data.Char import chr
>>> letters = map(chr, L[97, ...])
>>> letters[:9]
L['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']


>>> len(L[1, 3, ...])  # uh oh
```

Otherwise, you can use `List` just like you would use a regular Python list.

```python
for i in L[0, ...]:
    print i


>>> 55 in L[1, 3, ...]
True
```

### Algebraic Data Types

Hask allows you to define [algebraic
datatypes](https://wiki.haskell.org/Algebraic_data_type), which are immutable
objects with a fixed number of typed, unnamed fields.

Here is the definition for the infamous `Maybe` type:

```python
from hask import data, d, deriving
from hask import Read, Show, Eq, Ord
from hask.lang.adt_syntax import ADT, HKT

@ADT
class Maybe(HKT("a", deriving=[Read, Show, Eq, Ord])):
    Nothing : []
    Just : "a"
Nothing, Just = Maybe.enums # brings `Nothing` and `Just` to outer scope
```

Let's break this down a bit. The syntax for defining a new [type
constructor](https://wiki.haskell.org/Constructor#Type_constructor) is:

```python
@ADT
class TypeName(HKT("type param", "type param2" ... "type param n"))
```

This defines a new algebraic datatype with type parameters.

To define [data
constructors](https://wiki.haskell.org/Constructor#Data_constructor) for this
type, use static field with annotations without realization.
The name of the data constructor goes first, followed by its
fields. If your data constructor has no fields, use `[]`.
For example:

```python
@ADT
class FooBar(HKT("a", "b")):
    Foo : ["a", "b", str]
    Bar : []
Foo, Bar = FooBar.enums
```

To automagically derive typeclass instances for the type, add
`deriving` parameter after the tzpe parameters.
Currently, the only typeclasses that can be derived are `Eq`, `Show`, `Read`,
`Ord`, and `Bounded`.

Putting it all together, here are the definitions of `Either` and `Ordering`:

```python
@ADT
class Either(HKT("a", "b", deriving=[Read, Show, Eq])):
    Left : "a"
    Right : "b"
Left, Right = Either.enums


@ADT
class Ordering(HKT(deriving=[Read, Show, Eq, Ord, Bounded])):
    LT : []
    EQ : []
    GT : []
LT, EQ, GT = Ordering.enums
```

You can now use the data constructors to create instances of these new types.
If the data constructor takes no arguments,
you can use it just like a variable.

```python
>>> Maybe.Just(10)
Just(10)

>>> Nothing
Nothing

>>> Just(Just(10))
Just(Just(10))

>>> Left(1)
Left(1)

>>> Foo(1, 2, "hello")
Foo(1, 2, 'hello')
```

You can view the type of an object with `showType` or `_t`
(with `from hask import _t`; equivalent to `:t` in ghci).

```python
>>> from hask import _t

>>> _t(1)
int

>>> _t(Just("soylent green"))
(Maybe str)

>>> _t(Right(("a", 1)))
(Either a (str, int))

>>> _t(Just)
(a -> Maybe a)

>>> showType(L[1, 2, 3, 4])
[int]
```

### The type system and typed functions

So what's up with those types? Hask operates its own shadow [Hindley-Milner
type system](https://en.wikipedia.org/wiki/Hindley%E2%80%93Milner_type_system)
on top of Python's type system; `_t` shows the Hask type of a particular
object.

In Hask, typed functions take the form of `TypedFunc` objects, which are typed
wrappers around Python functions. There are two ways to create `TypedFunc`
objects:

1) Use the `sig` decorator to decorate the function with the type signature

  ```python
  @sig(H/ "a" >> "b" >> "a")
  def const(x, y):
      return x
  ```

2) Use the `**` operator (similar to `::` in Haskell) to provide the type.
Useful for turning functions or lambdas into `TypedFunc` objects in the REPL,
or wrapping already-defined Python functions.

  ```python
  def const(x, y):
      return x
  
  const = const ** (H/ "a" >> "b" >> "a")
  ```

`TypedFunc` objects have several special properties. First, they are type
checked—when arguments are supplied, the type inference engine will check
whether their types match the type signature, and raise a `TypeError` if there
is a discrepancy.

```python
>>> f = (lambda x, y: x + y) ** (H/ int >> int >> int)

>>> f(2, 3)
5

>>> f(9, 1.0)  # type error
```

Second, `TypedFunc` objects can be [partially
applied](https://wiki.haskell.org/Partial_application):

```python
>>> g = (lambda a, b, c: a / (b + c)) ** (H/ int >> int >> int >> int)

>>> g(10, 2, 3)
2

>>> part_g = g(12)

>>> part_g(2, 2)
3

>>> g(20, 1)(4)
4
```

`TypedFunc` objects also have two special infix operators, the `*` and `%`
operators. `*` is the compose operator (equivalent to `(.)` in Haskell), so
`f * g` is equivalent to `lambda x: f(g(x))`. `%` is just the apply operator,
which applies a `TypedFunc` to one argument (equivalent to `($)` in Haskell).
The convinience of this notation (when combined with partial application)
cannot be overstated—you can get rid of a ton of nested parenthesis this way.

```python
>>> from hask.Prelude import flip
>>> h = (lambda x, y: x / y) ** (H/ float >> float >> float)

>>> h(3.0) * h(6.0) * flip(h, 2.0) % 36.0
9.0
```

The compose operation is also typed-checked, which makes it appealing to write
programs in [pointfree style](https://wiki.haskell.org/Pointfree), i.e,
chaining together lots of functions with composition and relying on the type
system to catch programming errors.

As you would expect, data constructors are also just `TypedFunc` objects:

```python
>>> Just * Just * Just * Just % 77
Just(Just(Just(Just(77))))
```

The type signature syntax is very simple, and consists of a few basic
primitives that can be combined to build any type signature:

| Primitive | Syntax/examples |
| --------- | --------------- |
| Type literal for Python builtin type or user-defined class | `int`, `float`, `set`, `list` |
| Type variable | `"a"`, `"b"`, `"zz"` |
| `List` of some type | `[int]`, `["a"]`, `[["a"]]` |
| Tuple type | `(int, int)`, `("a", "b", "c")`, `(int, ("a", "b"))` |
| ADT with type parameters | `t(Maybe, "a")`, `t(Either, "a", str)` |
| Unit type (`Unit`) | `Star` |
| Untyped Python function | `func` |
| Typeclass constraint | `H[(Eq, "a"), (Show, "b")]/`, `H[(Functor, "f"), (Show, "f")]/` |

Some examples:

```python
# add two ints together
@sig(H/ int >> int >> int)
def add(x, y):
    return x + y


# reverse order of arguments to a function
@sig(H/ (H/ "a" >> "b" >> "c") >> "b" >> "a" >> "c")
def flip(f, b, a):
    return f(a, b)


# map a Python (untyped) function over a Python (untyped) set
@sig(H/ func >> set >> set)
def set_map(fn, lst):
    return set((fn(x) for x in lst))


# map a typed function over a List
@sig(H/ (H/ "a" >> "b") >> ["a"] >> ["b"])
def map(f, xs):
    return L[(f(x) for x in xs)]


# type signature with an Eq constraint
@sig(H[(Eq, "a")]/ "a" >> ["a"] >> bool)
def not_in(y, xs):
    return not any((x == y for x in xs))


# type signature with a type constructor (Maybe) that has type arguments
@sig(H/ int >> int >> t(Maybe, int))
def safe_div(x, y):
    return Nothing if y == 0 else Just(x//y)


# type signature for a function that returns nothing
@sig(H/ int >> Unit)
def launch_missiles(num_missiles):
    print "Launching {0} missiles! Bombs away!" % num_missiles
    return Star
```

It is also possible to create type synonyms using `t`.
For example, check out the definition of `Rational`:

```python
class Ratio(HKT("a", deriving=[Eq])):
    R : ["a", "a"]
R = Ratio.R

Rational = t(Ratio, int)


@sig(H/ Rational >> Rational >> Rational)
def addRational(rat1, rat2):
    ...
```

### Pattern matching

Pattern matching is a more powerful control flow tool than the `if` statement,
and can be used to deconstruct iterables and ADTs and bind values to local
variables.

Pattern matching expressions follow this syntax:

```python
~(caseof(value_to_match)
    | m(pattern_1) >> return_value_1
    | m(pattern_2) >> return_value_2
    | m(pattern_3) >> return_value_3)
```

Here is a function that uses pattern matching to compute the fibonacci
sequence. Note that within a pattern match expression, `m.*` is used to bind
variables, and `p.*` is used to access them.

```python
def fib(x):
    return ~(caseof(x)
                | m(0)   >> 1
                | m(1)   >> 1
                | m(m.n) >> fib(p.n - 1) + fib(p.n - 2))

>>> fib(1)
1

>>> fib(6)
13
```

As the above example shows, you can combine pattern matching and recursive
functions without a hitch.

You can also deconstruct an iterable using `^` (the cons operator). The variable
before the `^` is bound to the first element of the iterable, and the variable
after the `^` is bound to the rest of the iterable. Here is a function that
adds the first two elements of any iterable, returning `Nothing` if there are
less than two elements:

```python
@sig(H[(Num, "a")]/ ["a"] >> t(Maybe, "a"))
def add_first_two(xs):
    return ~(caseof(xs)
                | m(m.x ^ (m.y ^ m.z)) >> Just(p.x + p.y)
                | m(m.x)               >> Nothing)


>>> add_first_two(L[1, 2, 3, 4, 5])
Just(3)

>>> add_first_two(L[9.0])
Nothing
```

Pattern matching is also very useful for deconstructing ADTs and assigning
their fields to temporary variables.

```python
def default_to_zero(x):
    return ~(caseof(x)
                | m(Just(m.x)) >> p.x
                | m(Nothing)   >> 0)


>>> default_to_zero(Just(27))
27


>>> default_to_zero(Nothing)
0
```

If you find pattern matching on ADTs too cumbersome, you can also use numeric
indexing on ADT fields. An `IndexError` will be thrown if you mess something
up.

```python
>>> Just(20.0)[0]
20.0

>>> Left("words words words words")[0]
'words words words words'

>>> Nothing[0]  # IndexError
```

### Typeclasses and typeclass instances

[Typeclasses](https://en.wikipedia.org/wiki/Type_class) allow you to add
additional functionality to your ADTs. Hask implements all of the major
typeclasses from Haskell (see the Appendix for a full list) and provides syntax
for creating new typeclass instances.

As an example, let's add a [`Monad`](https://wiki.haskell.org/Monad) instance
for the `Maybe` type.  First, however, `Maybe` needs
[`Functor`](https://wiki.haskell.org/Functor) and
[`Applicative`](https://wiki.haskell.org/Applicative_functor) instances.

```python
def maybe_fmap(fn, x):
    """Apply a function to the value inside of a (Maybe a) value"""
    return ~(caseof(x)
                | m(Nothing)   >> Nothing
                | m(Just(m.x)) >> Just(fn(p.x)))


instance(Functor, Maybe).where(
    fmap = maybe_fmap
)
```

`Maybe` is now an instance of `Functor`. This allows us to call `fmap`
and map any function of type `a -> b` into a value of type `Maybe a`.
Otherwise you can use `map`—infix version of `fmap`.

```python
>>> times2 = (lambda x: x * 2) ** (H/ int >> int)
>>> toFloat = float ** (H/ int >> float)

>>> toFloat |map| Just(10)
Just(10.0)

>>> toFloat |map| fmap(times2, Just(25))
Just(50.0)
```

Lots of nested calls to `fmap` get unwieldy very fast. Fortunately, any
instance of `Functor` can be used with the another infix `fmap` operator, `*`.
This is equivalent to `<$>` in Haskell.
Rewriting our example from above:

```python
>>> (toFloat * times2) * Just(25)
Just(50.0)

>>> (toFloat * times2) * Nothing
Nothing
```

Note that this example uses `*` as both the function compose operator and as
`fmap`, to lift functions into a `Maybe` value. If this seems confusing,
remember that `fmap` for functions is just function composition!

Now that `Maybe` is an instance of `Functor`, we can make it an instance of
`Applicative` and then an instance of `Monad` by defining the appropriate
function implementations. To implement `Applicative`, we just need to provide
`pure`. To implement `Monad`, we need to provide `bind`.

```python
from hask import Applicative, Monad

instance(Applicative, Maybe).where(
    pure = Just
)

instance(Monad, Maybe).where(
    bind = lambda x, f: ~(caseof(x)
                            | m(Just(m.a)) >> f(p.a)
                            | m(Nothing)   >> Nothing)
)
```

The `mbind` function also has an infix form, which is `|bind|` in Hask.

```python
@sig(H/ int >> int >> t(Maybe, int))
def safe_div(x, y):
    return Nothing if y == 0 else Just(x//y)


>>> from hask.Prelude import flip
>>> divBy = flip(s
