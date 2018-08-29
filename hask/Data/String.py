from hask.lang import H
from hask.lang import sig
from hask.lang import L


String = str


@sig(H/ String >> [String])
def lines(string):
    """
    ``lines :: String -> [String]``

    lines breaks a string up into a list of strings at newline characters.
    The resulting strings do not contain newlines.
    """
    return L[[]] if not string else L[string.split("\n")]


@sig(H/ String >> [String])
def words(string):
    """
    ``words :: String -> [String]``

    words breaks a string up into a list of words, which were delimited by
    white space.
    """
    return L[[]] if string == "" else L[string.split(" ")]


@sig(H/ [String] >> String)
def unlines(strings):
    """
    ``lines :: [String] -> String``

    unlines is an inverse operation to lines. It joins lines, after appending a
    terminating newline to each.
    """
    return "\n".join(strings)


@sig(H/ [String] >> String)
def unwords(strings):
    """
    ``unwords :: [String] -> String``

    unwords is an inverse operation to words. It joins words with separating
    spaces.
    """
    return " ".join(strings)

@sig(H/ String >> String >> String)
def concat(x, y):
    """
    ``concat :: String -> String -> String``

    Concatenates two strings.
    """
    return x + y