# http://code.activestate.com/recipes/384122/
# “Python has the wonderful "in" operator and it would be nice to have
# additional infix operator like this.
# This recipe shows how (almost) arbitrary infix operators can be defined.”
class Infix:
    def __init__(self, function):
        self.function = function
    def __ror__(self, other):
        return Infix(lambda x, self=self, other=other: self.function(other, x))
    def __or__(self, other):
        return self.function(other)
    def __call__(self, value1, value2):
        return self.function(value1, value2)