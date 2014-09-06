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
        part = song_dict[args['mc_name']]
        note_list = []
        degree = args[args['mc_name']+"_degree"]
        for n in part.flat.notesAndRests:
            val = None  #rests will stay as None
            if isinstance(n, note.Note):
                val = n.nameWithOctave
            elif isinstance(n, note.Chord):
                #TODO: currently take one pitch, discard the rest
                val = n.pitches[0].nameWithOctave 

            #append val repeatedly, based on duration in timesteps
            for t in range(n.quarterLength/args['timestep']):
                note_list.append(val)

        current_key = MarkovKey(tuple(note_list[:degree])) #TODO: currently only condition on self

        #TODO: currently don't generate transition probabilities to the first degree notes of song
        for i in range(degree):
            note_list.pop(0)

        print "Note list: " + repr(note_list)
        print
        while len(note_list) > 0:
            nxt = note_list.pop(0)
            print repr(nxt)
            if not markov_dict.has_key(tuple(current_key)):
                print "First time seeing key " + repr(current_key)
                markov_dict[tuple(current_key)] = {}
            if not markov_dict[tuple(current_key)].has_key(nxt):
                print "First time seeing transition from " + repr(current_key) + " to " + repr(nxt)
                markov_dict[tuple(current_key)][nxt] = 0.

            markov_dict[tuple(current_key)][nxt] += 1.
            current_key = current_key[1:] + [nxt]

    #normalize transition probabilities
    for key, transitions in markov_dict.iteritems():
        total = sum(transitions.values())
        for option, count in transitions.iteritems():
            markov_dict[key][option] = count / total
    return markov_dict

parser = argparse.ArgumentParser(prog="autoharp trainer")
parser.add_argument("--corpus", nargs="*")
parser.add_argument("-f", "--file")
parser.add_argument("-i", "--info")
parser.add_argument("-t", "--timestep")
parser.add_argument("-d", "--degree")
args = vars(parser.parse_args())
info = ("", args["info"])[args["info"] != None]

songs = args["corpus"]
part_names= ["Treble", "Alto","Tenor", "Bass"] #should come from args
song_dicts = []

for song in songs:
    #parsed = converter.parse(song) #For the glorious future in which xml export works
    parsed = pickle.load(song)
    parts=filter(lambda x: x in part_names, map(lambda y: y.id, parsed.getElementsByClass(stream.Part)))
    print parts
    if len(parts) != 4:
        continue
    song_dicts.append({})
    for i in parts:
        if i.id == u'Treble':
            song_dicts[-1]['Treble']=i
        if i.id == u'Alto':
            song_dicts[-1]['Alto']=i
        if i.id == u'Tenor':
            song_dicts[-1]['Tenor']=i
        if i.id == u'Bass':
            song_dicts[-1]['Bass']=i

#config_args = {'mc_name'='Soprano', 'Tenor'=16, 'Soprano'=8, 'timestep'=1./4}

#soprano_mc = trainMC(song_dicts, config_args)


#parts_dict = {'tenor': tenor_mc}

parts_dict = {}
for part in part_names:
    config_args = {'mc_name' : part, part + "_degree" : 16, 'timestep' : 1./4}
    parts_dict[part] = trainMC(song_dicts, config_args)

pickle_dict = {'info': info, 'timestep': 1./4, 
               'parts_dict': parts_dict}

pickle.dump(pickle_dict, open(args["file"], "w"))


