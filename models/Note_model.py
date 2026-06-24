from database.bd import DatabaseManager


class NotesModels(DatabaseManager):

    def ajouter_note(self, etudiant_id, matiere_id, note):
        try:
            self.cusor.execute(
                '''INSERT INTO notes (etudiant_id, matiere_id, note) VALUES (?, ?, ?)''',
                (etudiant_id, matiere_id, note)
            )
            self.conn.commit()
        except Exception as e:
            print(f"Erreur ajout note : {e}")

    def lister_notes(self):
        self.cusor.execute(
            '''SELECT n.id, e.nom, e.prenom, m.nom_matiere, n.note
               FROM notes n
               JOIN etudiants e ON n.etudiant_id = e.id
               JOIN matieres  m ON n.matiere_id  = m.id'''
        )
        return self.cusor.fetchall()

    def modifier_note(self, note_id, nouvelle_note):
        self.cusor.execute(
            '''UPDATE notes SET note = ? WHERE id = ?''',
            (nouvelle_note, note_id)
        )
        self.conn.commit()

    def supprimer_note(self, note_id):
        self.cusor.execute(
            '''DELETE FROM notes WHERE id = ?''',
            (note_id,)
        )
        self.conn.commit()

    def rechercher_note_par_etudiant(self, etudiant_id):
        self.cusor.execute(
            '''SELECT n.id, e.nom, e.prenom, m.nom_matiere, n.note
               FROM notes n
               JOIN etudiants e ON n.etudiant_id = e.id
               JOIN matieres  m ON n.matiere_id  = m.id
               WHERE n.etudiant_id = ?''',
            (etudiant_id,)
        )
        return self.cusor.fetchall()

    def calculer_moyenne_etudiant(self, etudiant_id):
        self.cusor.execute(
            '''SELECT AVG(note) FROM notes WHERE etudiant_id = ?''',
            (etudiant_id,)
        )
        result = self.cusor.fetchone()
        return result[0] if result else None
