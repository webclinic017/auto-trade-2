def with_metaclass(meta, *bases):
    print('meta 1')
    class metaclass(meta):
        def __new__(cls, name, this_bases, d):
            print('meta 3')
            return meta(name, bases, d)
    print('meta 2')
    return type.__new__(metaclass, str('temporary_class'), (), {})

class MetaBaseBase2(type):
    pass

class MetaBase2(MetaBaseBase2):

    def __init__(cls, *args, **kwargs):
        print('meta 6')
        pass

    def __call__(cls, *args, **kwargs):
        # return super().__call__(*args, **kwargs)
        print('meta 8')
        return "abc"

class MetaCat(MetaBase2):
    def __new__(cls, *args, **kwargs):
        print('meta 4')
        obj = super(MetaCat, cls).__new__(cls, *args, **kwargs)
        # obj.__new__(cls)
        obj.__init__(obj)
        return obj
        # return Cat

    def __init__(cls, *args, **kwargs):
        print('meta 5')
        super(MetaCat, cls).__init__(*args, **kwargs)
        return 
        # return "cde"
    def __call__(cls, *args, **kwargs):
        print('meta 7')
        return super().__call__(*args, **kwargs)


class Cat(with_metaclass(MetaCat, object)):
    Name = "cat"

    def __new__(cls):
        """ not called """
        print('Cat self __new__')
        return super().__new__()

    def __init__(self):
        print('Cat self __init__')

    def __call__(cls, *args, **kwargs):
        """ not called """
        print('Cat self __call__')
        return super().__call__(*args, **kwargs)

Cat()