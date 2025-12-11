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

# On differentiation
A new note is to be made when the previous character is not in the list of allowed characters: "abcdefglns1234567890.r"

# On special things
Rests are in the following format: "r" followed by a duration in beats
