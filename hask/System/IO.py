import builtins
from sys import stdin
from hask.lang import H, d, data, t, sig, caseof, m, p, _t, instance
from hask.lang import Show, show
from hask.Data.String import String
from hask.Data.Functor import Functor, fmap
from hask.Control.Applicative import Applicative
from hask.Control.Monad import Monad, bind, bindIgnore
from hask.Data.Unit import Unit, Star

IO, LazyPure =\
  data.IO("a") == d.LazyPure((H/ Unit >> "a").sig)

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

@sig(H/ t(IO, "a") >> "a")
def unsafePerformIO(io):
    """
    unsafePerformIO :: IO a -> a

    Unsafe performs IO.
    """
    return io.i0(Star)

@sig(H/ (H/ "a" >> "b") >> t(IO, "a") >> t(IO, "b"))
def fmapIO(f, x):
    """
    fmapIO :: (a -> b) -> (IO a -> IO b)

    (<$>) realisation of IO.
    *Do not use this. Use Data.Functor.fmap*
    """
    def _fmap(n):
        unboxed = unsafePerformIO(x)
        return f(unboxed)
    return LazyPure(_fmap ** (H/ Unit >> "b"))

@sig(H/ "a" >> t(IO, "a"))
def pure(x):
    """
    pure :: a -> IO a

    Wraps something in IO.
    """
    return LazyPure((lambda n: x) ** (H/ Unit >> "a"))

@sig(H[(Applicative, "f")]/ t("f", H/ "a" >> "b") >> t("f", "a") >> t("f", "b"))
def apIO(f, x):
    """
    apIO :: (a -> b) -> (IO a -> IO b)

    (<*>) realisation of IO.
    *Do not use this. Use Control.Applicative.ap*
    """
    def _ap(n):
        unboxedF = unsafePerformIO(f)
        unboxedX = unsafePerformIO(x)
        return unboxedF(unboxedX)
    return LazyPure(_ap ** (H/ Unit >> "b"))

@sig(H/ t(IO, "a") >> (H/ "a" >> t(IO, "b")) >> t(IO, "b"))
def bindIO(x, f):
    """
    bindIO :: IO a -> (a -> IO b) -> IO b

    (>>=) realization of IO.
    *Do not use this. Use Control.Monad.bind*
    """
    def _bind(n):
        unboxed = unsafePerformIO(x)
        return unsafePerformIO(f(unboxed))
    return LazyPure(_bind ** (H/ Unit >> "b"))

instance(Functor, IO).where(fmap = fmapIO)
instance(Applicative, IO).where(pure = pure, ap = apIO)
instance(Monad, IO).where(bind = bindIO)