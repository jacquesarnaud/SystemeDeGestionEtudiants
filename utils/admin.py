from services.connexion import ServiceConnexion
from utils.logger import LoggerUtils
from utils.saisie import saisir_entier, pause
from services.Admin_service import AdminService
from config.Mes_constante import (
    OPTION_PRINCIPALE_ADMIN,
    GESTION_DES_ETUDIANTS,
    GESTION_DES_PROFESSEURS,
    GESTION_DES_UTILISATEURS
)
from utils.generateur import generer_email,generer_mot_de_passe,generer_matricule

# ════════════════════════════════════════════════════════
#  GESTION DES ÉTUDIANTS
# ════════════════════════════════════════════════════════

def menu_gestion_etudiants(admin_service: AdminService, logger: LoggerUtils):
    while True:
        print(GESTION_DES_ETUDIANTS)
        choix = input("Veuillez choisir une option : ").strip()

        if choix == '1':
            nom = input("Nom : ").strip()
            prenom = input("Prénom : ").strip()
            age = saisir_entier("Âge : ")
            classe_id = saisir_entier("ID de la classe (1=A / 2=B / 3=C) : ")

            if age is not None and classe_id is not None:
                identifiants = admin_service.ajouter_etudiant(nom, prenom, age, classe_id)
                if identifiants:
                    print(f"""
        utilisateur {nom} {prenom} est creer avec succes suivant ses identifiant:
          Matricule   : {identifiants['matricule']}
          Email        : {identifiants['email']}
          Mot de passe : {identifiants['mot_de_passe']}
       !!! Remettez ces informations à l'étudiant !!!
        """)
                    logger.log_info(f"Étudiant + compte créés : {identifiants['matricule']}")
            pause()

        elif choix == '2':
            etudiants = admin_service.lister_etudiants()
            if etudiants:
                print(f"\n  {'ID':<5} {'Matricule':<18} {'Nom':<15} {'Prénom':<15} {'Âge':<5} {'Classe'}")
                print("  " + "─" * 65)
                for e in etudiants:
                    print(f"  {e['id']:<5} {e['matricule']:<18} {e['nom']:<15} {e['prenom']:<15} {e['age']:<5} {e['classe'] or '—'}")
            else:
                print("Aucun étudiant enregistré.")
            pause()

        elif choix == '3':
            etudiant_id = saisir_entier("ID de l'étudiant à modifier : ")
            classe_id   = saisir_entier("Nouvel ID de classe (1=A / 2=B / 3=C) : ")
            if etudiant_id is not None and classe_id is not None:
                admin_service.modifier_etudiant(etudiant_id, classe_id)
                print("Classe modifiée avec succès.")
            pause()

        elif choix == '4':
            etudiant_id = saisir_entier("ID de l'étudiant à supprimer : ")
            if etudiant_id is not None:
                confirmation = input("Confirmer la suppression ? (o/n) : ").strip().lower()
                if confirmation == 'o':
                    admin_service.supprimer_etudiant(etudiant_id)
                    logger.log_info(f"Étudiant supprimé : ID {etudiant_id}")
                    print("Étudiant supprimé.")
                else:
                    print("Suppression annulée.")
            pause()

        elif choix == '5':
            matricule = input("Matricule à rechercher : ").strip()
            etudiant  = admin_service.rechercher_etudiant(matricule)
            if etudiant:
                print(f"""
  ID        : {etudiant['id']}
  Matricule : {etudiant['matricule']}
  Nom       : {etudiant['nom']}
  Prénom    : {etudiant['prenom']}
  Âge       : {etudiant['age']}
  Classe    : {etudiant['classe'] or '—'}
  id_user   : {etudiant['id_user']}""")
                logger.log_info(f"Étudiant trouvé : {matricule}")
            else:
                print("Étudiant non trouvé.")
                logger.log_info(f"Recherche infructueuse — matricule : {matricule}")
            pause()

        elif choix == '0':
            break

        else:
            print("Option invalide. Veuillez réessayer.")


# ════════════════════════════════════════════════════════
#  GESTION DES PROFESSEURS
# ════════════════════════════════════════════════════════

def menu_gestion_professeurs(admin_service: AdminService, logger: LoggerUtils):
    while True:
        print(GESTION_DES_PROFESSEURS)
        choix = input("Veuillez choisir une option : ").strip()

        if choix == '1':
            # Afficher les matières disponibles
            matieres = admin_service.lister_matieres()
            if matieres:
                print("\n── Matières disponibles ──")
                for m in matieres:
                    print(f"  ID {m['id']} | {m['nom_matiere']}")

            nom        = input("\nNom : ").strip()
            prenom     = input("Prénom : ").strip()
            matiere_id = saisir_entier("ID de la matière (1=Mathematiques / 2=Physique-Chimie / 3=Anglais /4=Francais) : ")
            classe_id  = saisir_entier("ID de la classe (1=A / 2=B / 3=C) : ")

            if matiere_id is not None and classe_id is not None:
                identifiants = admin_service.ajouter_professeur(nom, prenom, matiere_id, classe_id)
                if identifiants:
                    print(f"""
utilisateur {nom} {prenom} est creer avec succes suivant ses identifiant:
          Email        : {identifiants['email']}
          Mot de passe : {identifiants['mot_de_passe']}
       !!! Remettez ces informations à l'étudiant !!!""")
                    logger.log_info(f"Professeur créé : {nom} {prenom}")
            pause()

        elif choix == '2':
            professeurs = admin_service.lister_professeurs()
            if professeurs:
                print(f"\n  {'ID':<5} {'Nom':<15} {'Prénom':<15} {'Matière':<20} {'Classe':<8} {'id_user'}")
                print("  " + "─" * 70)
                for p in professeurs:
                    print(f"  {p['id']:<5} {p['nom']:<15} {p['prenom']:<15} {p['matiere'] or '—':<20} {p['classe'] or '—':<8} {p['id_user']}")
            else:
                print("Aucun professeur enregistré.")
            pause()

        elif choix == '3':
            professeur_id       = saisir_entier("ID du professeur à modifier : ")
            nouvelle_matiere_id = saisir_entier("Nouvel ID de matière : ")
            if professeur_id is not None and nouvelle_matiere_id is not None:
                admin_service.modifier_professeur(professeur_id, nouvelle_matiere_id)
                print("Professeur modifié avec succès.")
            pause()

        elif choix == '4':
            professeur_id = saisir_entier("ID du professeur à supprimer : ")
            if professeur_id is not None:
                confirmation = input("Confirmer la suppression ? (o/n) : ").strip().lower()
                if confirmation == 'o':
                    admin_service.supprimer_professeur(professeur_id)
                    logger.log_info(f"Professeur supprimé : ID {professeur_id}")
                    print("Professeur supprimé.")
                else:
                    print("Suppression annulée.")
            pause()

        elif choix == '0':
            break

        else:
            print("Option invalide. Veuillez réessayer.")


# ════════════════════════════════════════════════════════
#  GESTION DES UTILISATEURS
# ════════════════════════════════════════════════════════

def menu_gestion_utilisateurs(admin_service: AdminService, logger: LoggerUtils):
    while True:
        print(GESTION_DES_UTILISATEURS)
        choix = input("Veuillez choisir une option : ").strip()

        if choix == '1':
            utilisateurs = admin_service.afficher_liste_utilisateurs()
            if utilisateurs:
                print(f"\n  {'ID':<5} {'Nom':<15} {'Prénom':<15} {'Email':<30} {'Rôle'}")
                print("  " + "─" * 70)
                for u in utilisateurs:
                    print(f"  {u['id']:<5} {u['nom']:<15} {u['prenom']:<15} {u['email']:<30} {u['role']}")
            else:
                print("Aucun utilisateur enregistré.")
            pause()

        elif choix == '2':
            email    = input("Email : ").strip()
            password = input("Mot de passe : ")
            role     = input("Rôle (admin / professeur / etudiant) : ").strip().lower()
            if role not in ('admin', 'professeur', 'etudiant'):
                print("Rôle invalide.")
            else:
                admin_service.ajouter_utilisateur(email, password, role)
                logger.log_info(f"Utilisateur ajouté : {email} ({role})")
                print("Utilisateur ajouté avec succès.")
            pause()

        elif choix == '3':
            user_id          = saisir_entier("ID de l'utilisateur à modifier : ")
            nouveau_email    = input("Nouvel email (vide = inchangé) : ").strip() or None
            nouveau_password = input("Nouveau mot de passe (vide = inchangé) : ") or None
            nouveau_role     = input("Nouveau rôle (vide = inchangé) : ").strip().lower() or None
            if nouveau_role and nouveau_role not in ('admin', 'professeur', 'etudiant'):
                print("Rôle invalide.")
            elif user_id is not None:
                admin_service.modifier_utilisateur(
                    user_id, nouveau_email, nouveau_password, nouveau_role
                )
                logger.log_info(f"Utilisateur modifié : ID {user_id}")
                print("Utilisateur modifié avec succès.")
            pause()

        elif choix == '4':
            user_id = saisir_entier("ID de l'utilisateur à supprimer : ")
            if user_id is not None:
                confirmation = input(
                    f"Confirmer la suppression de l'utilisateur {user_id} ? (o/n) : "
                ).strip().lower()
                if confirmation == 'o':
                    admin_service.supprimer_utilisateur(user_id)
                    logger.log_info(f"Utilisateur supprimé : ID {user_id}")
                    print("Utilisateur supprimé.")
                else:
                    print("Suppression annulée.")
            pause()

        elif choix == '0':
            break

        else:
            print("Option invalide. Veuillez réessayer.")


# ════════════════════════════════════════════════════════
#  MENU ADMIN PRINCIPAL
# ════════════════════════════════════════════════════════

def menu_admin(admin_service: AdminService, connexion: ServiceConnexion,
               logger: LoggerUtils, email: str):
    while True:
        print(OPTION_PRINCIPALE_ADMIN)
        choix = input("Veuillez choisir une option : ").strip()

        if choix == '1':
            menu_gestion_etudiants(admin_service, logger)
        elif choix == '2':
            menu_gestion_professeurs(admin_service, logger)
        elif choix == '3':
            menu_gestion_utilisateurs(admin_service, logger)
        elif choix == '0':
            connexion.deconnecter(email)
            break
        else:
            print("Option invalide. Veuillez réessayer.")
