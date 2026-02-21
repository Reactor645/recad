import time
from time import sleep
import os
import subprocess
import sys
import winsound
import background

# --- IMPORTS VOOR ANDERE MODULES (Zorg dat deze bestanden bestaan) ---
# PyInstaller zal deze automatisch bundelen
from ArrestReport import arrestreport
import dispatch
import ArrestReport
import finemanager
import OpenWarrant
from sounds import *
import keyboard

# --- VARIABELEN ---
passedtime = 0
starttimer = 0
shiftactive = 0
overtime = 0
stopdispatch = 0
callsign = None  # Initializeer callsign globaal
shifttime = 0




ReCAD_art = """
  _____       _____          _____  
 |  __ \     / ____|   /\   |  __ \ 
 | |__) |___| |       /  \  | |  | |
 |  _  // _ \ |      / /\ \ | |  | |
 | | \ \  __/ |____ / ____ \| |__| |
 |_|  \_\___|\_____/_/    \_\_____/ 
                                    
                                    
                                    """

# =========================================================================
# === STARTPUNT FILTER (ESSENTIEEL VOOR SUBPROCESS IN DE .EXE BUNDEL) ===
# =========================================================================
os.system('cls' if os.name == 'nt' else 'clear')
print(ReCAD_art)
print("Created by Reactor Interactive")
sleep(3)
os.system('cls' if os.name == 'nt' else 'clear')
print("Copyright © 2026 Reactor Interactive. All rights reserved.")
sleep(2)
os.system('cls' if os.name == 'nt' else 'clear')

if len(sys.argv) > 1 and sys.argv[1] == 'dispatch':
    # Dit is de dispatch terminal, gestart door het hoofd-CAD.
    print("--- DISPATCH CONSOLE GESTART ---")

    # Roep hier de hoofdloop of functie van de dispatch-module aan.
    # Dit moet de functie zijn die de dispatch-terminal actief houdt.
    if hasattr(dispatch, 'start_dispatch_loop'):
        try:
            dispatch.start_dispatch_loop()
        except Exception as e:
            print(f"Fout tijdens uitvoeren dispatch loop: {e}")
    else:
        print("Fout: De dispatch module heeft geen 'start_dispatch_loop' functie.")

    # Zorg dat de dispatch terminal NIET meteen sluit
    input("\n[DISPATCH]: Druk op ENTER om Dispatch te sluiten...")
    sys.exit()  # Sluit de dispatch terminal af


# =========================================================================

# --- FUNCTIE OM DISPATCH IN NIEUW VENSTER TE STARTEN ---
def start_dispatch_process():
    global callsign
    MODULE_TO_RUN = 'dispatch'

    # Bouw de volledige opdracht als één enkele string voor de 'start'-operator.
    # Dit dwingt Windows om een nieuw venster te openen en daar de .exe in te starten.
    command_str = f'start "Dispatch Console - {callsign}" cmd /k "{sys.executable}" {MODULE_TO_RUN}'

    try:
        # Gebruik shell=True omdat we een complexe shell-commando-string gebruiken
        subprocess.Popen(command_str, shell=True)
        print("[DISPATCH]: Dispatch started in new window.")
    except Exception as e:
        print(f"Error while starting dispatch.{e}")


# --- HOOFDLOGICA VAN HET CAD SYSTEEM ---



print("Connecting to RCPD servers, please wait...")

# Maak de ArrestReports map aan
os.makedirs("ArrestReports", exist_ok=True)


sleep(3)
print("Welcome to ReCAD")
callsign = input("Please enter a callsign: ")
sleep(1)
print("We currently support: ERLC, PSPO and EH")
game = input("What game do you want the CAD for?: ")

print("dayshift = DAY")
print("nightshift = NIGHT")
day_or_night_shift = input("Are you working day or night shifts?: ")

if day_or_night_shift.upper() == "DAY" and game.upper() == "ERLC" or game.upper() == "EH":
    print("Your shift starts at 08:00 and ends at 20:00")
elif day_or_night_shift.upper() == "NIGHT" and game.upper() == "ERLC" or game.upper() == "EH":
    print("Your shift starts at 20:00 and ends at 08:00")
elif day_or_night_shift.upper() == "DAY" and game.upper() == "PSPO":
    shifttime = int(input("Please enter shifttime in minutes: "))
    shifttime = shifttime * 60
    shifttime = str(shifttime)
    print("Your shift is " + shifttime + " seconds long")
    shifttime = int(shifttime)
elif day_or_night_shift.upper() == "NIGHT" and game.upper() == "PSPO":
    shifttime =int(input("Please enter shifttime in minutes: "))
    shifttime = shifttime * 60
    shifttime = str(shifttime)
    print("Your shift is " + shifttime + " seconds long")
    shifttime = int(shifttime)


else:
    print("Invalid value")

print("Please type ShiftStart when starting a shift. The CAD will begin timing your shift!")



shiftstart = input("Ready: ")

if shiftstart == "ShiftStart":
    # Start de dispatch terminal als de shift begint

    start_dispatch_process()
    sleep(1)
    axon_beep_layered()

    shiftactive = 1
    print(shiftactive) #remove
    starttimer = 1
    print("Shift active! Tracking time...")


    # --- SHIFT LOOP ---
    while shiftactive == 1:

        # SHIFT TIMER LOOPT ALS HIJ ACTIEF IS
        if starttimer == 1:
            passedtime += 1

            sleep(1)

            # CHECKT OF SHIFT 12 MINUTEN DUURDE (720 seconden)
            if passedtime == shifttime:
                stopdispatch = 1
                ready_to_end_shift = input("Ready to end the shift? (Y or N): ")

                if ready_to_end_shift.upper() == "Y":
                    print("Shift has ended successfully.")
                    axon_end_shift()
                    passedtime = 0
                    starttimer = 0
                    shiftactive = 0  # dispatch stopt ook

                elif ready_to_end_shift.upper() == "N":
                    print("Overtime started!")
                    overtime = 1
                    starttimer = 0  # timer stopt, maar shift blijft actief
                    shiftactive = 1  # shift blijft actief voor dispatch