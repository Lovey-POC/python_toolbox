import gc
import weakref

import nose.tools

from garlicsim.general_misc.caching import cache


def counting_func(a=1, b=2, *args, **kwargs):
    if not hasattr(counting_func, 'i'):
        counting_func.i = 0
    try:
        return counting_func.i
    finally:
        counting_func.i = (counting_func.i + 1)

        
def test_basic():
    
    f = cache()(counting_func)
    
    assert f() == f() == f(1, 2) == f(a=1, b=2)
    
    assert f() != f('boo')
    
    assert f('boo') == f('boo') == f(a='boo')
    
    assert f('boo') != f(meow='frrr')
    
    assert f(meow='frrr') == f(1, meow='frrr') == f(a=1, meow='frrr')
    

def test_weakref():
    
    f = cache()(counting_func)
    
    class A(object): pass
    
    a = A()
    result = f(a)
    assert result == f(a) == f(a) == f(a)
    a_ref = weakref.ref(a)    
    del a
    gc.collect()
    assert a_ref() is None
    
    a = A()
    result = f(meow=a)
    assert result == f(meow=a) == f(meow=a) == f(meow=a)
    a_ref = weakref.ref(a)
    del a
    gc.collect()
    
    assert a_ref() is None
    
    
def test_max_size():
    
    f = cache(max_size=3)(counting_func)
    
    r0, r1, r2 = f(0), f(1), f(2)
    
    assert f(0) == f(0) == r0 == f(0)
    assert f(1) == f(1) == r1 == f(1)
    assert f(2) == f(2) == r2 == f(2)
    
    r3 = f(3)
    
    assert f(0) != r0 # Now we recalculated f(0) so we forgot f(1)
    assert f(2) == f(2) == r2 == f(2)
    assert f(3) == f(3) == r3 == f(3)
    

def test_unhashable_arguments():
    
    f = cache()(counting_func)
    
    
    assert f(set((1, 2))) == f(set((1, 2)))
    
    assert f(7, set((1, 2))) != f(8, set((1, 2)))
    
    assert f('boo') != f(meow='frrr')
    
    assert f(meow={1: [1, 2], 2: frozenset([3, 'b'])}) == \
           f(1, meow={1: [1, 2], 2: frozenset([3, 'b'])})
    
    
def test_function_instead_of_max_size():

    def confusedly_put_function_as_max_size():
        exec('@cache\n'
             'def f():\n'
             '    pass')
        
    try:
        confusedly_put_function_as_max_size()
    except TypeError, exception:
        assert type(exception) is TypeError
        assert exception.args[0] == (
            'You entered the callable `%s` where you should have '
            'entered the `max_size` for the cache. You probably '
            'used `@cache`, while you should have used `@cache()`'
        )
    else:
        raise Exception('Should have gotten `TypeError`.')
    
    