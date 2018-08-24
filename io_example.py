from hask import *

@sig(H/ String >> t(IO, Unit))
def helloPrint(s):
    return print(Just(s + "!"))

helloTest = putStr("Enter string: ") |chain| getLine |bind| helloPrint
helloTest2 = Data.Function.flip(Data.String.concat, "!") |map| getLine
helloTest3 = Data.String.concat |map| getLine |ap| getLine

main = helloTest |chain| \
       (helloTest2 |bind| putStrLn) |chain| \
       (helloTest3 |bind| putStrLn)
System.IO.unsafePerformIO(main)