import sourceinspect as si

def func():
    pass

ret = si.getsource(func)
print(repr(ret))
assert ret.strip('\n') == 'def func():\n    pass'

def func():
    print(233)
    print(666)

ret = si.getsource(func)
print(repr(ret))
assert ret.strip('\n') == 'def func():\n    print(233)\n    print(666)'

def deco(x):
    return x

@deco
def func(done):
    well = done
    return well

ret = si.getsource(func)
print(repr(ret))
assert ret.strip('\n') == '@deco\ndef func(done):\n    well = done\n    return well'
