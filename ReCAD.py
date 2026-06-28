import time
from colorama import Fore, Back, Style, init
import os
from datetime import datetime
import speech_recognition as sr
import rapidfuzz
import keyboard
import winsound
import sys
import json
from recad_online import *
import random
from pypresence import Presence
import configparser


def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)

    internal_path = os.path.join('.', '_internal', relative_path)
    if os.path.exists(internal_path):
        return internal_path

    return os.path.join('.', relative_path)


init(autoreset=True)

os.system('cls')
officer_status = "10-7 out of service"
listening = False
recognizer = sr.Recognizer()
microphone = sr.Microphone()
suspect_database = "database.json"
config = configparser.ConfigParser()
config.read("recad.ini")
listening_is_allowed = True

ReCAD_art = r"""
_____       _____          _____  
|  __ \     / ____|   /\   |  __ \ 
| |__) |___| |       /  \  | |  | |
|  _  // _ \ |      / /\ \ | |  | |
| | \ \  __/ |____ / ____ \| |__| |
|_|  \_\___|\_____/_/    \_\_____/ 


                                    """

License_text = """
Copyright © 2026 Reactor Interactive. All rights reserved.

This software, including all source code, design, and assets used in ReCAD, 
may not be copied, distributed, or used for commercial purposes without 
the express written permission of the copyright holder.

Personal use is allowed, but redistribution or commercial exploitation 
is strictly prohibited without authorization.

For inquiries regarding licensing, please contact: reactor645zakelijk@gmail.com or go to the official ReCAD site at: https://recadofficial.netlify.app
"""

CLIENT_ID = "1518992162514010276"

if config["Extras"]["discord_rich_presence"] == "Yes":

    RPC = Presence(CLIENT_ID)
    try:
        RPC.connect()

        RPC.update(
            state="Using ReCAD",
            details="Patrolling with ReCAD",
            large_image="recadlogo",
            large_text="ReCAD",
            start=time.time(),
            buttons=[
                {
                    "label": "Site",
                    "url": "https://recadofficial.netlify.app"
                }
            ]
        )


    except Exception as e:
        pass
else:
    pass




#DO NOT TOUCH ANYTHING ABOVE ME! THINGS MIGHT CRASH IF YOU DON'T KNOW WHAT YOU'RE DOING AND RECAD WON'T WORK ANYMORE!!!

audiofolder = None

PTT_button = config["General"]["PTT_button"]
Type_button = config["General"]["type_button"]
Panic_button = config["General"]["panic_button"]

if config["General"]["voice"] == "female":
    audiofolder = "audio_female"
elif config["General"]["voice"] == "male":
    audiofolder = "audio_male"

MDT_COMMANDS = {
    "10-8 available": {
        "keywords": ["ten eight", "available", "status eight", "10-8", "108"],
        "audio": resource_path(audiofolder + "/available.wav")
    },
    "10-11 traffic stop": {
        "keywords": ["ten eleven", "traffic stop", "pulling over", "10-11", "1011"],
        "audio": resource_path(audiofolder + "/traffic_stop.wav")
    },
    "10-23 on scene": {
        "keywords": ["ten twenty three", "on scene", "arrived", "10-23", "1023"],
        "audio": resource_path(audiofolder + "/onscene.wav")
    },
    "creating arrest report": {
        "keywords": ["arrest report, arrest, manager"],
        "audio": resource_path(audiofolder + "/tenfour.wav")
    },
    "PANIC BUTTON PRESSED": {
        "keywords": ["code 99", "10-33", "1033", "10 33", "ten thirty three"],
        "audio": resource_path(audiofolder + "/panic.wav")
    },
    "creating fine": {
        "keywords": ["fine", "fine manager"],
        "audio": resource_path(audiofolder + "/tenfour.wav")
    },
    "starting shift": {
        "keywords": ["starting shift", "10-41", "10 41", "1041", "ten forty one"],
        "audio": resource_path(audiofolder + "/shiftstart.wav")
    },
    "ending shift": {
        "keywords": ["ending shift", "10-42", "10 42", "1042", "ten forty two"],
        "audio": resource_path(audiofolder + "/shiftend.wav")
    },
    "connecting to ReCAD online": {
        "keywords": ["connect"],
        "audio": None
    },
    "starting a ReCAD online host": {
        "keywords": ["host", "start server"],
        "audio": None
    },
    "sending radio traffic": {
        "keywords": ["dispatch"],
        "audio": resource_path(audiofolder + "/thisisdispatch.wav")
    },
    "code 4": {
        "keywords": ["code 4", "code four"],
        "audio": resource_path(audiofolder + "/code4.wav")
    },
    "10-6, busy": {
        "keywords": ["ten six", "10-6", "106", "10 6"],
        "audio": resource_path(audiofolder + "/tensix.wav")
    },
}

#You can edit the things above me like you want. BUT only touch the parts AFTER the =. And keep the "", only change the letter or number like you want it to work!!!

#Startup code. Not required to edit unless to change dates or something.

print(Fore.BLUE + ReCAD_art)
print(Fore.BLUE + "Developed by Reactor Interactive")
time.sleep(2)
os.system('cls')
print(Fore.BLUE + "© Reactor Interactive 2026. All rights reserved | Read license.txt for more info")
with open("license.txt", "w") as file:
    file.write(License_text)
time.sleep(2)
os.system('cls')

def draw_dashboard():
    os.system('cls')
    print("================================================================")
    print(f"unit: {callsign} --- status: {officer_status}")
    print("================================================================")
    print(f"Press {PTT_button.upper()} to talk to dispatch, press {Type_button.upper()} to type")

def arrest_report_manager():
    listening_is_allowed = False
    os.system('cls')
    print("============================")
    print(f"{callsign} ARREST REPORT MANAGER")
    print("============================")

    charges = []
    items = []

    arrestee_name = input("Name of arrestee: ")
    arresting_officer_name = input("Name of the arresting officer: ")

    while True:
        charge = input("Enter a charge the suspect has committed (Type done when done) \n >>> ")
        if charge.lower() == "done":
            break
        charges.append(charge)

    while True:
        found_item = input("Enter an item that suspect had on him during arrest (Type done when done) \n >>> ")
        if found_item.lower() == "done":
            break
        items.append(found_item)

    print(f"[{dispatchname}] Entering data, please wait...")

    os.makedirs("arrest reports", exist_ok=True)

    titleline = "============================ \n"
    title = "POLICE ARREST REPORT \n"
    arrestee = f"ARRESTEE: {arrestee_name} \n"
    arrestingofficer = f"ARREST OFFICER: {arresting_officer_name} \n"


    convictedcharges = "CHARGES: " + ", ".join(charges) + "\n"
    founditems = "FOUND ITEMS: " + ", ".join(items) + "\n"

    with open("arrest reports/" + arrestee_name + ".txt", "w") as file:
        file.write(titleline)
        file.write(title)
        file.write(titleline)
        file.write(datetime.now().strftime("%m/%d/%Y %I:%M:%S %p"))
        file.write("\n")
        file.write(arrestee)
        file.write(arrestingofficer)
        file.write(convictedcharges)
        file.write(founditems)

    print(f"[{dispatchname}] Finished")
    with open("shiftlog.txt", "a") as file:
        file.write(datetime.now().strftime("%m/%d/%Y %I:%M:%S %p") + " " + callsign + " Created arrest report\n")
    add_data_to_database(arrestee_name, charges, False)
    time.sleep(0.5)
    draw_dashboard()
    listening_is_allowed = True

def fine_manager():
    listening_is_allowed = False
    os.system('cls')
    print("================================================================")
    print(f"{callsign} FINE MANAGER")
    print("================================================================")

    fined_person_name = input("Name of fined person: ")
    officer_name = input("Name of officer: ")
    charge = input("Reason for fine: ")
    amount = input("Amount charged: ")

    print("Printing ticket...")

    os.makedirs("fines", exist_ok=True)

    with open(f"fines/{fined_person_name}.txt", "w") as file:

        file.write("======================\n")
        file.write("POLICE FINE\n")
        file.write("======================\n")
        file.write(datetime.now().strftime("%m/%d/%Y %I:%M:%S %p"))
        file.write("\n")
        file.write(f"FINED PERSON: {fined_person_name} \n")
        file.write(f"OFFICER: {officer_name} \n")
        file.write(f"CHARGED WITH: {charge} \n")
        file.write(f"AMOUNT CHARGED: {amount} \n")
        file.write("\n")

    print(f"[{dispatchname}] Finished")
    with open("shiftlog.txt", "a") as file:
        file.write(datetime.now().strftime("%m/%d/%Y %I:%M:%S %p") + " " + callsign + " Created fine\n")
    add_data_to_database(fined_person_name, charge, False)
    fine_packet = {
        "suspect": fined_person_name,
        "amount": amount,
    }
    send_data("FINE", fine_packet)
    time.sleep(0.5)
    draw_dashboard()
    listening_is_allowed = True

def add_data_to_database(name, charge, wanted):
    if os.path.exists(suspect_database):
        with open(suspect_database, "r") as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError:
                data = {}
    else:
        data = {}

    if name not in data:
        data[name] = []

    add_person = {
        "name": name,
        "charge": charge,
        "wanted": wanted,
    }

    data[name].append(add_person)

    with open(suspect_database, "w") as file:
        json.dump(data, file, indent=4)

def check_for_panic():
    if keyboard.is_pressed(Panic_button):
        print("PANIC BUTTON PRESSED")

        winsound.PlaySound(
            resource_path("audio/panic.wav"),
            winsound.SND_FILENAME | winsound.SND_ASYNC
        )

        while keyboard.is_pressed(Panic_button):
            time.sleep(0.01)


def check_for_text():
    if keyboard.is_pressed(Type_button):

        time.sleep(0.2)

        input_text = input(f"[{dispatchname}] Go ahead with radio traffic: ")

        if not input_text.strip():
            return

        final_text = input_text.lower().strip()

        text_best_status = None
        text_highest_score = 0
        text_selected_audio = None


        for status, data in MDT_COMMANDS.items():
            for option in data["keywords"]:
                text_score = rapidfuzz.fuzz.partial_ratio(option, final_text)

                if text_score > text_highest_score:
                    text_highest_score = text_score
                    text_best_status = status
                    text_selected_audio = data["audio"]

        if text_highest_score >= 75 and text_best_status:
            global officer_status
            officer_status = text_best_status

            if text_selected_audio:
                winsound.PlaySound(text_selected_audio, winsound.SND_FILENAME | winsound.SND_ASYNC)

            draw_dashboard()

            if text_best_status == "creating arrest report":
                arrest_report_manager()
            elif text_best_status == "creating fine":
                fine_manager()
            elif text_best_status == "starting shift":
                with open("shiftlog.txt", "w") as file:
                    file.write(datetime.now().strftime("%m/%d/%Y %I:%M:%S %p") + " " + callsign + " Starting shift\n")
                send_data("STATUS_UPDATE", {"status": officer_status})
            elif text_best_status == "10-8 available":
                with open("shiftlog.txt", "a") as file:
                    file.write(datetime.now().strftime("%m/%d/%Y %I:%M:%S %p") + " " + callsign + " Set as available\n")
                send_data("STATUS_UPDATE", {"status": officer_status})
            elif text_best_status == "10-23 on scene":
                with open("shiftlog.txt", "a") as file:
                    file.write(datetime.now().strftime("%m/%d/%Y %I:%M:%S %p") + " " + callsign + " Arrived on scene\n")
                send_data("STATUS_UPDATE", {"status": officer_status})
            elif text_best_status == "ending shift":
                with open("shiftlog.txt", "a") as file:
                    file.write(datetime.now().strftime("%m/%d/%Y %I:%M:%S %p") + " " + callsign + " Ended shift\n")
                send_data("STATUS_UPDATE", {"status": officer_status})
            elif text_best_status == "starting a ReCAD online host":
                automatic_pincode = str(random.randint(1000, 9999))
                start_hosting(automatic_pincode, callsign)
            elif text_best_status == "connecting to ReCAD online":
                pincode = input("Enter pincode the host gave you: ")
                connect_to_host(pincode, callsign)
        else:

            print(f"[{dispatchname}] Command not recognized via text.")
            time.sleep(2)
            draw_dashboard()


def process_audio(audio_data):
    try:
        text = recognizer.recognize_google(audio_data, language="en-US")
    except sr.UnknownValueError:
        print(f"[{dispatchname}] Static on the line, say again?")
        return
    except Exception as e:
        print(f"[{dispatchname}] Radio error: {e}")
        return

    spoken_text = text.lower().strip()
    best_status = None
    highest_score = 0
    selected_audio = None

    for status, data in MDT_COMMANDS.items():
        for option in data["keywords"]:
            score = rapidfuzz.fuzz.partial_ratio(option, spoken_text)
            if score > highest_score:
                highest_score = score
                best_status = status
                selected_audio = data["audio"]

    if highest_score >= 75 and best_status:
        global officer_status
        officer_status = best_status
        winsound.PlaySound(selected_audio, winsound.SND_FILENAME | winsound.SND_ASYNC)
        draw_dashboard()

        if best_status == "creating arrest report":
            arrest_report_manager()
        elif best_status == "creating fine":
            fine_manager()
        elif best_status == "starting shift":
            with open("shiftlog.txt", "w") as file:
                file.write(datetime.now().strftime("%m/%d/%Y %I:%M:%S %p") + " " + callsign + " Starting shift\n")
            send_data("STATUS_UPDATE", {"status": officer_status})
        elif best_status == "10-8 available":
            with open("shiftlog.txt", "a") as file:
                file.write(datetime.now().strftime("%m/%d/%Y %I:%M:%S %p") + " " + callsign + " Set as available\n")
            send_data("STATUS_UPDATE", {"status": officer_status})
        elif best_status == "10-23 on scene":
            with open("shiftlog.txt", "a") as file:
                file.write(datetime.now().strftime("%m/%d/%Y %I:%M:%S %p") + " " + callsign + " Arrived on scene\n")
            send_data("STATUS_UPDATE", {"status": officer_status})
        elif best_status == "ending shift":
            with open("shiftlog.txt", "a") as file:
                file.write(datetime.now().strftime("%m/%d/%Y %I:%M:%S %p") + " " + callsign + " Ended shift\n")
            send_data("STATUS_UPDATE", {"status": officer_status})
        elif best_status == "starting a ReCAD online host":
            automatic_pincode = str(random.randint(1000, 9999))
            start_hosting(automatic_pincode, callsign)
        elif best_status == "connecting to ReCAD online":
            pincode = input("Enter pincode the host gave you: ")
            connect_to_host(pincode, callsign)
    else:
        print(f"[{dispatchname}] Say again please.")
        draw_dashboard()





#Base code starting beneath

print("============================")
print("POLICE COMPUTER AIDED DISPATCH")
print("============================")

dispatchname = input("\n [SYSTEM SETUP] Want to have dispatch or control \n >>> ")
if dispatchname.lower() == "dispatch":
    dispatchname = "DISPATCH"
if dispatchname.lower() == "control":
    dispatchname = "CONTROL"

os.system('cls')
print("============================")
print("POLICE COMPUTER AIDED DISPATCH")
print("============================")

callsign = config["General"]["callsign"]

if callsign.lower() == "":
    print("INVALID CALLSIGN!")
else:
    os.system('cls')

print("============================")
print(Fore.BLUE + f"unit: {callsign} --- status: {officer_status}")
print("============================")

print(f"Press {PTT_button} to talk to dispatch, press {Type_button} to type")

while listening_is_allowed:
    check_for_text()
    check_for_panic()

    if keyboard.is_pressed(PTT_button):
        winsound.PlaySound(resource_path(audiofolder + "/radiostart.wav"), winsound.SND_FILENAME | winsound.SND_ASYNC)

        with microphone as source:
            audio = recognizer.listen(source)

        try:
            winsound.PlaySound(resource_path(audiofolder + "/radioend.wav"), winsound.SND_FILENAME | winsound.SND_ASYNC)
        except Exception:
            pass


        threading.Thread(target=process_audio, args=(audio,), daemon=True).start()

    time.sleep(0.01)






