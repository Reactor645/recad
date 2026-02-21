import pyttsx3
import keyboard
from ArrestReport import arrestreport
from finemanager import finemanager
from OpenWarrant import warrantmanager
import os
import time  # Nodig voor eventuele sleeps/timing
from LiveDispatch import LiveDispatch
from background import changebackground
engine = pyttsx3.init()
engine.setProperty('volume', 1.0)

# De 'done' variabele is hier niet nodig en kan verwarring veroorzaken.
# We gebruiken de break in de loop.


def start_dispatch_loop():
    print("\n--- Dispatch Console ready ---")
    print("Type 'STOP' to close the dispatch console")
    while True:
        # Wis het scherm om het overzichtelijk te houden (optioneel)
        # os.system('cls' if os.name == 'nt' else 'clear')

        # De input vraag komt binnen de lus te staan
        dispatch_message = input("Send a message to dispatch (arrestmanager, finemanager, warrantmanager or STOP): ").lower()
        if dispatch_message == "arrestmanager":
            print("[DISPATCH]: Opening Arrest Manager...")
            engine.say("10 4, let me open your arrest manager")
            engine.runAndWait()
            # Roep de functie aan om het rapport te maken
            arrestreport()
            time.sleep(1)  # Pauze om gebruiker te laten zien wat er gebeurt
        elif dispatch_message == "background":
            changebackground()

        elif dispatch_message == "finemanager":
            print("[DISPATCH]: Opening Fine Manager...")
            engine.say("10 4, let me open your fine manager")
            engine.runAndWait()
            finemanager()
            time.sleep(1)

        elif dispatch_message == "livedispatch":
            print("[DISPATCH]: starting live dispatching session...")
            LiveDispatch()
            time.sleep(1)

        elif dispatch_message == "warrantmanager":
            warrantmanager()



        elif dispatch_message == "stop":
            print("[DISPATCH]: Console closing, press enter to stop the dispatch console")
            engine.say("Closing dispatch")
            engine.runAndWait()
            break  # Verlaat de while-lus, waardoor de terminal in ReCAD.py de input() toont.

        else:
            print(f"[DISPATCH]: Unknown command: {dispatch_message}. Try again.")
            engine.say("Can you repeat please")
            engine.runAndWait()



# Omdat je de functie in ReCAD.py oproept met 'dispatch.start_dispatch_loop()',
# is er geen 'if __name__ == "__main__":' blok hier nodig.

