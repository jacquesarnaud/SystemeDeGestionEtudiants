from services.Etudiant_service import EtudiantService
from datetime import date as Date
from config.Mes_constante import (
    MENU_PROFESSEUR, GESTION_DES_NOTES_PROF,
    GESTION_DES_ABSENCES_PROF, MENU_ETUDIANT
)
from utils.saisie import pause

# ════════════════════════════════════════════════════════
#  MENU ÉTUDIANT
# ════════════════════════════════════════════════════════

def menu_etudiant(connexion, etudiant_id: int, email: str):
    etu_service = EtudiantService()
    while True:
        print(MENU_ETUDIANT)
        choix = input("Veuillez choisir une option : ").strip()

        if choix == '1':
            notes = etu_service.voir_mes_notes(etudiant_id)
            if notes:
                print("\n── Mes notes ──")
                for n in notes:
                    prinf"  {n['nom_matiere']:<25} | {n['note']}/20"t()
            else:
                print("Aucune note enregistrée.")
            pause()

        elif choix == '2':
            moyennes = etu_service.moyenne_par_matiere(etudiant_id)
            if moyennes:
                print("\n── Mes moyennes par matière ──")
                for m in moyennes:
                    print(f"  {m['matiere']:<25} | {m['moyenne']}/20  ({m['nb_notes']} note(s))")
            else:
                print("Aucune note enregistrée.")
            pause()

        elif choix == '3':
            moyenne = etu_service.moyenne_generale(etudiant_id)
            if moyenne is not None:
                print(f"\n  Moyenne générale : {round(moyenne, 2)}/20")
            else:
                print("Aucune note enregistrée.")
            pause()

        elif choix == '4':
            absences = etu_service.voir_mes_absences(etudiant_id)
            if absences:
                print("\n── Mes absences ──")
                for a in absences:
                    print(f"  {a['nom_matiere']:<25} | {a['date']} | {a['status']}")
            else:
                print("Aucune absence.")
            pause()

        elif choix == '5':
            t = etu_service.total_absences(etudiant_id)
            print(f"""
            ── Total de mes absences ──
              Total          : {t['total']}
              Justifiées     : {t['justifiees']}
              Non justifiées : {t['non_justifiees']}
            """)
            pause()

        elif choix == '0':
            connexion.deconnecter(email)
            break
        else:
            print("Option invalide.")
