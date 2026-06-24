# service professeur
from models.Etudiant_model import EtudiantModels
from models.Absence_model import AbsenceModels
from models.Matiere_model import MatiereModels
from models.Professeur_model import ProfesseurModels


class Professeurservice:

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

    def attribuer_note_etudiant(self, matricule, matiere_id, note):
        etudiant = self.etudiant_model.rechercher_etudiant(matricule)
        if etudiant:
            self.matiere_model.attribuer_note(etudiant[0], matiere_id, note)
            return True
        else:
            return False

    def modifier_note_etudiant(self, matricule, matiere_id, nouvelle_note):
        etudiant = self.etudiant_model.rechercher_etudiant(matricule)
        if etudiant:
            self.matiere_model.modifier_note(etudiant[0], matiere_id, nouvelle_note)
            return True
        else:
            return False