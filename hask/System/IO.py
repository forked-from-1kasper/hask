import builtins
from sys import stdin
from hask.lang import H, d, data, t, sig, annotated, constraint
from hask.lang import caseof, m, p, _t, instance
from hask.lang import Show, show
from hask.lang.type_vars import *
from hask.Data.String import String
from hask.Data.Functor import Functor, fmap
from hask.Control.Applicative import Applicative
from hask.Control.Monad import Monad, bind, bindIgnore
from hask.Data.Unit import Unit, Star
from hask.lang.adt_syntax import ADT

@ADT("a")
class IO:
    """
    A value of type `IO a` is a computation which, when performed,
    does some I/O before returning a value of type `a`.

    There is really only one good way to “perform” an I/O action:
    using `System.IO.unsafePerformIO` at end of your program.

    `IO` is a monad, so `IO` actions can be combined using
    the `(>>)` (`|chain|`) and `(>>=)` (`|bind|`) operations
    from the `Monad` (Control.Monad) class.
    """
    LazyPure: [(H/ Unit >> "a").sig]
LazyPure = IO.LazyPure

@annotated
def putStr(s : String) -> IO(Unit):
    """
    putStr :: String -> IO Unit

    Prints string “s” to stdout without going to new line.
    """
    @sig(H/ Unit >> Unit)
    def _putStr(n):
        builtins.print(s, end='')
        return Star
    return LazyPure(_putStr)


@annotated
def putStrLn(s : String) -> IO(Unit):
    """
    putStrLn :: String -> IO Unit

    Prints string “s” to stdout with going to new line.
    """
    @sig(H/ Unit >> Unit)
    def _putStrLn(n):
        builtins.print(s)
        return Star
    return LazyPure(_putStrLn)

@constraint(Show(a))
def print(x : a) -> IO(Unit):
    """
    print :: Show a => a -> IO Unit

    The “print” function outputs a value of any printable type to the stdout.
    """
    return putStrLn(show(x))

getLine = LazyPure((lambda n: input()) ** (H/ Unit >> String))
getLine.__doc__ = """
    getLine :: IO String

    Reads line from stdin.
"""

getContents = LazyPure((lambda n: stdin.read()) ** (H/ Unit >> String))
getContents.__doc__ = """
    getContents :: IO String

    Returns all user input as a single string.
"""


@annotated
def pure(x : a) -> IO(a):
    """
    pure :: a -> IO a

    Wraps something in IO.
    """
    return LazyPure((lambda n: x) ** (H/ Unit >> "a"))


@annotated
def unsafePerformIO(io : IO(a)) -> a:
    """
    unsafePerformIO :: IO a -> a

    Unsafe performs IO.
    """
    return io.i0(Star)


@annotated
def unsafeFmapIO(f : a >> b, x : IO(a), n : Unit) -> b:
    return f(unsafePerformIO(x))


@annotated
def unsafeApIO(fn : IO(a >> b), x : IO(a), n : Unit) -> b:
    return unsafePerformIO(fn)(unsafePerformIO(x))


@annotated
def unsafeBindIO(x : IO(a), f : a >> IO(b), n : Unit) -> b:
    return unsafePerformIO(f(unsafePerformIO(x)))


instance(Functor, IO).where(fmap = lambda f, x: LazyPure(unsafeFmapIO(f, x)))
instance(Applicative, IO).where(
    pure = pure,
    ap = lambda f, x: LazyPure(unsafeApIO(f, x))
)
instance(Monad, IO).where(
    bind = lambda x, f: LazyPure(unsafeBindIO(x, f))
)
