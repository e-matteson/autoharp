#from music21 import *
import argparse
import pickle

#todo:
#rewrite to work with timesteps, conditioning


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


parser = argparse.ArgumentParser(prog="autoharp")
parser.add_argument("model_file")
parser.add_argument("-i", "--info", action="store_true",)
args = vars(parser.parse_args())


model_file = pickle.load(open(args["model_file"], "r"))
model = model_file['parts_dict']
dt = model_file['timestep']

if args["info"]:
    if model_file["info"] != "":
        print model_file["info"]
    else:
        print "No model info."

print model



random.seed(0) #for debugging
pp = pprint.PrettyPrinter() 


degree=2
dict=trainer('pitch',parts,degree)
out=sampleMC(dict,'pitch',degree)
out.show('text')
out.show()
sp=midi.realtime.StreamPlayer(out)
sp.play()
