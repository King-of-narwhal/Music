import math
import numpy
import sounddevice
import time

song = input("What is the file name for the song you would like? ")
with open(song, "r") as file:
    user_txt = file.read()
# Exponintially increases volume so our ears can detect it
volume = float(input("Volume (0-20]: "))
if volume <= 0.0:
    volume = 0.1
elif volume > 20.0:
    volume = 20.0
volume = volume ** 2
def real_note(f0, duration, volume, instrument):
    sample_rate = 44100
    t = numpy.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    wave = numpy.zeros_like(t)
    harmonics = 10
    instrument_harmonics = {
            "euphonium":[1.0, 0.7, 0.5, 0.3, 0.2],
            "trombone":[1.0, 0.7, 0.5, 0.3, 0.2],
            "trumpet":[1.0, 0.6, 0.4, 0.3, 0.2],
            "french horn":[1.0, 0.6, 0.4, 0.25, 0.15],
            "tuba":[1.0, 0.7, 0.5, 0.3, 0.2],
            "clarinet":[1.0, 0.0, 0.8, 0.0, 0.5],
            "flute":[1.0, 0.05, 0.02, 0.01, 0.005],
            "piano":[1.0, 0.8, 0.6, 0.5, 0.4]
    }
    instrument_num = -1
    if instrument in "0123456789":
        instrument_list = list(instrument_harmonics.keys())
        instrument_name = instrument_list[int(instrument)]
    else:
        instrument_name = instrument.lower()
    weights = instrument_harmonics[instrument_name]
    #ADSR envelope
    #"Settings"
    attack = 0.01 #0.01
    decay = 0.1 #0.1
    sustain_level = 0.7 #0.7 
    release = 0.1 #0.1

    env = numpy.ones_like(t)
    attack_samples = int(sample_rate * attack)
    decay_samples = int(sample_rate * decay)
    release_samples = int(sample_rate * release)
    sustain_samples = len(t) - attack_samples - decay_samples - release_samples
    env[:attack_samples] = numpy.linspace(0, 1, attack_samples)
    env[attack_samples:attack_samples+decay_samples] = numpy.linspace(1, sustain_level, decay_samples)
    env[attack_samples+decay_samples:attack_samples+decay_samples+sustain_samples] = sustain_level
    env[-release_samples:] = numpy.linspace(sustain_level, 0, release_samples)

    for i, weight in enumerate(weights):
        wave += weight * numpy.sin(2 * numpy.pi * (i+1) * f0 * t)
    wave *= env
    wave /= numpy.max(numpy.abs(wave))
    wave *= volume
    return wave
instrument = input("Choose an instrument, spell it out or take it from this list: euphonium (0), trombone (1), trumpet (2), french horn (3), tuba (4), clarinet (5), flute (6), piano (7): ")
def sine_wave(frequency, length, volume):
    sample_rate = 44100
    t = numpy.linspace(0, length, int(44100 * length), endpoint=False)
    return volume * numpy.sin(2 * numpy.pi * frequency * t) #Generates the frequency (don't ask how this works, I just googled it)
def note_to_pitch(note, accidental_array, key): #Note is string in format [octave][letter][duration][accidental][dynamic]
    progress = 0                                                                                    #These two are optional
    #Find the letter, octave, accidental, length and dynamic of the note
    i = 0
    while i <= len(note):
        #Get Duration, accidental & dynamic
        if progress == 2:
            length = ""
            accidentals = False
            dynamics = False
            accidental = ""
            dynamic = ""
            for j in range(i - 1, len(note)):
                if note[j] in "lsn":
                    accidentals = True
                if note[j] in "pfm":
                    dynamics = True
                    accidentals = False
                if accidentals:
                    accidental += note[j]
                elif dynamics:
                    dynamic += note[j]
                else:
                    length += note[j]
            length = float(length)
            i = j + 1
        #Get letter
        elif progress == 1:
            letter = note[i - 1]
            progress += 1
        #Get octave
        elif progress == 0:
            j = i
            octave = ""
            while note[j] not in "abcdefg":
                octave += note[j]
                j += 1
            octave = int(octave)
            progress += 1
            i = j
        i += 1
    if accidental == "":
        found = False
        for i in range(len(accidental_array)):
            if accidental_array[i][0] == letter:
                accidental = accidental_array[i][1]
                found = True
        if not found:
            for i in range(0, len(key), 2):
                if key[i] == letter:
                    accidental = key[i + 1]
                    found = True
        if not found:
            accidental = "n"
    else:
        accidental_array2 = []
        #Gets rid of any previous accidentals of the same letter
        for i in range(len(accidental_array)):
            if accidental_array[i][0] != letter:
                accidental_array2.append(accidental_array[i])
        accidental_array2.append(letter + accidental) #Adds the new accidental
        accidental_array = accidental_array2
    print("Octave: " + str(octave) + ", letter: " + letter + ", duration: " + str(length) + ", accidental: " + accidental + ", dynamic: " + dynamic)
    #Goes up a note then makes it flat
    flats = "degab"
    notes = "cdefgab"
    if accidental == "s":
        accidental = "l"
        for i in range(len(notes)):
            if notes[i] == letter:
                flat = False
                flat_note_num = i + 1
                if flat_note_num == len(notes):
                    flat_note_num = 0
                    octave += 1
                #Checks to see if the note should not be sharp and if so moves it up a note then makes it natural
                for j in range(len(flats)):
                    if notes[flat_note_num] == flats[j]:
                        flat = True
                if flat:
                    letter2 = notes[flat_note_num]
                else:
                    accidental = "n"
                    octave -= 1
                    letter2 = notes[flat_note_num]
        letter = letter2
    #Checks to see if the note should not be flat and if so moves it down a note then makes it natural
    elif accidental == "l":
        flat = False
        for i in range(len(flats)):
            if flats[i] == letter:
                flat = True
        if flat == False:
            for i in range(len(notes)):
                if letter == notes[i]:
                    letter2 = notes[i - 1]
            accidental = "n"
            letter = letter2
            if letter == "b":
                octave -= 1
    #Finds every note
    all_notes = []
    for i in range(len(notes)):
        for j in range(len(flats)):
            if flats[j] == notes[i]:
                all_notes.append(notes[i] + "l")
        all_notes.append(notes[i] + "n")
    semitones = 0
    #Makes a special case for if it is already a4
    if letter == "a" and octave == 4 and accidental == "n":
        hertz = 440
    #Calculates number of semitones if it has to count up
    elif octave < 5 and letter != "b" and letter != "a" or letter == "a" and accidental == "l" or letter == "a" and octave < 4 or letter == "b" and octave < 4:
        start = False
        for i in range(octave, 5):
            for j in range(len(all_notes)):
                if i == octave:
                    #print(all_notes[j] + ", " + letter + accidental)
                    if all_notes[j] == (letter + accidental):
                        start = True
                if start:
                    if all_notes[j] == "an" and i == 4:
                        start = False
                    semitones += 1
        semitones -= 1
        semitones = 0 - semitones
    #Calculates number of semitones if it has to count down
    else:
        start = False
        for i in range(4, octave + 1):
            for j in range(len(all_notes)):
                if i == 4:
                    if all_notes[j] == "an":
                        start = True
                if all_notes[j] == (letter + accidental) and i >= octave:
                    start = False
                if start == True and i != 4 or start == True and all_notes[j] != "an":
                    semitones += 1
        semitones += 1
    if letter != "a" or octave != 4 or accidental != "n":
        hertz = 440 * (2 ** (semitones / 12))
    return hertz, length, dynamic, accidental_array
def sound_play(sin_wave):
    sounddevice.play(sin_wave, 44100)
    sounddevice.wait() #Waits for the frequency to be played
#notes = ["f4n1","e4n1","f4n1","d4n1"]
#for i in range(len(notes)):
#    play_note(notes[i])
pitches = []
lines = 0
i = 0
accidentals = []
allowed = "abcdefglns-1234567890.rpm#"
notes = []
string = ""
key = ""
tag = False
while i < len(user_txt):
    if user_txt[i] == "\n":
        lines += 1
    #If lines = 0, copies characters before slash into time signature 1 and characters after into time signature 2
    if lines == 0:
        char = ""
        j = i
        time1 = ""
        time2 = ""
        slash = False
        while char != "\n":
            char = user_txt[j]
            if char == "/":
                slash = True
            else:
                if slash:
                    if char != "\n":
                        time2 += char
                else:
                    time1 += char
            j += 1
        time1 = int(time1)
        time2 = int(time2)
        i = j - 2 #Skips ahead
    #If lines = 1, copies current line into key signature
    elif lines == 1:
        char = ""
        j = i + 1
        chars = 1
        while char != "\n":
            char = user_txt[j]
            if char != "\n":
                key += char
            j += 1
            chars += 1
        i = j - 2 #Skips ahead
    #If lines = 2, copies current line into bpm
    if lines == 2:
        char = ""
        j = i + 1
        bpm = ""
        while char != "\n":
            char = user_txt[j]
            if char != "\n":
                bpm += char
            j += 1
        i = j - 1
        lines += 1
        bpm = int(bpm) #Makes bpm an integer
    #If lines >= 3 it's gonna add things to notes
    elif lines >= 3:
        char = user_txt[i]
        if char == "#":
            tag = True
        if char == "\n":
            tag = False
        if tag == False:
            allow = False
            for j in range(len(allowed)):
                if allowed[j] == char:
                    allow = True
            #Continues making the current note
            if allow:
                string += char
            #Appends the note to notes array if it found something it doesn't allow
            else:
                #Sets a flag for next measure
                if char == "\n":
                    string += "i"
                if char != " " or user_txt[i + 1] != "#":
                    notes.append(string)
                    string = ""
    i += 1

bpm *= 4 / time1

#Builds all the sine waves first so when notes are played it does not have to do as much calculating so it doesn't get behind
waves = []
dynamics = "mf"
F = 2.5
P = 0.5
volume2 = math.sqrt(2) / 4
accidental_array = []
notes2 = []
for i in range(len(notes)):
    note = notes[i]
    if i > 0:
        if notes[i - 1][len(notes[i - 1]) - 1] == "i":
            accidental_array = []
    if note[len(note) - 1] == "i":
        note = ""
        for j in range(len(notes[i]) - 1):
            note += notes[i][j]
    if notes[i][0] == "r":
        waves.append(note)
    else:
        #Gets rid of the i at the end if there is one
        hertz, duration, dynamics, accidental_array = note_to_pitch(note, accidental_array, key)
        mezo = False
        f = False
        p = False
        fs = 0
        if dynamics != "":
            volume2 = math.sqrt(2)
            #Detects if it is mezo
            if dynamics[0] == "m":
                mezo = True
            for i in range(len(dynamics)):
                # Takes the root of the volume so our ears can detect it (Has a plus one and minus one because I don't want the volume to go up when volume2 is less than one)
                if dynamics[i] == "p":
                    p = True
                    volume2 = math.sqrt(volume2 + 1) - 1
                # Takes the square of the volume so our ears can detect it (Has a plus one and minus one because I don't want the volume to go down when volume2 is less than one)
                elif dynamics[i] == "f":
                    f = True
                    if fs <= 6:
                        volume2 = (volume2 + 1) ** 2 - 1
                    f += 1
            #If the dynamic is mezo, make it closer to the opposite dynamic
            if mezo:
                if f:
                    volume2 /= 1.5
                if p:
                    volume2 *= 1.5
            #Makes it quieter
            volume2 /= 4
        duration *= 60 / bpm
        if duration < 0.11:
            duration = 0.11
        wave = real_note(hertz, duration, volume * volume2, instrument)
        waves.append(wave)
    notes2.append(note)

#Plays all the sounds! (Finally)
for i in range(len(waves)):
    print(notes2[i])
    if waves[i][0] == "r":
        duration = ""
        for j in range(1, len(notes2[i])):
            duration += notes2[i][j]
        duration = 60 / bpm * float(duration)
        time.sleep(duration)
    else:
        sound_play(waves[i])
