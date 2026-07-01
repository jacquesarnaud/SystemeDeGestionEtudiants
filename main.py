from database.bd import DatabaseManager
from services.Admin_service import AdminService
from services.connexion import ServiceConnexion
from utils.logger import LoggerUtils
from utils.admin import menu_admin
from utils.professeur import menu_professeur
from utils.etudiant import menu_etudiant
from config.Mes_constante import MENU_PRINCIPALE, CONNECTER


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
            while True:
                email = input("Email : ").strip()
                password = input("Mot de passe : ")

                if connexion.connecter(email, password):
                    utilisateur = admin_service.user_model.rechercher_utilisateur(email)
                    break

                print("\nEmail ou mot de passe incorrect. Veuillez réessayer.\n")

            role = utilisateur["role"]
            nom_con = utilisateur["prenom"]

            print(f"\n Bienvenue {nom_con},Vous etes vonnecté en tant que : {role.upper()}")

            if role == 'admin':
                menu_admin(admin_service, connexion, logger, email)

            elif role == 'professeur':
                professeur = admin_service.professeur_model.rechercher_professeur_par_id_user(
                    utilisateur["id"]
                )

                if professeur:
                    menu_professeur(connexion, email, professeur["classe_id"])
                else:
                    print("Profil professeur introuvable. Contactez l'administrateur.")

            elif role == 'etudiant':
                etudiant = admin_service.etudiant_model.rechercher_etudiant_par_id_user(
                    utilisateur["id"]
                )

                if etudiant:
                    menu_etudiant(connexion, etudiant["id"], email)
                else:
                    print("Profil étudiant introuvable. Contactez l'administrateur.")

            else:
                print("Rôle inconnu. Contactez l'administrateur.")

        elif choix == '2':
            print("Au revoir !")
            logger.log_info("Fin de session.")
            break

        else:
            print("Option invalide. Veuillez réessayer.")


if __name__ == "__main__":
    main()
