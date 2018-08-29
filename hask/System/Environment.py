from hask.lang import H, sig, L, t
from hask.Data.Maybe import Just, Nothing, Maybe
from hask.Data.String import String
from hask.Data.Unit import Unit
from hask.System.IO import IO, LazyPure
import sys, os

getArgs = LazyPure((lambda n: L[[]] if len(sys.argv) < 1 else L[sys.argv[1:]]) **
                   (H/ Unit >> [String]))
getArgs.__doc__ = """
    ``getArgs :: IO [String]``

    Computation ``getArgs`` returns a list of the program’s
    command line arguments (not including the program name).
"""

@sig(H/ String >> t(IO, t(Maybe, String)))
def lookupEnv(var):
    """
    ``lookupEnv :: String -> IO (Maybe String)``

    Return the value of the environment variable ``var``,
    or ``Nothing`` if there is no such value.
    """
    def unsafeToMaybe(x):
        if x is None:
            return Nothing
        else:
            return Just(x)
    return LazyPure((lambda n: unsafeToMaybe(os.environ.get(var, None))) **
                    (H/ Unit >> t(Maybe, String)))