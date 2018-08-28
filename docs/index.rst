.. hask documentation master file, created by
   sphinx-quickstart on Tue Aug 28 16:41:54 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to hask's documentation!
================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   maybe

Hask is a pure-Python, zero-dependencies library that mimics most of the core language tools from Haskell, including:

 * Full Hindley-Milner type system (with typeclasses) that will typecheck any function decorated with a Hask type signature
 * Easy creation of new algebraic data types and new typeclasses, with Haskell-like syntax
 * Pattern matching with ``case`` expressions
 * Automagical function currying/partial application and function composition
 * Efficient, immutable, lazily evaluated ``List`` type with Haskell-style list comprehensions
 * All your favorite syntax and control flow tools, including operator sections, monadic error handling, guards, and more
 *  Python port of (some of) the standard libraries from Haskell’s ``base``, including:

   * Algebraic datatypes from the Haskell ``Prelude``, including ``Maybe`` and ``Either``
   * Typeclasses from the Haskell base libraries, including ``Functor``, ``Applicative``, ``Monad``, ``Enum``, ``Num``, and all the rest
   * Standard library functions from ``base``, including all functions from ``Prelude``, ``Data.List``, ``Data.Maybe``, and more

 * Monadic, lazy I/O `(WIP)`

Features not yet implemented, but coming soon:

 * Better support for polymorphic return values/type defaulting
 * Better support for lazy evaluation (beyond just the ``List`` type and pattern matching)
 * More of the Haskell standard library (``Control.*`` libraries, QuickCheck, and more)

**Note that all of this is still very much pre-alpha, and some things may be buggy!**


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
