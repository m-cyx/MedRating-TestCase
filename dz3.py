def f1(a, b, *args, **kwargs):
    print(a)
    print(b)
    print(args)
    print(kwargs)
    print()
    f2(*args, **kwargs)


# l = [1, 2, 3]
# f1(1, 2, [1, 2, 3], {1: 1}, 1, 3, 4, 2, 1)
# f1(1, 2, *l)
# f1(1, 2, **{'1': 2})
# f1(1, 2, key=2)

# #f1(1,2,(3), q=3,w=4,e=5)


def f2(a, b, *args, c):
    print(a)
    print(b)
    print(args)
    print(*args)
    print(c)
    print()

l = [1,2,3]
# f2('a', 'b', l, c='c')


def f3(a, b=None, *args, d=None):
    print(a)
    print(b)
    print(args)
    print(d)
    print()


# Standard arguments
# *args arguments
# **kwargs arguments

f3(1, l, {b;2, d3} )

def f4(a, b, **kwargs):
    print(a)
    print(b)
    print(kwargs)
    print()


def f5(a, b, *, d):
    print(a)
    print(b)
    print(d)
    print()
