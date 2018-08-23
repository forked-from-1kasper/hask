from hask.lang import H, sig
from hask.cmp import cmp
from hask.Data.Unit import Unit, Star
import builtins


#=============================================================================#
# Typed wrappers for builtin Python functions.
# This makes it easier to chain lots of things together in function composition
# without having to manually add type signatures to Python builtins.


callable = callable ** (H/ "a" >> bool)
cmp = cmp ** (H/ "a" >> "a" >> int)
divmod = divmod ** (H/ "a" >> "b" >> ("c", "c"))
getattr = getattr ** (H/ "a" >> str >> "b")
hasattr = hasattr ** (H/ "a" >> str >> bool)
hash = hash ** (H/ "a" >> int)
hex = hex ** (H/ int >> str)
isinstance = isinstance ** (H/ "a" >> "b" >> bool)
issubclass = issubclass ** (H/ "a" >> "b" >> bool)
len = len ** (H/ "a" >> int)
oct = oct ** (H/ int >> str)
repr = repr ** (H/ "a" >> str)
sorted = sorted ** (H/ "a" >> list)
chr = chr ** (H/ int >> str)

@sig(H/ "a" >> str >> Unit)
def delattr(obj, name):
    builtins.delattr(obj, name)
    return Star

@sig(H/ "a" >> str >> "b" >> Unit)
def setattr(obj, name, value):
    builtins.setattr(obj, name, value)
    return Star