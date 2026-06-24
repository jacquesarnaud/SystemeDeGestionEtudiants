from models.User_model import UtilisateurModels
from utils.logger import LoggerUtils


class ServiceConnexion:

    def __init__(self):
        self.user_bd = UtilisateurModels()
        self.logger  = LoggerUtils()

    def connecter(self, email, password):

        utilisateur = self.user_bd.rechercher_utilisateur(email)

        if utilisateur and utilisateur["mot_de_passe"] == password:
            self.logger.log_info(f"Connexion réussie : {email}")
            return True
        else:
            self.logger.log_warning(f"Tentative de connexion échouée : {email}")
            return False

    def deconnecter(self, email):
        self.logger.log_info(f"Déconnexion : {email}")
        print("Vous avez été déconnecté.")
