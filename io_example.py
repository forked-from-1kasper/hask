from hask import *
from hask.Data.Functor import fmap
from hask.Control.Monad import bind, bindIgnore

@sig(H/ String >> t(IO, Unit))
def helloPrint(s):
    return print(Just(s + "!"))

helloTest = bindIgnore(putStr("Enter string: "), bind(getLine, helloPrint))
helloTest2 = fmap((lambda s: s + "!") ** (H/ String >> String))(getLine)

System.IO.unsafePerformIO(helloTest)