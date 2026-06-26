from models.Note_model import NotesModels
from models.Absence_model import AbsenceModels


class EtudiantService:

    def __init__(self):
        self.notes_model = NotesModels()
        self.absence_model = AbsenceModels()

    # ─── Notes ───────────────────────────────────────────────────────────────────

    def voir_mes_notes(self, etudiant_id: int):
        return self.notes_model.rechercher_note_par_etudiant(etudiant_id)

    # ─── Moyennes ────────────────────────────────────────────────────────────────

    def moyenne_generale(self, etudiant_id: int):
        return self.notes_model.calculer_moyenne_etudiant(etudiant_id)

    def moyenne_par_matiere(self, etudiant_id: int) -> list:
        """Calcule la moyenne par matière à partir des notes de l'étudiant."""
        notes = self.notes_model.rechercher_note_par_etudiant(etudiant_id)
        if not notes:
            return []

        # Regrouper les notes par matière
        matieres: dict = {}
        for note in notes:
            nom_matiere = note["nom_matiere"]
            if nom_matiere not in matieres:
                matieres[nom_matiere] = []
            matieres[nom_matiere].append(note["note"])

        # Calculer la moyenne pour chaque matière
        return [
            {
                "matiere": matiere,
                "moyenne": round(sum(liste) / len(liste), 2),
                "nb_notes": len(liste)
            }
            for matiere, liste in matieres.items()
        ]

    # ─── Absences ────────────────────────────────────────────────────────────────

    def voir_mes_absences(self, etudiant_id: int):
        return self.absence_model.rechercher_absence_par_etudiant(etudiant_id)

    def total_absences(self, etudiant_id: int) -> dict:
        absences = self.absence_model.rechercher_absence_par_etudiant(etudiant_id)
        if not absences:
            return {"total": 0, "justifiees": 0, "non_justifiees": 0}

        justifiees = sum(1 for a in absences if a["status"] == "justifiée")
        non_justifiees = sum(1 for a in absences if a["status"] == "non justifiée")
        return {
            "total": len(absences),
            "justifiees": justifiees,
            "non_justifiees": non_justifiees
        }
