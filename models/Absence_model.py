from database.bd import DatabaseManager


class AbsenceModels(DatabaseManager):

    def ajouter_absence(self, etudiant_id, matiere_id, date, status):
        try:
            self.cusor.execute(
                '''INSERT INTO absences (etudiant_id, matiere_id, date, status)
                   VALUES (?, ?, ?, ?)''',
                (etudiant_id, matiere_id, date, status)
            )
            self.conn.commit()
        except Exception as e:
            print(f"Erreur ajout absence : {e}")

    def lister_absences(self):
        self.cusor.execute(
            '''SELECT a.id, e.nom, e.prenom, m.nom_matiere, a.date, a.status
               FROM absences a
               JOIN etudiants e ON a.etudiant_id = e.id
               JOIN matieres  m ON a.matiere_id  = m.id'''
        )
        return self.cusor.fetchall()

    def justifier_absence(self, absence_id):
        self.cusor.execute(
            '''UPDATE absences SET status = 'justifiée' WHERE id = ?''',
            (absence_id,)
        )
        self.conn.commit()

    def supprimer_absence(self, absence_id):
        self.cusor.execute(
            '''DELETE FROM absences WHERE id = ?''',
            (absence_id,)
        )
        self.conn.commit()

    def rechercher_absence_par_etudiant(self, etudiant_id):
        self.cusor.execute(
            '''SELECT a.id, e.nom, e.prenom, m.nom_matiere, a.date, a.status
               FROM absences a
               JOIN etudiants e ON a.etudiant_id = e.id
               JOIN matieres  m ON a.matiere_id  = m.id
               WHERE a.etudiant_id = ?''',
            (etudiant_id,)
        )
        return self.cusor.fetchall()
