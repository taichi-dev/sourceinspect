import sourceinspect

def func():
    pass

print(sourceinspect.Inspector.getsourcelines(func))
