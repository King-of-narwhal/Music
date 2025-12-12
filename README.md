# Music
Plays a song using the Kyle Format for Amazing Music (KFAM for short) file format

# On the "settings" for a song
To write a song make a file (preferably ending in .kfam but thruthfully it does not matter) then in the song file your music should go in the following order:

Line 1: time signature in format \[a\]/\[b\] (a does not matter because measures do not exist)

Line 2: key signature

Line 3: tempo in bpm. Format: \[number\]

Every other line: the actual notes

# On writing notes
The notes should be written in the following format:

Things you can't get rid of:

Octave (any number)

Note letter (a-g),

Duration (In beats)

Things you can't get rid of:

Accidental ("n" \[natural\], "s" \[sharp\], or "l" \[flat\] \[The l is just because b, symbol for flat, is taken by the note b and f, short for flat, is taken by the note f\])

Dynamic (the more f's the more volume, the more p's the less volume, if you type an m it will divide it by 1.5 if forte or multiply by 1.5 if forte)

# On differentiation
A new note is to be made when the previous character is not in the list of allowed characters: "abcdefglns1234567890.rpm"

# On special things
Rests are in the following format: "r" followed by a duration in beats

If you use a "#" it will make everything afterwards a comment (note: if you put a space before the 

# Dependencies
You will need to install numPy https://numpy.org/ as well as sounddevice https://python-sounddevice.readthedocs.io/en/0.5.3/
