from models.Note_model import NotesModels
from models.Absence_model import AbsenceModels
from models.Etudiant_model import EtudiantModels
from models.Matiere_model import MatiereModels


class ProfesseurService:

    def __init__(self):
        self.notes_model = NotesModels()
        self.absence_model = AbsenceModels()
        self.etudiant_model = EtudiantModels()
        self.matiere_model = MatiereModels()

 
 


    def lister_etudiants_classe(self, classe_id: int):
        """Le professeur ne voit que les étudiants de sa propre classe."""
        return self.etudiant_model.lister_etudiants_par_classe(classe_id)

    def lister_matieres(self):
        return self.matiere_model.lister_matieres()





    def ajouter_note(self, etudiant_id: int, matiere_id: int, note: float) -> bool:
        if not (0 <= note <= 20):
            print("Erreur : la note doit être entre 0 et 20.")
            return False
        self.notes_model.ajouter_note(etudiant_id, matiere_id, note)
        return True

    def modifier_note(self, note_id: int, nouvelle_note: float) -> bool:
        if not (0 <= nouvelle_note <= 20):
            print("Erreur : la note doit être entre 0 et 20.")
            return False
        self.notes_model.modifier_note(note_id, nouvelle_note)
        return True

    def supprimer_note(self, note_id: int):
        self.notes_model.supprimer_note(note_id)

    def voir_notes_etudiant(self, etudiant_id: int):
        return self.notes_model.rechercher_note_par_etudiant(etudiant_id)

    def lister_toutes_notes(self):
        return self.notes_model.lister_notes()





    def enregistrer_absence(self, etudiant_id: int, matiere_id: int,
                            date: str, status: str):
        self.absence_model.ajouter_absence(etudiant_id, matiere_id, date, status)

    def justifier_absence(self, absence_id: int):
        self.absence_model.justifier_absence(absence_id)

    def voir_absences_etudiant(self, etudiant_id: int):
        return self.absence_model.rechercher_absence_par_etudiant(etudiant_id)

    def lister_toutes_absences(self):
        return self.absence_model.lister_absences()