from hask.lang import H, caseof, sig
from hask.lang.adt_syntax import ADT, HKT

@ADT
class Void(HKT()): pass

@sig(H/ Void >> "a")
def absurd(v):
    """
    absurd :: Void -> a

    Since Void values logically don’t exist,
    this witnesses the logical reasoning tool of “ex falso quodlibet”.
    """
    return ~caseof(v)