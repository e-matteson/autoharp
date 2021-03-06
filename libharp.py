#The keys in the markov chain will be instances of this.
#
class MarkovKey(object):
    
    #takes {'any part name': (note1, note2,...)}
    def __init__(self, args):
        self.partnames = args.keys()
        for i in args.values():
            if not isinstance(i, tuple):
                raise ValueError("right side must be a tuple of note name strings.")
        self.__dict__.update(args)

    def __eq__(self, other):
        for name in self.partnames:
            if not hasattr(other, name) or getattr(other, name) != getattr(self, name):
                return False
        if self.partnames != other.partnames:
            return False
        return True

    def __hash__(self):
        return hash(reduce(lambda base, new: base.__add__(new), [getattr(self, name) for name in self.partnames], ()))


class MarkovNote(object):
    def __init__(self, name, is_end):
        #takes note name (str), and whether its the last timestep of note (bool) 
        self.name = name
        self.is_end = is_end

    def __eq__(self, other):
        return self.name == other.name and self.is_end == other.is_end
        
    def __hash__(self):
        return hash(self.name+str(self.is_end))


if __name__ == "__main__":
    a = MarkovKey({'tenor':("A", "B"), 'bass':("C",)})
    b = MarkovKey({'treble':("C",), 'bass':("A", "B")})
    c = MarkovKey({'treble':("C",), 'tenor':("B", "A")})
    d = MarkovKey({'tenor':("B", "A"), 'treble':("C",)})

    dict = {}
    dict[a] = 1
    dict[b] = 2
    dict[c] = 3
    dict[d] = 4

    print dict
    print str(a.__hash__()) + " " + str(b.__hash__())
    print a == b
