import subprocess as sp
import soundfile as sf
from pedalboard import Pedalboard, Reverb
from math import trunc
import numpy as np


# Checking if the file is .wav or not if not converting the file into a .wav file and mentioning that file as temp.wav also initating the main factor 
# to change the song to slowed and reverb
def slowedreverb(audio, output, room_size = 0.75, damping = 0.5, wet_level = 0.08, dry_level = 0.2, delay = 2, slowfactor = 0.08):
    filename = audio
    if '.wav' not in audio:
        print('Audio needs to be .wav! Converting...')
        sp.call(f'ffmpeg -i "{audio}" tmp.wav', shell = True)
        audio = 'tmp.wav'
        
    audio, sample_rate = sf.read(audio)
    sample_rate -= trunc(sample_rate*slowfactor)


# Adding Reverb now