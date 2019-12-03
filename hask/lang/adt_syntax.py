from hask.lang.type_system import build_ADT
from hask.lang import H, t, sig
from hask.lang import Read, Show, Eq, Ord
from hask.lang.type_system import TypeMeta

def ADT(*typeargs, deriving=[]):
    def __new__(cls, *args):
        return t(cls, *args)

    def generator(cls):
        for obj in deriving:
            if not isinstance(obj, TypeMeta):
                raise TypeError('“%a” is not typeclass' % obj)

        annotations = getattr(cls, '__annotations__', {})
        data_constructors = [(key, annotations[key]) for key in annotations]

        t = build_ADT(typename = cls.__name__,
                      typeargs = typeargs,
                      data_constructors = data_constructors,
                      to_derive = deriving)
        res, *constructors = t

        for (constructor, value) in zip(annotations, constructors):
            setattr(res, constructor, value)

        setattr(res, 'enums', constructors)
        setattr(res, '__new__', __new__)
        setattr(res, '__doc__', getattr(cls, '__doc__', ''))

        return res

    return generator
