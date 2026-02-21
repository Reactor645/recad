import ctypes
from random import randint
import os
from time import sleep

import ArrestReport

text = ""
title = ""


def alert(text, title):
    ctypes.windll.user32.MessageBoxW(0, text, title, 0)

def Warrant():
    accepted = randint(1, 2)
    if accepted == 1:
        print("Warrant denied.")
        alert("Judge has decided, please check your cad.", "Alert")
    elif accepted == 2:
        print("Warrant approved, full overview: name of person for warrant: " + Warrantperson + "warranttype: " + Warranttype + "Proceed with caution")
        alert("Judge has decided, please check your cad.", "Alert")

def warrantmanager():
    Warrantperson = input("Who do you want a warrant for: ")
    Warranttype = input("What type of warrant do you want? (Search, no knock or arrest): ")
    Warrantprior = input("What is the priority of your warrant? (1, 2 or 3): ")

    print("Please wait, a judge will review your request. This can take up to 3 minutes for a priority 3 and up to 7 minutes for a priority 1.")

    if Warrantprior == "1":
        sleep(randint(60, 420))
        Warrant()
    elif Warrantprior == "2":
        sleep(randint(60, 300))
        Warrant()
    elif Warrantprior == "3":
        sleep(randint(60, 180))
        Warrant()

