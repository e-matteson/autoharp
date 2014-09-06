import sys, re, music21, pickle


def print_note(note, prefix=""):
    print prefix,
    note=note.encode('hex')
    for i in xrange(len(note)):
        sys.stdout.write(note[i])
        if i % 4 == 3:
            print " ",
    print


duration_dict={0x27: .25,
               0x4e: .5, #eighth
               0x69: 2./3, 
               0x76: .75,
               0x9d: 1,  #quarter
               0xec: 1.5,
               0x13b: 2, #half
               0x189: 2.5,
               0x1d8: 3,
               0x276: 4, #whole
               0x2c4: 4.5,
               0x313: 5,
               0x3b1: 6,
               0x44e: 7,
               0x589: 9,
               }
               

def htoi(hexstring):
    return int(hexstring.encode('hex'),16)

def parse(bytestring):
    outer_stream = music21.stream.Stream()
    
    part_names = ['treble', 'alto', 'tenor', 'bass']
        
    part_strings = []
    for i in xrange(len(part_names) - 1):
        part_strings.append(bytestring[bytestring.find(part_names[i]):bytestring.find(part_names[i+1])])

    end_index = bytestring.find('Tempo')
    part_strings += [bytestring[bytestring.find(part_names[-1]):(end_index, None)[end_index == -1]]]

    for part_name, part_string in zip(part_names, part_strings):
        part_stream = parse_part(part_string, part_name)
        part_stream.id = part_name.capitalize() #does this need to be unicode
        outer_stream.insert(0, part_stream)
    return outer_stream

#    music21.converter.freeze(outer_stream, fp=sys.argv[1].replace(".mus", ".mxl"))

def parse_part(bytestring, part):
    print "*********\n"+part
    part_stream = music21.stream.Part()
    note_re = re.compile(".\x40.{12}\xff\xff") #regex for finding notes
    
    num_notes = 0
    chord_note = None

    notes = note_re.findall(bytestring)

    for note in notes:
        print_note(note, str(num_notes)+"\t")
        try:
                #duration stored in bytes 6 and 7 
            duration = duration_dict[htoi(note[6:8])]
        except KeyError:
            print "unknown duration: " + note[6:8].encode('hex')
            print part + ", note # " + str(num_notes)
            print_note(note)
            #sys.exit(1)
            return
            
        if note[0] == "\xff": #Rest
            m21_rest = music21.note.Rest()
            m21_rest.duration.quarterLength=duration
            part_stream.append(m21_rest)
        else: #is note
            pitchclass = htoi(note[0]) % 12
            octave = htoi(note[0]) / 12 - 1
            m21_note = music21.note.Note(quarterLength=duration)
#                m21_note.quarterlength = duration
            m21_note.octave = octave
            m21_note.pitch.pitchClass = pitchclass

            if htoi(note[3]) in (1,5):
#                print "found chord! " + part + " "+str(num_notes)
                chord_note = m21_note
            else:
                if chord_note != None:
                    if duration == chord_note.quarterLength:
                        m21_note=music21.chord.Chord([chord_note, m21_note])
                        chord_note = None
                    else:
                        print "Chord with notes of different durations!"
                        print_note(note)
                part_stream.append(m21_note)

#            if part=='bass' and num_notes < 10:
#                print_note(note)

        num_notes += 1
    print "\nParsing " + f + "\n"
    raw_input()
    return part_stream

import os

for f in os.listdir('songdumps')[::-1]:
    
    file = open("songdumps/"+f, 'rb')
    outer_stream = parse(file.read())

#sf = music21.freezeThaw.StreamFreezer(outer_stream)
#sf.write(fp=sys.argv[1].replace(".mus", ".pkl"))
