import subprocess as sp  # This library helps us run external commands, like converting audio files
import soundfile as sf   # This library helps us read and write sound files
from pedalboard import Pedalboard, Reverb  # These libraries help us add special effects to our music
from math import trunc   # This library helps us with some math stuff
import numpy as np        # This library helps us with numerical operations

# This function takes a music file, adds a slowed and reverb effect, and saves the new music file.
def slowedreverb(audio, output, room_size=0.75, damping=0.5, wet_level=0.08, dry_level=0.2, delay=2, slowfactor=0.08):
    # First, let's check if the input file is already a .wav file.
    filename = audio
    if '.wav' not in audio:
        # If not, we need to convert it to a .wav file.
        print('Audio needs to be .wav! Converting...')
        # We use a tool called ffmpeg to do the conversion.
        sp.call(f'ffmpeg -i "{audio}" tmp.wav', shell=True)
        audio = 'tmp.wav'  # Now, our converted file is called tmp.wav.

    # Let's read the audio file and get some information about it.
    audio, sample_rate = sf.read(audio)

    # Now, we're going to make the audio slower by changing the sample rate.
    # Imagine the music playing slower like a turtle!
    sample_rate -= trunc(sample_rate * slowfactor)

    # Next, we're going to add a reverb effect to our music.
    # We're setting up a special pedalboard with a reverb effect on it.
    board = Pedalboard([Reverb(
        room_size=room_size,
        damping=damping,
        wet_level=wet_level,
        dry_level=dry_level
    )])

    # Now, we're applying the pedalboard (our effects) to the audio.
    effected = board(audio, sample_rate)

    # Let's separate the audio into two channels (left and right).
    channel1 = effected[:, 0]
    channel2 = effected[:, 1]

    # We're going to shift one channel in time to create an echo effect.
    shift_len = delay * 1000  # Imagine delaying one channel, like an echo in a big room!
    shifted_channel1 = np.concatenate((np.zeros(shift_len), channel1[:-shift_len]))

    # Now, let's combine the shifted channel with the original channel.
    combined_signal = np.hstack((shifted_channel1.reshape(-1, 1), channel2.reshape(-1, 1)))

    # Finally, let's save our newly created music with all the effects!
    sf.write(output, combined_signal, sample_rate)

    # Yay! We did it! Let's celebrate by printing a message.
    print(f"converted {filename}")
