from hask import *

@sig(H/ String >> t(IO, Unit))
def helloPrint(s):
    return print(Just(s + "!"))

helloTest = putStr("Enter string: ") |bindIgnore| (getLine |bind| helloPrint)
helloTest2 = (lambda s: s + "!") ** (H/ String >> String) |map| getLine

main = bindIgnore(helloTest, helloTest2 |bind| putStrLn)
System.IO.unsafePerformIO(main)