import sys
import functools


# def inexhaustible(generator):
#     class Inexhaustible(object):
#         def __init__(self, generator):
#             self.start_generator = generator

#         def __call__(self, *args, **kwargs):
#             self.args = args
#             self.kwargs = kwargs
#             return self

#         def __iter__(self):
#             self.my_generator = self.start_generator(*self.args, **self.kwargs)
#             return self

#         def next(self):
#             return self.my_generator.next()

#     a = Inexhaustible(generator)
#     return a

def inexhaustible(func):
    inexhaustible.f = func
    #print list(inexhaustible.f())
    #print list(inexhaustible.f())
    @functools.wraps(func)
    def decorated(*args, **kwargs):
        result = list(inexhaustible.f())
        return 
    return decorated


call_counter = 0

@inexhaustible
def some_generator():
    global call_counter
    call_counter += 1
    yield 1
    yield 2

x = some_generator()

print (x is inexhaustible.f)

print(list(x))
print(list(x))

print(call_counter)

#exec(sys.stdin.read())
