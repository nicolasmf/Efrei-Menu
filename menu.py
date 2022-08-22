import json
import os
from Wrapper import Wrapper

HEADER = """ 
 ____  ____  ____  ____  ____      __    ____  ____ 
( ___)( ___)(  _ \( ___)(_  _)    /__\  (  _ \(_  _)
 )__)  )__)  )   / )__)  _)(_    /(__)\  )___/ _)(_ 
(____)(__)  (_)\_)(____)(____)  (__)(__)(__)  (____)
                                      By Nicolas MF
"""


def show_menu() -> str:
    os.system("cls" if os.name == "nt" else "clear")
    print(HEADER)
    print("1. Voir mes matières")
    print("2. Voir mes notes")
    with open("variables.json", "r") as file:
        data = json.load(file)
    print(
        "3. Changer de semestre" + f" (S{data['semester']})"
        if data["semester"] != ""
        else ""
    )
    print("4. Actualiser mes identifiants")
    print("0. Quitter")
    return input("> ")


def interact(answer, wrapper):
    if answer == "0":
        print("Au revoir !")
        return

    elif answer == "1":
        wrapper.print_subjects_info()

    elif answer == "2":
        wrapper.print_subjects_grades()

    elif answer == "3":
        wrapper.change_semester(input("Entrez le numéro du semestre désiré : "))

    elif answer == "4":
        wrapper.save_credentials()

    else:
        print("Entrez une commande valide.")
        return

    print()
    return input("Appuyez sur entrée pour revenir au menu...")


def main():
    wrapper = Wrapper()

    answer = show_menu()
    while answer != "0":
        interact(answer, wrapper)
        answer = show_menu()
    return 0


if __name__ == "__main__":
    main()
