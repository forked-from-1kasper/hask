import builtins
from sys import stdin
from hask.lang import H, d, data, t, sig, caseof, m, p, _t, instance
from hask.lang import Show, show
from hask.Data.String import String
from hask.Data.Functor import Functor, fmap
from hask.Control.Applicative import Applicative
from hask.Control.Monad import Monad, bind, bindIgnore
from hask.Data.Unit import Unit, Star
from hask.lang.adt_syntax import ADT, HKT

@ADT
class IO(HKT("a")):
    LazyPure: [(H/ Unit >> "a").sig]
LazyPure = IO.LazyPure

@sig(H/ String >> t(IO, Unit))
def putStr(s):
    """
    putStr :: String -> IO Unit

    Prints string “s” to stdout without going to new line.
    """
    @sig(H/ Unit >> Unit)
    def _putStr(n):
        builtins.print(s, end='')
        return Star
    return LazyPure(_putStr)

@sig(H/ String >> t(IO, Unit))
def putStrLn(s):
    """
    putStrLn :: String -> IO Unit

    Prints string “s” to stdout with going to new line.
    """
    @sig(H/ Unit >> Unit)
    def _putStrLn(n):
        builtins.print(s)
        return Star
    return LazyPure(_putStrLn)

@sig(H[(Show, "a")]/ "a" >> t(IO, Unit))
def print(x):
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


@sig(H/ "a" >> t(IO, "a"))
def pure(x):
    """
    pure :: a -> IO a

    Wraps something in IO.
    """
    return LazyPure((lambda n: x) ** (H/ Unit >> "a"))


@sig(H/ t(IO, "a") >> "a")
def unsafePerformIO(io):
    """
    unsafePerformIO :: IO a -> a

    Unsafe performs IO.
    """
    return io.i0(Star)


@sig(H/ (H/ "a" >> "b") >> t(IO, "a") >> Unit >> "b")
def unsafeFmapIO(f, x, n):
    unboxed = unsafePerformIO(x)
    return f(unboxed)


@sig(H[(Applicative, "f")]/ t("f", H/ "a" >> "b") >> t("f", "a") >> Unit >> "b")
def unsafeApIO(f, x, n):
    unboxedF = unsafePerformIO(f)
    unboxedX = unsafePerformIO(x)
    return unboxedF(unboxedX)


@sig(H/ t(IO, "a") >> (H/ "a" >> t(IO, "b")) >> Unit >> "b")
def unsafeBindIO(x, f, n):
    unboxed = unsafePerformIO(x)
    return unsafePerformIO(f(unboxed))


instance(Functor, IO).where(fmap = lambda f, x: LazyPure(unsafeFmapIO(f, x)))
instance(Applicative, IO).where(
    pure = pure,
    ap = lambda f, x: LazyPure(unsafeApIO(f, x))
)
instance(Monad, IO).where(
    bind = lambda x, f: LazyPure(unsafeBindIO(x, f))
)