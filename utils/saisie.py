
def pause():
    input("\nAppuyez sur Entrée pour revenir au menu...")


def saisir_entier(prompt: str):
    try:
        return int(input(prompt))
    except ValueError:
        print("Saisie invalide : un nombre entier est attendu.")
        return None


def saisir_note(prompt: str):
    try:
        note = float(input(prompt))
        if 0 <= note <= 20:
            return note
        print("Erreur : la note doit être entre 0 et 20.")
        return None
    except ValueError:
        print("Saisie invalide.")
        return None



if __name__ == "__main__":
    saisir_entier(pause())
    saisir_note(pause())