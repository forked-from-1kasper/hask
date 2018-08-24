from hask.lang import H, d, data, t, sig, caseof, m, p, _t, instance
from hask.Data.Functor import Functor, fmap
from hask.Control.Applicative import Applicative
from hask.Control.Monad import Monad, bind, bindIgnore
from hask.Data.Unit import Unit, Star

IO, LazyPure =\
  data.IO("a") == d.LazyPure((H/ Unit >> "a").sig)

@sig(H/ str >> t(IO, Unit))
def putStr(s):
    """
    putStr :: s -> IO Unit

    Prints string “s” to stdout without going to new line.
    """
    @sig(H/ Unit >> Unit)
    def _putStr(n):
        print(s, end='')
        return Star
    return LazyPure(_putStr)

@sig(H/ str >> t(IO, Unit))
def putStrLn(s):
    """
    putStrLn :: s -> IO Unit

    Prints string “s” to stdout with going to new line.
    """
    @sig(H/ Unit >> Unit)
    def _putStrLn(n):
        print(s)
        return Star
    return LazyPure(_putStrLn)

getLine = LazyPure((lambda n: input()) ** (H/ Unit >> str))

@sig(H/ t(IO, "a") >> "a")
def unsafePerformIO(io):
    """
    unsafePerformIO :: IO a -> a

    Unsafe performs IO.
    """
    return io.i0(Star)

@sig(H/ "a" >> t(IO, "a"))
def pure(x):
    """
    pure :: a -> IO a

    Wraps something in IO.
    """
    return LazyPure((lambda n: x) ** (H/ Unit >> "a"))


@sig(H/ t(IO, "a") >> (H/ "a" >> t(IO, "b")) >> t(IO, "b"))
def bindIO(x, f):
    """
    bindIO :: IO a -> (a -> IO b) -> IO b

    (>>=) realisation for IO.
    *Do not use this. Use Control.Monad.bind*
    """
    def _bind(n):
        unboxed = unsafePerformIO(x)
        return unsafePerformIO(f(unboxed))
    return LazyPure(_bind ** (H/ Unit >> "b"))

@sig(H/ (H/ "a" >> "b") >> t(IO, "a") >> t(IO, "b"))
def fmapIO(f, x):
    """
    fmapIO :: (a -> b) -> (IO a -> IO b)

    (<$>) realisation for IO.
    *Do not use this. Use Data.Functor.fmap*
    """
    def _fmap(n):
        unboxed = unsafePerformIO(x)
        return f(unboxed)
    return LazyPure(_fmap ** (H/ Unit >> "b"))

instance(Functor, IO).where(fmap = fmapIO)
instance(Applicative, IO).where(pure = pure)
instance(Monad, IO).where(bind = bindIO)