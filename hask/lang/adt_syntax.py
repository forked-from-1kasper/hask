from hask.lang.type_system import build_ADT
from hask.lang import H, t, sig
from hask.lang import Read, Show, Eq, Ord

def ADT(cls):
    if not isinstance(cls, HKT):
        raise TypeError('ADT must be inherited from “HKT” class')

    typename, typeargsObj, env = cls.typeargs
    
    if len(typeargsObj) != 1:
        raise TypeError('ADT must be inherited *only* from “HKT” class')

    typeargs = list(typeargsObj[0].typeargs)
    deriving = typeargsObj[0].deriving

    annotations = env.get('__annotations__', {})
    data_constructors = [(key, annotations[key]) for key in annotations]

    t = build_ADT(typename = typename,
                  typeargs = typeargs,
                  data_constructors = data_constructors,
                  to_derive = deriving)
    res, *constructors = t

    for (constructor, value) in zip(annotations, constructors):
        setattr(res, constructor, value)
    setattr(res, 'enums', constructors)
    return res

class HKT():
    def __init__(self, *args, **kwargs):
        self.typeargs = args
        self.deriving = kwargs.get("deriving", [])