import sys, re

file = open(sys.argv[1], 'rb')

s = file.read()

note_re = re.compile(".\x40")
for part in ['treble', 'alto', 'tenor', 'bass']:
    index = note_re.search(s, s.find(part)).start()
    note = s[index:index+29]
#    while note data:
 #       parse notes
    note=note.encode('hex')
    for i in xrange(len(note)):
        sys.stdout.write(note[i])
        if i % 4 == 3:
            print " ",
    print
    next

