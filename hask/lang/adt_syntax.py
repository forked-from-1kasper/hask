from hask.lang.type_system import build_ADT
from hask.lang import H, t, sig
from hask.lang import Read, Show, Eq, Ord
from hask.lang.type_system import TypeMeta

def ADT(*typeargs, deriving = []):
    def retfun(cls):
        for obj in deriving:
            if not isinstance(obj, TypeMeta):
                raise TypeError('“%a” is not typeclass'.format(obj))

        annotations = getattr(cls, '__annotations__', {})
        data_constructors = list(annotations.items())

        klass, *ctors = build_ADT(
            typename = cls.__name__,
            typeargs = typeargs,
            data_constructors = data_constructors,
            to_derive = deriving
        )

        for ctor, value in zip(annotations, ctors):
            setattr(klass, ctor, value)

        klass.enums = ctors
        klass.__new__ = t
        klass.__doc__ = getattr(cls, '__doc__', '')

        return klass

    return retfun
