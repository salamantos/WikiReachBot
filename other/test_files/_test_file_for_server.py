def f():
    print('f')


a = {1: f}
for i in a:
    print a.get(i)()
