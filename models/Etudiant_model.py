from database.bd import DatabaseManager


class EtudiantModels(DatabaseManager):

    def ajouter_etudiant(self, matricule, nom, prenom, age, classe_id, id_user):
        try:
            self.cusor.execute(
                '''INSERT INTO etudiants (matricule, nom, prenom, age, classe_id, id_user)
                   VALUES (?, ?, ?, ?, ?, ?)''',
                (matricule, nom, prenom, age, classe_id, id_user)
            )
            self.conn.commit()
        except Exception as e:
            print(f"Erreur ajout étudiant : {e}")

    def lister_etudiants(self):
        self.cusor.execute('''
            SELECT e.id, e.matricule, e.nom, e.prenom, e.age,
                   c.nom_classe AS classe, e.id_user
            FROM etudiants e
            LEFT JOIN classes c ON e.classe_id = c.id
        ''')
        return self.cusor.fetchall()

    def lister_etudiants_par_classe(self, classe_id):
        self.cusor.execute(
            '''SELECT e.id, e.matricule, e.nom, e.prenom, e.age,
                      c.nom_classe AS classe, e.id_user
               FROM etudiants e
               LEFT JOIN classes c ON e.classe_id = c.id
               WHERE e.classe_id = ?''',
            (classe_id,)
        )
        return self.cusor.fetchall()

    def supprimer_etudiant(self, etudiant_id):
        self.cusor.execute(
            "DELETE FROM etudiants WHERE id = ?", (etudiant_id,)
        )
        self.conn.commit()

    def modifier_etudiant(self, etudiant_id, classe_id):
        self.cusor.execute(
            "UPDATE etudiants SET classe_id = ? WHERE id = ?",
            (classe_id, etudiant_id)
        )
        self.conn.commit()

    def rechercher_etudiant(self, matricule):
        self.cusor.execute(
            '''SELECT e.id, e.matricule, e.nom, e.prenom, e.age,
                      c.nom_classe AS classe, e.id_user
               FROM etudiants e
               LEFT JOIN classes c ON e.classe_id = c.id
               WHERE e.matricule = ?''',
            (matricule,)
        )
        return self.cusor.fetchone()

    def rechercher_etudiant_par_id_user(self, id_user):
        """Retrouve le profil étudiant depuis le compte connecté."""
        self.cusor.execute(
            '''SELECT e.id, e.matricule, e.nom, e.prenom, e.age,
                      c.nom_classe AS classe, e.id_user
               FROM etudiants e
               LEFT JOIN classes c ON e.classe_id = c.id
               WHERE e.id_user = ?''',
            (id_user,)
        )
        return self.cusor.fetchone()

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

    def meilleure_etudiant(self):
        self.cusor.execute(
            '''SELECT e.id, e.nom, e.prenom, AVG(n.note) AS moyenne
               FROM etudiants e
               JOIN notes n ON e.id = n.etudiant_id
               GROUP BY e.id
               ORDER BY moyenne DESC
               LIMIT 1'''
        )
        return self.cusor.fetchone()
