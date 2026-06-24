from services.Professeur_service import ProfesseurService
from services.Etudiant_service import EtudiantService
from datetime import date as Date
from config.Mes_constante import (
    MENU_PROFESSEUR, GESTION_DES_NOTES_PROF,
    GESTION_DES_ABSENCES_PROF, MENU_ETUDIANT
)
from services.Professeur_service import Professeurservice
from utils.saisie import pause,saisir_entier,saisir_note


# ═══════════════════════════════════════════════════════
#  MENU PROFESSEUR
# ════════════════════════════════════════════════════════

def menu_notes_professeur(prof_service: ProfesseurService, classe_id: int):
    prof_service = Professeurservice
    while True:
        print(GESTION_DES_NOTES_PROF)
        choix = input("Veuillez choisir une option : ").strip()

        if choix == '1':
            # Afficher uniquement les étudiants de la classe du professeur
            etudiants = prof_service.lister_etudiants_classe(classe_id)
            if not etudiants:
                print("Aucun étudiant dans votre classe.")
                pause()
                continue
            print("\n── Vos étudiants ──")
            for e in etudiants:
                print(f"  ID {e['id']} | {e['nom']} {e['prenom']}")

            matieres = prof_service.lister_matieres()
            print("\n── Matières ──")
            for m in matieres:
                print(f"  ID {m['id']} | {m['nom_matiere']}")

            etudiant_id = saisir_entier("\nID de l'étudiant : ")
            matiere_id  = saisir_entier("ID de la matière  : ")
            note        = saisir_note("Note (0–20)        : ")

            if etudiant_id and matiere_id and note is not None:
                if prof_service.ajouter_note(etudiant_id, matiere_id, note):
                    print("Note ajoutée avec succès.")
            pause()

        elif choix == '2':
            etudiants = prof_service.lister_etudiants_classe(classe_id)
            print("\n── Vos étudiants ──")
            for e in etudiants:
                print(f"  ID {e['id']} | {e['nom']} {e['prenom']}")
            etudiant_id = saisir_entier("\nID de l'étudiant : ")
            if etudiant_id:
                notes = prof_service.voir_notes_etudiant(etudiant_id)
                if notes:
                    print(f"\n── Notes ──")
                    for n in notes:
                        print(f"  ID {n['id']} | {n['nom_matiere']:<20} | {n['note']}/20")
                else:
                    print("Aucune note pour cet étudiant.")
            pause()

        elif choix == '3':
            note_id       = saisir_entier("ID de la note à modifier : ")
            nouvelle_note = saisir_note("Nouvelle note (0–20) : ")
            if note_id and nouvelle_note is not None:
                if prof_service.modifier_note(note_id, nouvelle_note):
                    print("Note modifiée.")
            pause()

        elif choix == '4':
            note_id = saisir_entier("ID de la note à supprimer : ")
            if note_id:
                if input("Confirmer ? (o/n) : ").strip().lower() == 'o':
                    prof_service.supprimer_note(note_id)
                    print("Note supprimée.")
            pause()

        elif choix == '5':
            notes = prof_service.lister_toutes_notes()
            if notes:
                print("\n── Toutes les notes ──")
                for n in notes:
                    print(f"  {n['nom']:<15} {n['prenom']:<15} | {n['nom_matiere']:<20} | {n['note']}/20")
            else:
                print("Aucune note enregistrée.")
            pause()

        elif choix == '0':
            break
        else:
            print("Option invalide.")


def menu_absences_professeur(prof_service: ProfesseurService, classe_id: int):
    while True:
        print(GESTION_DES_ABSENCES_PROF)
        choix = input("Veuillez choisir une option : ").strip()

        if choix == '1':
            etudiants = prof_service.lister_etudiants_classe(classe_id)
            if not etudiants:
                print("Aucun étudiant dans votre classe.")
                pause()
                continue
            print("\n── Vos étudiants ──")
            for e in etudiants:
                print(f"  ID {e['id']} | {e['nom']} {e['prenom']}")

            matieres = prof_service.lister_matieres()
            print("\n── Matières ──")
            for m in matieres:
                print(f"  ID {m['id']} | {m['nom_matiere']}")

            etudiant_id = saisir_entier("\nID de l'étudiant : ")
            matiere_id  = saisir_entier("ID de la matière  : ")
            date_today  = str(Date.today())
            date_saisie = input(f"Date (vide = {date_today}) : ").strip()
            date        = date_saisie if date_saisie else date_today
            status      = input("Statut (justifiée / non justifiée) : ").strip().lower()

            if status not in ("justifiée", "non justifiée"):
                print("Statut invalide.")
            elif etudiant_id and matiere_id:
                prof_service.enregistrer_absence(etudiant_id, matiere_id, date, status)
                print("Absence enregistrée.")
            pause()

        elif choix == '2':
            etudiants = prof_service.lister_etudiants_classe(classe_id)
            print("\n── Vos étudiants ──")
            for e in etudiants:
                print(f"  ID {e['id']} | {e['nom']} {e['prenom']}")
            etudiant_id = saisir_entier("\nID de l'étudiant : ")
            if etudiant_id:
                absences = prof_service.voir_absences_etudiant(etudiant_id)
                if absences:
                    for a in absences:
                        print(f"  ID {a['id']} | {a['nom_matiere']:<20} | {a['date']} | {a['status']}")
                else:
                    print("Aucune absence.")
            pause()

        elif choix == '3':
            absence_id = saisir_entier("ID de l'absence à justifier : ")
            if absence_id:
                prof_service.justifier_absence(absence_id)
                print("Absence justifiée.")
            pause()

        elif choix == '4':
            absences = prof_service.lister_toutes_absences()
            if absences:
                for a in absences:
                    print(f"  {a['nom']:<15} {a['prenom']:<15} | {a['nom_matiere']:<20} | {a['date']} | {a['status']}")
            else:
                print("Aucune absence.")
            pause()

        elif choix == '0':
            break
        else:
            print("Option invalide.")


def menu_professeur(connexion, email: str, classe_id: int):
    prof_service = ProfesseurService()
    while True:
        print(MENU_PROFESSEUR)
        choix = input("Veuillez choisir une option : ").strip()

        if choix == '1':
            menu_notes_professeur(prof_service, classe_id)
        elif choix == '2':
            menu_absences_professeur(prof_service, classe_id)
        elif choix == '0':
            connexion.deconnecter(email)
            break
        else:
            print("Option invalide.")
