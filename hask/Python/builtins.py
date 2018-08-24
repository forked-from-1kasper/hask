from hask.lang.syntax import H, sig
from hask.Data.String import String
from hask.Data.Unit import Unit, Star
import builtins


#=============================================================================#
# Typed wrappers for builtin Python functions.
# This makes it easier to chain lots of things together in function composition
# without having to manually add type signatures to Python builtins.


callable = callable ** (H/ "a" >> bool)
cmp = (lambda a, b: (a > b) - (a < b)) ** (H/ "a" >> "a" >> int)
divmod = divmod ** (H/ "a" >> "b" >> ("c", "c"))
getattr = getattr ** (H/ "a" >> String >> "b")
hasattr = hasattr ** (H/ "a" >> String >> bool)
hash = hash ** (H/ "a" >> int)
hex = hex ** (H/ int >> String)
isinstance = isinstance ** (H/ "a" >> "b" >> bool)
issubclass = issubclass ** (H/ "a" >> "b" >> bool)
len = len ** (H/ "a" >> int)
oct = oct ** (H/ int >> String)
repr = repr ** (H/ "a" >> String)
sorted = sorted ** (H/ "a" >> list)
chr = chr ** (H/ int >> String)

@sig(H/ "a" >> String >> Unit)
def delattr(obj, name):
    builtins.delattr(obj, name)
    return Star

@sig(H/ "a" >> String >> "b" >> Unit)
def setattr(obj, name, value):
    builtins.setattr(obj, name, value)
    return Star