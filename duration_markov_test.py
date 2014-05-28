from music21 import *
import pprint
import random
import bisect, numpy

songs = corpus.getBachChorales()

tenorsongs = []
for song in songs[:25]:
    parsed = corpus.parse(song)
    for i in parsed.getElementsByClass(stream.Part):
        if i.id == u'Tenor':
            tenorsongs.append(parsed)

parts = [song['Tenor'] for song in tenorsongs]

#note_offsets = [measure.offsetMap for measure in foo.tenorsongs[0]['Tenor'].getElementsByClass('Measure')]

markov_degree = 2
markov_dict = {} #(A, B) => {C: 3, D: 4}

for part in parts:
    measures = part.getElementsByClass('Measure')
    notes = []
    for m in measures:
        notes += [notee.quarterLength for notee in m.getElementsByClass('Note')]
    
    current_key = notes[:markov_degree]
    for i in range(markov_degree):
        notes.pop(0)
    
    while len(notes) > 0:
        next = notes.pop(0)
        
        if not markov_dict.has_key(tuple(current_key)):
            markov_dict[tuple(current_key)] = {}
        if not markov_dict[tuple(current_key)].has_key(next):
             markov_dict[tuple(current_key)][next] = 0.0
        
        markov_dict[tuple(current_key)][next] += 1.0
        current_key = current_key[1:] + [next]

pp = pprint.PrettyPrinter() 
pp.pprint(markov_dict)
        
#normalize
for key, transitions in markov_dict.iteritems():
    total = sum(transitions.values())
    cdf = 0.0
    for notee, count in transitions.iteritems():
        cdf += count / total
        markov_dict[key][notee] = cdf



output = stream.Stream()
note1 = note.Note("A")
note1.quarterLength = 1.0
note2 = note.Note("C")
note2.quarterLength = 1.0
output.append(note1)
output.append(note2)

notenames = ["A", "C"]
for i in range(20):
    r = random.random()
    transition = markov_dict[(output[-2].quarterLength, output[-1].quarterLength)]
    next_note = note.Note(notenames[i % 2])
    durations, weights = zip(*transition.items())
    next_note.quarterLength = durations[bisect.bisect(list(numpy.cumsum(weights)), r)]
    output.append(next_note)
    
