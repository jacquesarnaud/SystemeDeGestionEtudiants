from models.Etudiant_model import EtudiantModels
from models.Absence_model import AbsenceModels
from models.Matiere_model import MatiereModels
from models.Professeur_model import ProfesseurModels
from models.User_model import UtilisateurModels
from models.Note_model import NotesModels


class AdminService:

    def __init__(self):
        self.etudiant_model   = EtudiantModels()
        self.absence_model    = AbsenceModels()
        self.matiere_model    = MatiereModels()
        self.professeur_model = ProfesseurModels()
        self.user_model       = UtilisateurModels()
        self.notes_model      = NotesModels()   # Correction : manquant dans la version originale

    # ─── Utilisateurs ───────────────────────────────────────────────────────────

    def afficher_liste_utilisateurs(self):
        return self.user_model.lister_utilisateurs()

    def recuperer_role(self, email):
        utilisateur = self.user_model.rechercher_utilisateur(email)
        if utilisateur:
            return utilisateur["role"]
        return None

    def verifier_identifiants(self, email, mot_de_passe):
        utilisateur = self.user_model.rechercher_utilisateur(email)
        return utilisateur is not None and utilisateur["mot_de_passe"] == mot_de_passe

    def ajouter_utilisateur(self, email, password, role):
        self.user_model.ajouter_utilisateur(email, password, role)

    def supprimer_utilisateur(self, utilisateur_id):
        self.user_model.supprimer_utilisateur(utilisateur_id)

    def modifier_utilisateur(self, utilisateur_id, nouveau_email=None,
                              nouveau_password=None, nouveau_role=None):
        self.user_model.modifier_utilisateur(utilisateur_id, nouveau_email,
                                             nouveau_password, nouveau_role)
    def rechercher_utilisateur(self,mail):
        nom_user= self.user_model.rechercher_utilisateur(mail)
        return nom_user["nom"] , nom_user["prenom"]

    # ─── Étudiants ──────────────────────────────────────────────────────────────

    def ajouter_etudiant(self, matricule, nom, prenom, age, classe):
        self.etudiant_model.ajouter_etudiant(matricule, nom, prenom, age, classe)

    def lister_etudiants(self):
        return self.etudiant_model.lister_etudiants()

    def supprimer_etudiant(self, etudiant_id):
        self.etudiant_model.supprimer_etudiant(etudiant_id)

    def modifier_etudiant(self, etudiant_id, nouvelle_classe):
        self.etudiant_model.modifier_etudiant(etudiant_id, nouvelle_classe)

    def rechercher_etudiant(self, matricule):
        return self.etudiant_model.rechercher_etudiant(matricule)

    # ─── Professeurs ────────────────────────────────────────────────────────────

    def ajouter_professeur(self, nom, prenom, matiere_id):
        self.professeur_model.ajouter_professeur(nom, prenom, matiere_id)

    def lister_professeurs(self):
        return self.professeur_model.lister_professeurs()

    def supprimer_professeur(self, professeur_id):
        self.professeur_model.supprimer_professeur(professeur_id)

    def modifier_professeur(self, professeur_id, nouvelle_matiere_id):
        self.professeur_model.modifier_professeur(professeur_id, nouvelle_matiere_id)

    def rechercher_professeur(self, nom):
        return self.professeur_model.rechercher_professeur(nom)

    def affecter_matiere(self, professeur_id, matiere_id):
        self.professeur_model.affecter_matiere(professeur_id, matiere_id)

    # ─── Matières ───────────────────────────────────────────────────────────────

    def ajouter_matiere(self, nom_matiere):
        self.matiere_model.ajouter_matiere(nom_matiere)

    def lister_matieres(self):
        return self.matiere_model.lister_matieres()

    def supprimer_matiere(self, matiere_id):
        self.matiere_model.supprimer_matiere(matiere_id)

    def modifier_matiere(self, matiere_id, nouveau_nom):
        self.matiere_model.modifier_matiere(matiere_id, nouveau_nom)

    def rechercher_matiere(self, nom_matiere):
        return self.matiere_model.rechercher_matiere(nom_matiere)

    # ─── Notes ──────────────────────────────────────────────────────────────────

    def ajouter_note(self, etudiant_id, matiere_id, note):
        self.notes_model.ajouter_note(etudiant_id, matiere_id, note)

    def lister_notes(self):
        return self.notes_model.lister_notes()

    def modifier_note(self, note_id, nouvelle_note):
        self.notes_model.modifier_note(note_id, nouvelle_note)

    def supprimer_note(self, note_id):
        self.notes_model.supprimer_note(note_id)

    # ─── Absences ───────────────────────────────────────────────────────────────

    def ajouter_absence(self, etudiant_id, matiere_id, date, status):
        self.absence_model.ajouter_absence(etudiant_id, matiere_id, date, status)

    def lister_absences(self):
        return self.absence_model.lister_absences()

    def justifier_absence(self, absence_id):
        self.absence_model.justifier_absence(absence_id)

    def supprimer_absence(self, absence_id):
        self.absence_model.supprimer_absence(absence_id)

    def rechercher_absence_par_etudiant(self, etudiant_id):
        return self.absence_model.rechercher_absence_par_etudiant(etudiant_id)

    # Statistiques

    def moyenne_etudiant(self, etudiant_id):
        return self.notes_model.calculer_moyenne_etudiant(etudiant_id)

    def moyenne_classe(self, classe):

        etudiants = self.etudiant_model.lister_etudiants_par_classe(classe)
        if not etudiants:
            return None
        total, count = 0, 0
        for etudiant in etudiants:
            notes = self.etudiant_model.rechercher_note_par_etudiant(etudiant["id"])
            if notes:
                total += sum(note["note"] for note in notes)
                count += len(notes)
        return total / count if count > 0 else None

    def meilleure_etudiant(self):

        return self.etudiant_model.meilleure_etudiant()
