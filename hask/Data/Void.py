from hask.lang import H, caseof, sig, annotated
from hask.lang.adt_syntax import ADT
from hask.lang.type_vars import *

@ADT()
class Void:
    """
    ``data Void``

    A logically uninhabited data type,
    used to indicate that a given term should not exist.
    """
    pass

@annotated
def absurd(v : Void) -> a:
    """
    ``absurd :: Void -> a``

    Since Void values logically don’t exist,
    this witnesses the logical reasoning tool of “ex falso quodlibet”.
    """
    return ~caseof(v)