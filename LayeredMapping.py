from collections import MutableMapping
from itertools import chain


class LayeredMapping(MutableMapping):
    """
    >>> x = LayeredMapping( {"a":1, "b":2}, {"b":4, "c":3} )
    >>> x['a']
    1
    >>> x['b']
    2
    >>> x['c']
    3
    >>> sorted(list(x.keys()))
    ['a', 'b', 'c']
    >>> all(key in x.keys() for key in ['a', 'b', 'c'])
    True
    >>> len(x)
    3
    >>> x['e'] = 4
    >>> len(x)
    4
    >>> x['d']
    Traceback (most recent call last):
        ...
    KeyError: 'd'
    >>> del x['b']
    >>> x['b']
    4
    """

    def __init__(self, *maps):
        self.maps = list(maps) or [{}]

    def __missing__(self, key):
        raise KeyError(key)

    def __getitem__(self, key):
        for mapping in self.maps:
            try:
                return mapping[key]
            except KeyError:
                pass
        return self.__missing__(key)

    def __setitem__(self, key, value):
        self.maps[0][key] = value

    def __delitem__(self, key):
        try:
            del self.maps[0][key]
        except:
            raise KeyError("Key not found in the first mapping: %r" % key)

    def __iter__(self):
        return iter(set(chain.from_iterable(self.maps)))

    def __len__(self):
        return len(set(chain.from_iterable(self.maps)))
