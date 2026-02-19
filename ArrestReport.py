import os

def arrestreport():
    felonies = []
    found_items = []

    # Map maken als hij niet bestaat (nodig om crash te voorkomen)
    os.makedirs("ArrestReports", exist_ok=True)

    os.system('cls' if os.name == 'nt' else 'clear')
    print("-----------------------")
    print(" Arrest Report Manager ")
    print("-----------------------")

    arresteename = input("Enter the name of the arrestee: ")
    name_of_arresting_officer = input("Enter the name of the arresting officer: ")

    # Felonies toevoegen
    while True:
        felony = input("Add a felony the arrestee committed (type Done when finished): ").upper()
        if felony == "DONE":
            break
        felonies.append(felony)

    # Found items toevoegen
    while True:
        item = input("Add an item found on the arrestee (type Done when finished): ").upper()
        if item == "DONE":
            break
        found_items.append(item)

    print("Creating arrest report, please wait...")

    titellineup = "--------------------\n"
    titelmain = "POLICE ARREST REPORT\n"
    titellinedown = "--------------------\n"
    arrestee = "Name of arrestee: " + arresteename + "\n"
    arrestingofficer = "Name of arresting officer: " + name_of_arresting_officer + "\n"

    # LIJSTEN OMZETTEN NAAR STRING (NODIG!!)
    convictedfelonies = "Felonies: " + ", ".join(felonies) + "\n"
    founditems = "Found items: " + ", ".join(found_items) + "\n"

    with open("ArrestReports/bestand.txt", "w") as file:
        file.write(titellineup)
        file.write(titelmain)
        file.write(titellinedown)
        file.write("\n")
        file.write(arrestee)
        file.write(arrestingofficer)
        file.write(convictedfelonies)
        file.write(founditems)



    os.rename("ArrestReports/bestand.txt", "ArrestReports/ArrestReport.txt")

    done = 1
