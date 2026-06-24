from services.Admin_service import AdminService
from services.connexion import ServiceConnexion
from utils.logger import LoggerUtils
from database.bd import DatabaseManager
from config.Mes_constante import (
    MENU_PRINCIPALE, CONNECTER
)
from utils.admin import menu_admin
from utils.etudiant import menu_etudiant
from utils.professeur import menu_professeur

def main():

    db = DatabaseManager()
    db.creer_super_admin()

    admin_service = AdminService()
    connexion     = ServiceConnexion()
    logger        = LoggerUtils()

    while True:
        print(MENU_PRINCIPALE)
        print(CONNECTER)
        choix = input("Veuillez choisir une option : ").strip()

        if choix == '1':
            while connexion:
                email    = input("Email : ").strip()
                password = input("Mot de passe : ")

                if connexion.connecter(email, password):
                    role = admin_service.recuperer_role(email)
                    nom_user = admin_service.rechercher_utilisateur(email)
                    nom_user_join= " ".join(nom_user)
                    print(f"Bienvenu {nom_user_join} , Vous-etes connecté en tant que : {role}")

                    if role == 'admin':
                        menu_admin(admin_service, connexion, logger, email)
                    elif role == 'professeur':
                        menu_professeur(connexion, email, classe_id)
                    elif role == 'etudiant':
                        menu_etudiant(connexion, etudiant_id, email)
                    else:
                        print("Rôle inconnu, contactez l'administrateur.")
                else:
                    print("Identifiants incorrects.")

        elif choix == '2':
            print("Au revoir !")
            logger.log_info("L'utilisateur a quitté le programme.")
            break

        else:
            print("Option invalide. Veuillez réessayer.")

if __name__ == "__main__":
    main()
