from music21 import *
#from music21.note import Note

import pprint
import random
import bisect, numpy
import argparse
import pickle
from libharp import MarkovKey

#todo  
#test chords
#allow MC to be conditioned on other parts
#find nice way of storing all the degrees, dict of custom objects?


def trainMC(song_dicts, args):
    

    markov_dict = {}
    for song_dict in song_dicts:
        for name, part in song_dict.items():
            note_list = []
            for n in part.flat.notesAndRests:
                val = None  #rests will stay as None
                if isinstance(n, note.Note):
                    val = n.nameWithOctave
                elif isinstance(n, note.Chord):
                    #take one pitch, discard the rest
                    val = n.pitches[0].nameWithOctave 

                #append val repeatedly, based on duration in timesteps
                for t in range(n.quarterLength/args['timestep']):
                    note_list.append(val)

            current_key = MarkovKey(tuple(note_list[:markov_degree]))
            for i in range(markov_degree):
                note_list.pop(0)

            while len(note_list) > 0:
                next = note_list.pop(0)

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
part_names= ["Soprano", "Alto","Tenor", "Bass"]
song_dicts = []

for song in songs[:25]:
    parsed = corpus.parse(song)
    
    parts=filter(lambda x: x in part_names, parsed.getElementsByClass(stream.Part))
    if len(parts) != 4:
        continue
    song_dicts.append({})
    for i in parts:
        if i.id == u'Soprano': #treble
            song_dicts[-1]['Soprano']=i
        if i.id == u'Alto':
            song_dicts[-1]['Alto']=i
        if i.id == u'Tenor':
            song_dicts[-1]['Tenor']=i
        if i.id == u'Bass':
            song_dicts[-1]['Bass']=i

config_args = {'mc_name'='Soprano', 'Tenor'=16, 'Soprano'=8, 'timestep'=1./4}

soprano_mc = trainMC(song_dicts, config_args)

mc_dict = {'tenor': tenor_mc}
pickle_dict = {'info': info, 'timestep': timestep, 
               'mc_dict': mc_dict}

pickle.dump(pickle_dict, open(args["file"], "w"))


