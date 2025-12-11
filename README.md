# Music
Plays a song using the Kyle Format for Amazing Music (KFAM for short) file format

# On the "settings" for a song
To write a song make a file (preferably ending in .kfam but thruthfully it does not matter) then in the song file your music should go in the following order:

Line 1: time signature in format \[a\]/\[b\] (a does not matter because measures do not exist)

Line 2: tempo in bpm. Format: \[number\]

Every other line: the actual notes

# On writing notes
The notes should be written in the following format:

Note letter (a-g),

Octave (any number)

Accidental ("n" \[natural\], "s" \[sharp\], or "l" \[flat\] \[The l is just because b, symbol for flat, is taken by the note b and f, short for flat, is taken by the note f\])

Duration (In beats)

Do not get rid of any of these or the notes will not play

# On differentiation
A new note is to be made when the previous character is not in the list of allowed characters: "abcdefglns1234567890.rpm"

# On special things
Rests are in the following format: "r" followed by a duration in beats

Dynamics should follow the note if they exitst (you do not need a seperator) just write a p or f or mp or ffffff etc. right after the note. (These are not a neccessary thing to be added to the note like everything else is)

If you use a "#" it will make everything afterwards a comment (note: if you put a space before the 

# Dependencies
You will need to install numPy https://numpy.org/ as well as sounddevice https://python-sounddevice.readthedocs.io/en/0.5.3/
