from music21 import *
#from music21.note import Note
#from music21.note import Rest
#chord?

import pprint
import random
import bisect, numpy

#todo parametrize, handle chords



def trainMC(chain_type, parts,markov_degree):
    if chain_type=='duration':
        field='quarterLength'
        element_types='notesAndRests'
    elif chain_type=='pitch':
        field='nameWithOctave'
        element_types='notes'
    else:
        error('invalid chain_type')

    markov_dict = {} #(A, B) => {C: 3, D: 4}
    for part in parts:
        measures = part.getElementsByClass('Measure')
        
        note_keys = [(n.__class__.__name__, eval('n.'+field)) 
                         for n in eval('part.flat.'+element_types)]

        current_key = note_keys[:markov_degree]
        for i in range(markov_degree):
            note_keys.pop(0)
    
        while len(note_keys) > 0:
            next = note_keys.pop(0)
        
            if not markov_dict.has_key(tuple(current_key)):
                markov_dict[tuple(current_key)] = {}
            if not markov_dict[tuple(current_key)].has_key(next):
                markov_dict[tuple(current_key)][next] = 0.
        
            markov_dict[tuple(current_key)][next] += 1.
            current_key = current_key[1:] + [next]
        
    #normalize transition probabilities
    for key, transitions in markov_dict.iteritems():
        total = sum(transitions.values())
        for option, count in transitions.iteritems():
            markov_dict[key][option] = count / total
    return markov_dict


def sampleMC(markov_dict, chain_type, markov_degree,sequence=None):
    note_names = ["A3", "C4"] #for testing duration generation
    if sequence is None:
        output = stream.Stream()
    else:
        output = sequence

    if chain_type=='duration':
        field='quarterLength'
    elif chain_type=='pitch':
        field='nameWithOctave'
    else:
        error('invalid chain_type')

    note1 = note.Note(note_names[0])
    note1.quarterLength = 2.0
    note2 = note.Note(note_names[1])
    note2.quarterLength = 2.0
    output.append(note1)
    output.append(note2)

    for i in range(20):
        matching_key = tuple([(output[j].__class__.__name__, eval('output[j].'+field))
                              for j in range(-markov_degree,0)])

        options, weights = zip(*markov_dict[matching_key].items())
        r = random.random()
        selected_key = options[bisect.bisect(list(numpy.cumsum(weights)), r)]
        next_note = eval('note.'+selected_key[0]+'()') #construct Note() or Rest()
        exec('next_note.'+field+'=selected_key[1]')
        output.append(next_note)
    return output


random.seed(0) #for debugging
pp = pprint.PrettyPrinter() 

songs = corpus.getBachChorales()
tenorsongs = []
for song in songs[:25]:
    parsed = corpus.parse(song)
    for i in parsed.getElementsByClass(stream.Part):
        if i.id == u'Tenor':
            tenorsongs.append(parsed)

parts = [song['Tenor'] for song in tenorsongs]

#note_offsets = [measure.offsetMap for measure in foo.tenorsongs[0]['Tenor'].getElementsByClass('Measure')]


 # 'duration' or 'pitch'
degree=2
dict=trainMC('pitch',parts,degree)
out=sampleMC(dict,'pitch',degree)
out.show('text')
out.show()
sp=midi.realtime.StreamPlayer(out)
sp.play()
