import sourceinspect

def func():
    pass

print(sourceinspect.get_inspector().getsourcelines(func))
