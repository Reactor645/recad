# dispatch.py

from ArrestReport import arrestreport
from OpenWarrant import load_warrants
from finemanager import finemanager
import os
import time  # Nodig voor eventuele sleeps/timing
import OpenWarrant
from OpenWarrant import load_warrants


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
            # Roep de functie aan om het rapport te maken
            arrestreport()
            time.sleep(1)  # Pauze om gebruiker te laten zien wat er gebeurt

        elif dispatch_message == "finemanager":
            print("[DISPATCH]: Opening Fine Manager...")
            # Roep de functie aan om de boete te maken
            finemanager()
            time.sleep(1)

        elif dispatch_message == "warrantmanager":
            print("[DISPATCH]: Opening warrant Manager...")
            # Roep de functie aan om de boete te maken
            load_warrants()
            time.sleep(1)

        elif dispatch_message == "stop":
            print("[DISPATCH]: Console closing, press enter to stop the dispatch console")
            break  # Verlaat de while-lus, waardoor de terminal in ReCAD.py de input() toont.

        else:
            print(f"[DISPATCH]: Unknown command: {dispatch_message}. Try again.")

# Omdat je de functie in ReCAD.py oproept met 'dispatch.start_dispatch_loop()',
# is er geen 'if __name__ == "__main__":' blok hier nodig.

start_dispatch_loop()