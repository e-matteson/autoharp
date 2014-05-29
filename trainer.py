from music21 import *
#from music21.note import Note

import pprint
import random
import bisect, numpy
import argparse
import pickle

#todo  
#test chords
#allow MC to be conditioned on other parts
#find nice way of storing all the degrees, dict of custom objects?


def trainMC(parts, markov_degree, dt):

    markov_dict = {} #(A, B) => {C: 3, D: 4}
    for part in parts:

        note_keys = []
        for n in part.flat.notesAndRests:
            val = None  #rests will stay as None
            if isinstance(n, note.Note):
                val = n.nameWithOctave
            elif isinstance(n, note.Chord):
                val = n.pitches[0].nameWithOctave #take one pitch, discard the rest

            for t in range(n.quarterLength/dt):
                note_keys.append(val)

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
parser.add_argument("-t", "--timestep")
parser.add_argument("-d", "--degree")
args = vars(parser.parse_args())
info = ("", args["info"])[args["info"] != None]

songs = corpus.getBachChorales()
tenorsongs = []
for song in songs[:25]:
    parsed = corpus.parse(song)
    for i in parsed.getElementsByClass(stream.Part):
        if i.id == u'Tenor':
            tenorsongs.append(parsed)

parts = [song['Tenor'] for song in tenorsongs]

tenor_dict = trainMC(parts, args['degree'], args['timestep'])

parts_dict = {'tenor': tenor_dict}
pickle_dict = {'info': info, 'timestep': timestep, 
               'parts_dict': parts_dict}

pickle.dump(pickle_dict, open(args["file"], "w"))


