import sys, re


def print_note(note):
    note=note.encode('hex')
    for i in xrange(len(note)):
        sys.stdout.write(note[i])
        if i % 4 == 3:
            print " ",
    print



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


