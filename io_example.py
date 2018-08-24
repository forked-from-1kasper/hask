from hask import *
from hask.Data.Functor import fmap
from hask.Control.Monad import bind, bindIgnore

@sig(H/ str >> t(IO, Unit))
def helloPrint(s):
    return putStrLn(s + "!")

helloTest = bindIgnore(putStr("Enter string: "), bind(getLine, helloPrint))
helloTest2 = fmap((lambda s: s + "!") ** (H/ str >> str))(getLine)

System.IO.unsafePerformIO(helloTest)