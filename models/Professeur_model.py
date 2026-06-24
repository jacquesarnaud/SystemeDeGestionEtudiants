from database.bd import DatabaseManager


class ProfesseurModels(DatabaseManager):

    def ajouter_professeur(self, nom, prenom, matiere_id, classe_id, id_user):
        try:
            self.cusor.execute(
                '''INSERT INTO professeurs (nom, prenom, matiere_id, classe_id, id_user)
                   VALUES (?, ?, ?, ?, ?)''',
                (nom, prenom, matiere_id, classe_id, id_user)
            )
            self.conn.commit()
        except Exception as e:
            print(f"Erreur ajout professeur : {e}")

    def lister_professeurs(self):
        self.cusor.execute(
            '''SELECT p.id, p.nom, p.prenom,
                      m.nom_matiere AS matiere,
                      c.nom_classe  AS classe,
                      p.id_user
               FROM professeurs p
               LEFT JOIN matieres m ON p.matiere_id = m.id
               LEFT JOIN classes  c ON p.classe_id  = c.id'''
        )
        return self.cusor.fetchall()

    def supprimer_professeur(self, professeur_id):
        self.cusor.execute(
            "DELETE FROM professeurs WHERE id = ?", (professeur_id,)
        )
        self.conn.commit()

    def modifier_professeur(self, professeur_id, nouvelle_matiere_id):
        self.cusor.execute(
            "UPDATE professeurs SET matiere_id = ? WHERE id = ?",
            (nouvelle_matiere_id, professeur_id)
        )
        self.conn.commit()

    def rechercher_professeur(self, nom):
        self.cusor.execute(
            '''SELECT p.id, p.nom, p.prenom,
                      m.nom_matiere AS matiere,
                      c.nom_classe  AS classe,
                      p.id_user
               FROM professeurs p
               LEFT JOIN matieres m ON p.matiere_id = m.id
               LEFT JOIN classes  c ON p.classe_id  = c.id
               WHERE p.nom = ?''',
            (nom,)
        )
        return self.cusor.fetchone()

    def rechercher_professeur_par_id_user(self, id_user):
        """Retrouve le profil professeur depuis le compte connecté."""
        self.cusor.execute(
            '''SELECT p.id, p.nom, p.prenom,
                      m.nom_matiere AS matiere,
                      c.nom_classe  AS classe,
                      p.classe_id,
                      p.id_user
               FROM professeurs p
               LEFT JOIN matieres m ON p.matiere_id = m.id
               LEFT JOIN classes  c ON p.classe_id  = c.id
               WHERE p.id_user = ?''',
            (id_user,)
        )
        return self.cusor.fetchone()

    def affecter_matiere(self, professeur_id, matiere_id):
        self.cusor.execute(
            "UPDATE professeurs SET matiere_id = ? WHERE id = ?",
            (matiere_id, professeur_id)
        )
        self.conn.commit()
