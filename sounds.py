import time
from time import sleep

import winsound
import pyttsx3


import pyttsx3
engine = pyttsx3.init()
engine.setProperty("rate", 180)
engine.setProperty('volume', 1.0)

def axon_beep_layered():
    # We bootsen de dubbele toon na door
    # heel snel te wisselen tussen hoog en laag.
    for _ in range(2):
        winsound.Beep(2000, 20) # Hoge toon
        time.sleep(0.03)

def axon_end_shift():
    winsound.Beep(1500, 1000)

