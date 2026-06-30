import sqlite3
import os


class DatabaseManager:

    def __init__(self):
        # Créer le dossier si inexistant
        os.makedirs("./database", exist_ok=True)

        self.conn = sqlite3.connect("./database/DATABASSES.db")
        self.conn.row_factory = sqlite3.Row 
        self.cusor = self.conn.cursor()
        self.create_tables()


    def create_tables(self):
        self.cusor.executescript('''
            CREATE TABLE IF NOT EXISTS utilisateurs (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                nom         TEXT NOT NULL,
                prenom      TEXT NOT NULL,
                email       TEXT NOT NULL UNIQUE,
                mot_de_passe TEXT NOT NULL,
                role        TEXT NOT NULL CHECK(role IN ('admin', 'professeur', 'etudiant'))
            );

            CREATE TABLE IF NOT EXISTS professeurs (
                id         INTEGER PRIMARY KEY AUTOINCREMENT,
                nom        TEXT NOT NULL,
                prenom     TEXT NOT NULL,
                matiere_id INTEGER,
                FOREIGN KEY (matiere_id) REFERENCES matieres(id)
            );

            CREATE TABLE IF NOT EXISTS etudiants (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                matricule TEXT NOT NULL UNIQUE,
                nom TEXT NOT NULL,
                prenom TEXT NOT NULL,
                age INTEGER NOT NULL,
                classe_id INTEGER NOT NULL,
                id_user INTEGER UNIQUE,
                FOREIGN KEY (classe_id) REFERENCES classes(id),
                FOREIGN KEY (id_user) REFERENCES utilisateurs(id)
                );
            

            CREATE TABLE IF NOT EXISTS matieres (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                nom_matiere TEXT NOT NULL 
            );

            CREATE TABLE IF NOT EXISTS notes (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                etudiant_id INTEGER NOT NULL,
                matiere_id  INTEGER NOT NULL,
                note        REAL NOT NULL,
                FOREIGN KEY (etudiant_id) REFERENCES etudiants(id),
                FOREIGN KEY (matiere_id)  REFERENCES matieres(id)
            );

            CREATE TABLE IF NOT EXISTS absences (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                etudiant_id INTEGER NOT NULL,
                matiere_id  INTEGER NOT NULL,
                date        TEXT NOT NULL,
                status      TEXT NOT NULL CHECK(status IN ('justifiée', 'non justifiée')),
                FOREIGN KEY (etudiant_id) REFERENCES etudiants(id),
                FOREIGN KEY (matiere_id)  REFERENCES matieres(id)
            ); 
        ''')
        self.conn.commit()

    def migrate_tables(self):

        self.cusor.execute('''
            CREATE TABLE IF NOT EXISTS classes (
                id         INTEGER PRIMARY KEY AUTOINCREMENT,
                nom_classe TEXT NOT NULL
            )
        ''')

        try:
            self.cusor.execute(
                "ALTER TABLE etudiants ADD COLUMN classe_id INTEGER REFERENCES classes(id)"
            )
            print("[migration] classe_id ajouté à etudiants.")
        except Exception:
            pass

        try:
            self.cusor.execute(
                "ALTER TABLE etudiants ADD COLUMN id_user INTEGER UNIQUE REFERENCES utilisateurs(id)"
            )
            print("[migration] id_user ajouté à etudiants.")
        except Exception:
            pass

        try:
            self.cusor.execute(
                "ALTER TABLE professeurs ADD COLUMN classe_id INTEGER REFERENCES classes(id)"
            )
            print("[migration] classe_id ajouté à professeurs.")
        except Exception:
            pass


        try:
            self.cusor.execute(
                "ALTER TABLE professeurs ADD COLUMN id_user INTEGER UNIQUE REFERENCES utilisateurs(id)"
            )
            print("[migration] id_user ajouté à professeurs.")
        except Exception:
            pass

        self.conn.commit()
        print("[migration] Terminée.")

    def suprimer_table(self):
            self.cusor.executescript('''
            DROP TABLE etudiants
            ''')

    def creer_super_admin(self):
        try:
            self.cusor.execute(
                "SELECT id FROM utilisateurs WHERE email = ?",
                ("admin@gmail.com",)
            )
            if self.cusor.fetchone() is None:
                self.cusor.execute(
                    """
                    INSERT INTO utilisateurs (nom, prenom, email, mot_de_passe, role)
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    ("Super", "Admin", "admin@gmail.com", "admin123", "admin")
                )
                self.conn.commit()
                print("Super administrateur créé avec succès.")
            else:
                print("Super administrateur déjà existant.")
        except sqlite3.Error as e:

            print(f"Erreur lors de la création du super admin : {e}")
