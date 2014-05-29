from music21 import *
#from music21.note import Note

import pprint
import random
import bisect, numpy
import argparse
import pickle

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

parser = argparse.ArgumentParser(prog="autoharp trainer")
parser.add_argument("corpus", nargs="*")
parser.add_argument("-f", "--file")
parser.add_argument("-i", "--info")
args = vars(parser.parse_args())

dict = {}
info = ("", args["info"])[args["info"] != None]

pickle.dump((info, dict), open(args["file"], "w"))
exit()

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
