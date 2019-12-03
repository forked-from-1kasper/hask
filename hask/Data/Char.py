from hask.lang import H
from hask.lang import sig, annotated
import unicodedata
import builtins


#=============================================================================#
# Character classification


@annotated
def isControl(s : str) -> bool:
    """
    isControl :: str -> bool

    Selects control characters, which are the non-printing characters of the
    Latin-1 subset of Unicode.
    """
    return unicodedata.category(s) == 'Cc' # Other, Control category


@annotated
def isSpace(s : str) -> bool:
    """
    isSpace :: str -> bool

    Returns True for any Unicode space character, and the control characters
    \t, \n, \r, \f, \v.
    """
    return s in " \t\n\r\f\v"


@annotated
def isLower(s : str) -> bool:
    """
    isLower :: str -> bool

    Selects lower-case alphabetic Unicode characters (letters).
    """
    return s.lower() == s


@annotated
def isUpper(s : str) -> bool:
    """
    isUpper :: str -> bool

    Selects upper-case or title-case alphabetic Unicode characters (letters).
    Title case is used by a small number of letter ligatures like the
    single-character form of Lj.
    """
    return s.upper() == s


@annotated
def isAlpha(s : str) -> bool:
    """
    isAlpha :: str -> bool

    Selects alphabetic Unicode characters (lower-case, upper-case and
    title-case letters, plus letters of caseless scripts and modifiers
    letters). This function is equivalent to isLetter.
    """
    return s.isalpha()


@annotated
def isNumber(s : str) -> bool:
    """
    isNumber :: str -> bool

    Selects Unicode numeric characters, including digits from various scripts,
    Roman numerals, etc.
    """
    return unicodedata.category(s) in ['Nd', 'Nl', 'No']


@annotated
def isAlphaNum(s : str) -> bool:
    """
    isAlphaNum :: str -> bool

    Selects alphabetic or numeric digit Unicode characters.

    Note that numeric digits outside the ASCII range are selected by this
    function but not by isDigit. Such digits may be part of identifiers but are
    not used by the printer and reader to represent numbers.
    """
    return isAlpha(s) or isNumber(s)


@annotated
def isPrint(s : str) -> bool:
    """
    isPrint :: str -> bool

    Selects printable Unicode characters (letters, numbers, marks, punctuation,
    symbols and spaces).
    """
    raise NotImplementedError


@annotated
def isDigit(s : str) -> bool:
    """
    isDigit :: str -> bool

    Selects ASCII digits, i.e. '0'..'9'.
    """
    return s in "0123456789"


@annotated
def isOctDigit(s : str) -> bool:
    """
    isOctDigit :: str -> bool

    Selects ASCII octal digits, i.e. '0'..'7'.
    """
    return s in "01234567"


@annotated
def isHexDigit(s : str) -> bool:
    """
    isHexDigit :: str -> bool

    Selects ASCII hexadecimal digits, i.e. '0'..'9', 'a'..'f', 'A'..'F'.
    """
    return s in "0123456789abcdefABCDEF"


@annotated
def isLetter(s : str) -> bool:
    """
    isLetter :: str -> bool

    Selects alphabetic Unicode characters (lower-case, upper-case and
    title-case letters, plus letters of caseless scripts and modifiers
    letters). This function is equivalent to isAlpha.
    """
    return isAlpha(s)


@annotated
def isMark(s : str) -> bool:
    """
    isMark :: str -> bool

    Selects Unicode mark characters, e.g. accents and the like, which combine
    with preceding letters.
    """
    return unicodedata.category(s) in ['Mn', 'Mc', 'Me']


@annotated
def isPunctuation(s : str) -> bool:
    """
    isPunctuation :: str -> bool

    Selects Unicode punctuation characters, including various kinds of
    connectors, brackets and quotes.
    """
    return unicodedata.category(s) in ['Pc', 'Pd', 'Ps', 'Pe', 'Pi', 'Pf', 'Po']


@annotated
def isSymbol(s : str) -> bool:
    """
    isSymbol :: str -> bool

    Selects Unicode symbol characters, including mathematical and currency
    symbols.
    """
    return unicodedata.category(s) in ['Sm', 'Sc', 'Sk', 'So']


@annotated
def isSeparator(s : str) -> bool:
    """
    isSeparator :: str -> bool

    Selects Unicode space and separator characters.
    """
    return unicodedata.category(s) in ['Zs', 'Zl', 'Zp']


#=============================================================================#
# Subranges


@annotated
def isAscii(s : str) -> bool:
    """
    isAscii :: str -> bool

    Selects the first 128 characters of the Unicode character set,
    corresponding to the ASCII character set.
    """
    return ord(s) < 128


@annotated
def isLatin1(s : str) -> bool:
    """
    isLatin1 :: str -> bool

    Selects the first 256 characters of the Unicode character set,
    corresponding to the ISO 8859-1 (Latin-1) character set.
    """
    return ord(s) < 256


@annotated
def isAsciiUpper(s : str) -> bool:
    """
    isAsciiUpper :: str -> bool

    Selects ASCII upper-case letters, i.e. characters satisfying both isAscii
    and isUpper.
    """
    return isAscii(s) and isUpper(s)


@annotated
def isAsciiLower(s : str) -> bool:
    """
    isAsciiLower :: str -> bool

    Selects ASCII lower-case letters, i.e. characters satisfying both isAscii
    and isLower.
    """
    return isAscii(s) and isLower(s)


#=============================================================================#
# Case conversion


@annotated
def toUpper(s : str) -> str:
    """
    toUpper :: str -> str

    Convert a letter to the corresponding upper-case letter, if any. Any other
    character is returned unchanged.
    """
    return s.upper()


@annotated
def toLower(s : str) -> str:
    """
    toLower :: str -> str

    Convert a letter to the corresponding lower-case letter, if any. Any other
    character is returned unchanged.
    """
    return s.lower()


@annotated
def toTitle(s : str) -> str:
    """
    toTitle :: str -> str

    Convert a letter to the corresponding title-case or upper-case letter, if
    any. (Title case differs from upper case only for a small number of
    ligature letters.) Any other character is returned unchanged.
    """
    return toUpper(s)


#=============================================================================#
# Single digit characters


@annotated
def digitToInt(s : str) -> int:
    """
    digitToInt :: str -> int

    Convert a single digit Char to the corresponding Int. This function fails
    unless its argument satisfies isHexDigit, but recognises both upper and
    lower-case hexadecimal digits (i.e. '0'..'9', 'a'..'f', 'A'..'F').
    """
    if s not in "0123456789abcdefABCDEF":
        raise ValueError("not a digit %s" % s)
    return "0123456789abcdef".index(s.lower())


@annotated
def intToDigit(s : int) -> str:
    """
    intToDigit :: int -> str

    Convert an Int in the range 0..15 to the corresponding single digit Char.
    This function fails on other inputs, and generates lower-case hexadecimal
    digits.
    """
    if s > 15 or s < 0:
        raise ValueError("not a digit %s" % s)
    return str(s) if s < 10 else "abcdef"[s-10]


#=============================================================================#
# Numeric representations

chr = builtins.chr ** (H/ int >> str)
ord = builtins.ord ** (H/ str >> int)
