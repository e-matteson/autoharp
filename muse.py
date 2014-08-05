import sys, re, music21


def print_note(note):
    note=note.encode('hex')
    for i in xrange(len(note)):
        sys.stdout.write(note[i])
        if i % 4 == 3:
            print " ",
    print


duration_dict={0x27: .256,
               0x4e: .5, #eighth
               0x9d: 1,  #quarter
               0xec: 1.5,
               0x13b: 2, #half
               0x1d8: 3,
               0x276: 4, #whole
               0x313: 5,
               0x3b1: 6
               }
               

def htoi(hexstring):
    return int(hexstring.encode('hex'))

def parse(bytestring):
    outer_stream = music21.stream.Stream()
    
    note_re = re.compile(".\x40")
    for part in ['treble', 'alto', 'tenor', 'bass']:
        part_stream = music21.stream.Part()
        part_stream.id = part.capitalize() #does this need to be unicode?
        index = note_re.search(bytestring, bytestring.find(part)).start()
        note = bytestring[index:index+29]
        while note[-1] == "\x64":
            try:
                duration = duration_dict[htoi(note[8:10])]
            except KeyError:
                print "unknown duration! " + note[8:10].encode('hex')
                exit(1)

            if note[0] == "\xff": #Rest
                m21_rest = music21.note.Rest()
                m21_rest.duration.quarterlength = duration

                part_stream.append(m21_rest)
            else:
                pitchclass = htoi(note[0]) % 12
                octave = htoi(note[0]) / 12 - 1
            
                m21_note = music21.note.Note()
                m21_note.quarterlength = duration
                m21_note.octave = octave
                m21_note.pitch.pitchClass = pitchclass

                part_stream.append(m21_note)

            print_note(note)
            index += 29
            note = bytestring[index:index+29]
        outer_stream.append(part_stream)
    music21.converter.freeze(outer_stream, fp=sys.argv[1].replace(".mus", ".mxl"))


file = open(sys.argv[1], 'rb')
parse(file.read())
