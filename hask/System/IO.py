from hask.lang import H, d, data, t, sig, caseof, m, p, _t, instance
from hask.Data.Functor import Functor, fmap
from hask.Control.Applicative import Applicative
from hask.Control.Monad import Monad, bind
from hask.Data.Unit import Unit, Star

IO, LazyPure =\
  data.IO("a") == d.LazyPure((H/ Unit >> "a").sig)

@sig(H/ str >> t(IO, Unit))
def putStr(s):
    @sig(H/ Unit >> Unit)
    def _putStr(n):
        print(s, end='')
        return Star
    return LazyPure(_putStr)

@sig(H/ str >> t(IO, Unit))
def putStrLn(s):
    @sig(H/ Unit >> Unit)
    def _putStrLn(n):
        print(s)
        return Star
    return LazyPure(_putStrLn)

getLine = LazyPure((lambda n: input()) ** (H/ Unit >> str))

@sig(H/ t(IO, "a") >> "a")
def unsafePerformIO(io):
    return io.i0(Star)

@sig(H/ "a" >> t(IO, "a"))
def pure(x):
    return LazyPure((lambda n: x) ** (H/ Unit >> "a"))


@sig(H/ t(IO, "a") >> (H/ "a" >> t(IO, "b")) >> t(IO, "b"))
def bindIO(x, f):
    def _bind(n):
        unboxed = unsafePerformIO(x)
        return unsafePerformIO(f(unboxed))
    return LazyPure(_bind ** (H/ Unit >> "b"))

@sig(H/ (H/ "a" >> "b") >> t(IO, "a") >> t(IO, "b"))
def fmapIO(f, x):
    def _fmap(n):
        unboxed = unsafePerformIO(x)
        return f(unboxed)
    return LazyPure(_fmap ** (H/ Unit >> "b"))

instance(Functor, IO).where(fmap = fmapIO)
instance(Applicative, IO).where(pure = pure)
instance(Monad, IO).where(bind = bindIO)

@sig(H/ t(IO, "a") >> t(IO, "b") >> t(IO, "b"))
def evaluateWithoutSend(x, y):
    def _evaluateWithoutSend(n):
        unsafePerformIO(x)
        return unsafePerformIO(y)
    return LazyPure(_evaluateWithoutSend ** (H/ Unit >> "b"))

@sig(H/ str >> t(IO, Unit))
def helloPrint(s):
    return putStrLn(s + "!")

helloTest = evaluateWithoutSend(putStr("Enter string: "), bind(getLine, helloPrint))
helloTest2 = fmap((lambda s: s + "!") ** (H/ str >> str))(getLine)