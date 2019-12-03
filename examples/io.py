from hask import *

@annotated
def helloPrint(s : String) -> IO(Unit):
    return print(Just(s + "!"))

@annotated
def getLineWithPrompt(prompt : String) -> IO(String):
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