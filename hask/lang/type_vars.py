from string import ascii_lowercase
from .syntax import H, t

class TypeVarSyntax(str):
    def __rshift__(dom, cod):
        return H/ dom >> cod

    def __call__(self, *args):
        return t(self, *args)

reserved = "mpdtxyz"

for alpha in ascii_lowercase:
    if alpha not in reserved:
        globals()[alpha] = TypeVarSyntax(alpha)