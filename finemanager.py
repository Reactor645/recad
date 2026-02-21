import os

def finemanager ():
    fined_person = ""
    reason_for_fine = ""
    warning_or_fine = ""
    amount_fined = ""

    os.makedirs("Fines", exist_ok=True)

    os.system('cls' if os.name == 'nt' else 'clear')
    print("----------------------")
    print("      Fine Manager    ")
    print("----------------------")

    fined_person = input("Name of fined person: ")
    reason_for_fine = input("Reason for fine: ")
    warning_or_fine = input("Given warning or fine : ")
    amount_fined = input("Fined amount: ")

    titellineup = "------\n"
    titelmain = " FINE \n"
    titellinedown = "------\n"
    finedperson = "Name of fined person: " + fined_person + "\n"
    reasonforfine = "Reason for fine: " + reason_for_fine + "\n"
    warningorfine = "Given warning or fine: " + warning_or_fine + "\n"
    amount_fined = "Fined amount: " + amount_fined + "\n"

    with open("Fines/bestand.txt", "w") as file:
        file.write(titellineup)
        file.write(titelmain)
        file.write(titellinedown)
        file.write(finedperson)
        file.write(reasonforfine)
        file.write(warningorfine)
        file.write(amount_fined)
        print("Creating fine, please wait...")

    os.rename("Fines/bestand.txt", "Fines/fine" + fined_person + ".txt")

    done = 1