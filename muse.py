import sys, re


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
               

file = open(sys.argv[1], 'rb')

s = file.read()

note_re = re.compile(".\x40")
for part in ['treble', 'alto', 'tenor', 'bass']:
    index = note_re.search(s, s.find(part)).start()
    note = s[index:index+29]
    pitchclass = int(note[0].encode('hex'),16) % 12
    octave = int(note[0].encode('hex'),16) / 12 - 1
    print pitchclass
#    while note data:
 #       parse notes

    print_note(note)
    next


