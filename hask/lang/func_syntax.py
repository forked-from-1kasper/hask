from hask.lang.syntax import __signature__
from hask.lang.type_system import build_sig, make_fn_type, TypedFunc
import inspect

def typed(*constraints):
    def get_annotation(annotation, name):
        if isinstance(annotation, __signature__):
            return annotation.sig
        elif annotation == inspect._empty:
            raise TypeError('need annotation for “%s”' % name)
        else:
            return annotation
    
    def make_typed(fn):
        sig = inspect.signature(fn)
        params = sig.parameters
        types = [ get_annotation(params[param].annotation, param)
                  for param in params ] + \
                [ get_annotation(sig.return_annotation, 'return') ]

        sig = __signature__(types, constraints).sig

        fn_args = build_sig(sig)
        fn_type = make_fn_type(fn_args)
        res = TypedFunc(fn, fn_args, fn_type)
        setattr(res, '__annotations__', fn.__annotations__)
        return res
    return make_typed
