from services.connexion import ServiceConnexion
from utils.logger import LoggerUtils
from config.Mes_constante import ( OPTION_PRINCIPALE_ADMIN,
    GESTION_DES_ETUDIANTS, GESTION_DES_PROFESSEURS,GESTION_DES_UTILISATEURS )
from utils.saisie import saisir_entier
from services.Admin_service import AdminService

def menu_gestion_etudiants(admin_service: AdminService, logger: LoggerUtils):
    while True:
        print(GESTION_DES_ETUDIANTS)
        choix = input("Veuillez choisir une option : ").strip()

        if choix == '1':
            matricule = input("Matricule : ").strip()
            nom       = input("Nom : ").strip()
            prenom    = input("Prénom : ").strip()
            age       = saisir_entier("Âge : ")
            classe    = input("Classe : ").strip()
            if age is not None:
                admin_service.ajouter_etudiant(matricule, nom, prenom, age, classe)
                print(f"Étudiant {nom} {prenom} ajouté avec succès.")


        elif choix == '2':
            etudiants = admin_service.lister_etudiants()
            if etudiants:
                for etudiant in etudiants:
                    print(dict(etudiant))
            else:
                print("Aucun étudiant enregistré.")

        elif choix == '3':
            etudiant_id = saisir_entier("ID de l'étudiant à modifier : ")
            if etudiant_id is not None:
                nouvelle_classe = input("Nouvelle classe : ").strip()
                admin_service.modifier_etudiant(etudiant_id, nouvelle_classe)
                print("Étudiant modifié avec succès.")

        elif choix == '4':
            etudiant_id = saisir_entier("ID de l'étudiant à supprimer : ")
            if etudiant_id is not None:
                admin_service.supprimer_etudiant(etudiant_id)
                print("Étudiant supprimé.")
                logger.log_info("Étudiant supprimé")

        elif choix == '5':
            matricule = input("Matricule à rechercher : ").strip()
            etudiant  = admin_service.rechercher_etudiant(matricule)
            if etudiant:
                print(    print(f"""
                          ID        : {etudiant['id']}
                          Matricule : {etudiant['matricule']}
                          Nom       : {etudiant['nom']}
                          Prénom    : {etudiant['prenom']}
                          Âge       : {etudiant['age']}
                          Classe    : {etudiant['classe']}
                """))
                logger.log_info(f"Étudiant trouvé : {matricule}")
            else:
                print("Étudiant non trouvé.")
                logger.log_info(f"Recherche infructueuse — matricule : {matricule}")

        elif choix == '0':
            break

        else:
            print("Option invalide. Veuillez réessayer.")


def menu_gestion_professeurs(admin_service: AdminService):
    while True:
        print(GESTION_DES_PROFESSEURS)
        choix = input("Veuillez choisir une option : ").strip()

        if choix == '1':
            nom        = input("Nom : ").strip()
            prenom     = input("Prénom : ").strip()
            matiere_id = saisir_entier("ID de la matière : ")
            if matiere_id is not None:
                admin_service.ajouter_professeur(nom, prenom, matiere_id)
                print("Professeur ajouté avec succès.")

        elif choix == '2':
            professeurs = admin_service.lister_professeurs()
            if professeurs:
                for prof in professeurs:
                    print(dict(prof))
            else:
                print("Aucun professeur enregistré.")

        elif choix == '3':
            professeur_id       = saisir_entier("ID du professeur à modifier : ")
            nouvelle_matiere_id = saisir_entier("Nouvel ID de matière : ")
            if professeur_id is not None and nouvelle_matiere_id is not None:
                admin_service.modifier_professeur(professeur_id, nouvelle_matiere_id)
                print("Professeur modifié avec succès.")

        elif choix == '4':
            professeur_id = saisir_entier("ID du professeur à supprimer : ")
            if professeur_id is not None:
                admin_service.supprimer_professeur(professeur_id)
                print("Professeur supprimé.")

        elif choix == '0':
            break

        else:
            print("Option invalide. Veuillez réessayer.")


def menu_gestion_utilisateurs(admin_service: AdminService, logger: LoggerUtils):
    while True:
        print(GESTION_DES_UTILISATEURS)
        choix = input("Veuillez choisir une option : ").strip()

        if choix == '1':
            utilisateurs = admin_service.afficher_liste_utilisateurs()
            if utilisateurs:
                for u in utilisateurs:
                    print(dict(u))
            else:
                print("Aucun utilisateur enregistré.")

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

        elif choix == '3':
            user_id          = saisir_entier("ID de l'utilisateur à modifier : ")
            nouveau_email    = input("Nouvel email (vide = inchangé) : ").strip() or None
            nouveau_password = input("Nouveau mot de passe (vide = inchangé) : ") or None
            nouveau_role     = input("Nouveau rôle (vide = inchangé) : ").strip().lower() or None
            if nouveau_role and nouveau_role not in ('admin', 'professeur', 'etudiant'):
                print("Rôle invalide.")
            elif user_id is not None:
                admin_service.modifier_utilisateur(user_id, nouveau_email,
                                                   nouveau_password, nouveau_role)
                logger.log_info(f"Utilisateur modifié : ID {user_id}")
                print("Utilisateur modifié avec succès.")

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

        elif choix == '0':
            break

        else:
            print("Option invalide. Veuillez réessayer.")

def menu_admin(admin_service: AdminService, connexion: ServiceConnexion,
               logger: LoggerUtils, email: str):
    while True:
        print(OPTION_PRINCIPALE_ADMIN)
        choix = input("Veuillez choisir une option : ").strip()

        if choix == '1':
            menu_gestion_etudiants(admin_service, logger)
        elif choix == '2':
            menu_gestion_professeurs(admin_service)
        elif choix == '3':
            menu_gestion_utilisateurs(admin_service, logger)
        elif choix == '0':
            connexion.deconnecter(email)
            break
        else:
            print("Option invalide. Veuillez réessayer.")

