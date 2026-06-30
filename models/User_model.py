from database.bd import DatabaseManager


class UtilisateurModels(DatabaseManager):

    def ajouter_utilisateur(self, email, mot_de_passe, role, nom="", prenom=""):
        
        try:
            self.cusor.execute(
                '''
                INSERT INTO utilisateurs (nom, prenom, email, mot_de_passe, role)
                VALUES (?, ?, ?, ?, ?)
                ''',
                (nom, prenom, email, mot_de_passe, role)
            )
            self.conn.commit()
        except Exception as e:
            print(f"Erreur ajout utilisateur : {e}")

    def lister_utilisateurs(self):
        self.cusor.execute('''SELECT id, nom, prenom, email, role FROM utilisateurs''')
        return self.cusor.fetchall()

    def supprimer_utilisateur(self, utilisateur_id):
        self.cusor.execute(
            '''DELETE FROM utilisateurs WHERE id = ?''',
            (utilisateur_id,)
        )
        self.conn.commit()

    def modifier_utilisateur(self, utilisateur_id, nouveau_email=None,
                              nouveau_mot_de_passe=None, nouveau_role=None):
        """
        Correction : modification partielle — seuls les champs fournis sont mis à jour.
        L'ancienne version ne modifiait que le mot de passe.
        """
        champs, valeurs = [], []

        if nouveau_email:
            champs.append("email = ?")
            valeurs.append(nouveau_email)
        if nouveau_mot_de_passe:
            champs.append("mot_de_passe = ?")
            valeurs.append(nouveau_mot_de_passe)
        if nouveau_role:
            champs.append("role = ?")
            valeurs.append(nouveau_role)

        if not champs:
            print("Aucun champ à modifier.")
            return

        valeurs.append(utilisateur_id)
        self.cusor.execute(
            f"UPDATE utilisateurs SET {', '.join(champs)} WHERE id = ?",
            valeurs
        )
        self.conn.commit()

    def rechercher_utilisateur(self, email):
        """
        Retourne un sqlite3.Row (accès par clé grâce à row_factory).
        Ex : utilisateur["mot_de_passe"], utilisateur["role"]
        """
        self.cusor.execute(
            '''SELECT * FROM utilisateurs WHERE email = ?''',
            (email,)
        )
        return self.cusor.fetchone()

    def rechercher_utilisateur_par_id(self, utilisateur_id):
        self.cusor.execute(
            '''SELECT * FROM utilisateurs WHERE id = ?''',
            (utilisateur_id,)
        )
        return self.cusor.fetchone()
