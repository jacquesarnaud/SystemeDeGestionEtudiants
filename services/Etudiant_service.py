# service etudiant
from models.Etudiant_model import EtudiantModels
from models.Absence_model import AbsenceModels
from models.Matiere_model import MatiereModels
from models.Professeur_model import ProfesseurModels

class Etudiantservice:

    def __init__(self):
        self.etudiant_model = EtudiantModels()
        self.absence_model = AbsenceModels()
        self.matiere_model = MatiereModels()
        self.professeur_model = ProfesseurModels()

    def afficher_notes_etudiant(self, matricule):
        etudiant = self.etudiant_model.rechercher_etudiant(matricule)
        if etudiant:
            notes = self.matiere_model.lister_notes_etudiant(etudiant[0])
            return notes
        else:
            return None

    def afficher_absences_etudiant(self, matricule):
        etudiant = self.etudiant_model.rechercher_etudiant(matricule)
        if etudiant:
            absences = self.absence_model.lister_absences_etudiant(etudiant[0])
            return absences
        else:
            return None

    def afficher_moyenne_etudiant(self, matricule):

        etudiant = self.etudiant_model.rechercher_etudiant(matricule)
        if etudiant:
            moyenne = self.matiere_model.calculer_moyenne_etudiant(etudiant[0])
            return moyenne
        else:
            return None
