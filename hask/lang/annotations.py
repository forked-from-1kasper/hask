from hask import *
from hask.lang.syntax import __signature__
from hask.lang.type_system import build_sig, make_fn_type, TypedFunc
import inspect

def constraint(*constraints):
    def get_annotation(annotation, name):
        if annotation == inspect._empty:
            raise TypeError('Missing type for “%s”' % name)
        else:
            return annotation
    
    def make_typed(fn):
        sig = inspect.signature(fn)
        params = sig.parameters
        types = [ get_annotation(params[param].annotation, param)
                  for param in params ]
        types += [ get_annotation(sig.return_annotation, 'return') ]

        sig = __signature__(types, constraints).sig

        fn_args = build_sig(sig)
        fn_type = make_fn_type(fn_args)
        return TypedFunc(fn, fn_args, fn_type)
    return make_typed

annotated = constraint()
