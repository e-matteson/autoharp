#The keys in the markov chain will be instances of this.
#
class MarkovKey(object):
    
    #Any part names are acceptable as arguments
    def __init__(self, **kwargs):
        self.partnames = kwargs.keys()
        for i in kwargs.values():
            if not isinstance(i, tuple):
                raise ValueError("Part value must be a tuple of note name strings.")
        self.__dict__.update(kwargs)

    def __eq__(self, other):
        for name in self.partnames:
            if not hasattr(other, name) or getattr(other, name) != getattr(self, name):
                return False
        if self.partnames != other.partnames:
            return False
        return True

    def __hash__(self):
        print reduce(lambda base, new: base.__add__(new), [getattr(self, name) for name in self.partnames], ())
        return hash(reduce(lambda base, new: base.__add__(new), [getattr(self, name) for name in self.partnames], ()))


if __name__ == "__main__":
    a = MarkovKey(tenor = ("A", "B"), bass = ("C",))
    b = MarkovKey(treble = ("C",), bass = ("A", "B"))
    c = MarkovKey(treble = ("C",), tenor = ("B", "A"))
    d = MarkovKey(tenor = ("B", "A"), treble = ("C",))

    dict = {}
    dict[a] = 1
    dict[b] = 2
    dict[c] = 3
    dict[d] = 4

    print dict
    print str(a.__hash__()) + " " + str(b.__hash__())
    print a == b
