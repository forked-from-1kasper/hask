from hask import *

@sig(H/ String >> t(IO, Unit))
def helloPrint(s):
    return print(Just(s + "!"))

@sig(H/ String >> t(IO, String))
def getLineWithPrompt(prompt):
    return putStr(prompt) |chain| getLine

helloTest = getLineWithPrompt("Enter string: ") |bind| helloPrint
helloTest2 = \
    Data.Function.flip(Data.String.concat, "!") |map| \
    getLineWithPrompt("String #2: ")
helloTest3 = \
    Data.String.concat |map| \
    getLineWithPrompt("String #3: ") |ap| \
    getLineWithPrompt("String #4: ")

putStrLn("Never printed!")

main = \
    helloTest |chain| \
    (helloTest2 |bind| putStrLn) |chain| \
    (helloTest3 |bind| putStrLn)
System.IO.unsafePerformIO(main)