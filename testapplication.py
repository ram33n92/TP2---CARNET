import sys
import sqlite3
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QLineEdit, QVBoxLayout, QTableWidget, \
    QTableWidgetItem, QHBoxLayout, QInputDialog


class Application(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Carnet Addresse")
        self.setGeometry(100, 100, 600, 600)
        self.Creation_db()
        self.interface_app()

    def interface_app(self):

        ###CRÉATION LABEL
        self.label_nom = QLabel("Nom")
        self.ligne_nom = QLineEdit()

        self.label_prenom = QLabel("Prenom")
        self.ligne_prenom = QLineEdit()

        self.label_email = QLabel("Email")
        self.ligne_email = QLineEdit()

        self.label_tel = QLabel("Telephone")
        self.ligne_tel = QLineEdit()

        ###CREATION BTN
        self.btn_ajouter = QPushButton("Ajouter")
        self.btn_ajouter.clicked.connect(self.Ajouter_contact)

        self.btn_supprimer = QPushButton("Supprimer")
        self.btn_supprimer.clicked.connect(self.supprimer_contact)

        self.btn_modifier = QPushButton("Modifier")
        self.btn_modifier.clicked.connect(self.modifier_contact)

        self.btn_charger = QPushButton("Charger")
        self.btn_charger.clicked.connect(self.charger_contact)

        ###RAJOUT TABLE AFFICHAGE
        self.tableau = QTableWidget()
        self.tableau.setColumnCount(4)
        self.tableau.setHorizontalHeaderLabels(["Nom", "Prenom", "Email", "Telephone"])

        ###LAYOUT
        layout = QVBoxLayout()
        layout2 = QVBoxLayout()
        layout2.addWidget(self.label_prenom)
        layout2.addWidget(self.ligne_prenom)
        layout2.addWidget(self.label_nom)
        layout2.addWidget(self.ligne_nom)
        layout2.addWidget(self.label_email)
        layout2.addWidget(self.ligne_email)
        layout2.addWidget(self.label_tel)
        layout2.addWidget(self.ligne_tel)
        layout2.addWidget(self.btn_ajouter)
        layout2.addWidget(self.btn_modifier)
        layout2.addWidget(self.btn_supprimer)
        layout2.addWidget(self.btn_charger)

        layout_tableau = QHBoxLayout()
        layout_tableau.addWidget(self.tableau)

        layout.addLayout(layout2)
        layout.addLayout(layout_tableau)

        self.setLayout(layout)

    def Creation_db(self):
        self.conn = sqlite3.connect("carnet.db")
        self.cur = self.conn.cursor()
        print("Base de donnée crée")
        self.cur.execute("CREATE TABLE IF NOT EXISTS carnet (prenom TEXT, nom TEXT, tel TEXT, courriel TEXT);")
        self.conn.commit()
        self.conn.close()

    def Afficher_tableau(self):
        self.tableau.clearContents()

        conn = sqlite3.connect("carnet.db")
        requette = "SELECT * FROM carnet;"
        cur = conn.cursor()
        cur.execute(requette)
        conn.commit()
        resultat = cur.fetchall()
        self.tableau.setRowCount(len(resultat))
        self.tableau.setColumnCount(4)

        for i in range(len(resultat)):
            for j in range(4):
                item = QTableWidgetItem(str(resultat[i][j]))
                self.tableau.setItem(i, j, item)
        conn.close()

    def Ajouter_contact(self):
        self.conn = sqlite3.connect("carnet.db")
        self.cur = self.conn.cursor()
        prenom = self.ligne_prenom.text()
        nom = self.ligne_nom.text()
        tel = self.ligne_tel.text()
        courriel = self.ligne_email.text()

        if prenom and nom and tel and courriel:
            try:

                self.cur.execute("INSERT INTO carnet VALUES (?, ?, ?, ?);", (prenom, nom, tel, courriel))
                self.conn.commit()


                print("Data inserted successfully")

                self.ligne_prenom.clear()
                self.ligne_nom.clear()
                self.ligne_tel.clear()
                self.ligne_email.clear()

                self.Afficher_tableau()
            except sqlite3.Error as e:
                print("ERREUR", e)


        self.conn.close()
        self.Afficher_tableau()

    def charger_contact(self):
        try:
            self.conn = sqlite3.connect("carnet.db")
            self.cur = self.conn.cursor()
            self.cur.execute("SELECT * FROM carnet;")

            num_rows = self.cur.rowcount

            self.tableau.setRowCount(num_rows)

            contacts = self.cur.fetchall()

            for rangee, contact in enumerate(contacts):
                for colonne, contact2 in enumerate(contact):
                    item = QTableWidgetItem(str(contact2))
                    self.tableau.setItem(rangee, colonne, item)

        except Exception as e:
            print("ERREUR:", e)

        finally:
            if hasattr(self, 'conn'):
                self.conn.close()
        self.Afficher_tableau()

    def modifier_contact(self):
        try:
            rangee = self.tableau.currentRow()

            if rangee >= 0:
                prenom_initial = self.tableau.item(rangee, 0).text()
                nom_initial = self.tableau.item(rangee, 1).text()
                tel_initial = self.tableau.item(rangee, 2).text()
                courriel_initial = self.tableau.item(rangee, 3).text()

                print("Avant modification:", prenom_initial, nom_initial, tel_initial, courriel_initial)
                nouveau_prenom, ok = QInputDialog.getText(self, "Modifier Contact", "Nouveau prénom:", text=prenom_initial)
                if ok:
                    nouveau_nom, ok = QInputDialog.getText(self, "Modifier Contact", "Nouveau nom:", text=nom_initial)
                    if ok:
                        nouveau_tel, ok = QInputDialog.getText(self, "Modifier Contact", "Nouveau téléphone:", text=tel_initial)
                        if ok:
                            nouveau_courriel, ok = QInputDialog.getText(self, "Modifier Contact", "Nouveau courriel:", text=courriel_initial)
                            if ok:
                                conn = sqlite3.connect("carnet.db")
                                cur = conn.cursor()
                                cur.execute(
                                    "UPDATE carnet SET prenom = ?, nom = ?, email = ?, telephone = ? WHERE prenom = ? AND nom = ? AND email = ? AND telephone = ?;",
                                    (nouveau_prenom, nouveau_nom, nouveau_tel, nouveau_courriel, prenom_initial,
                                     nom_initial, tel_initial, courriel_initial))
                                conn.commit()
                                conn.close()

                                print("Après modification:", nouveau_prenom, nouveau_nom, nouveau_tel, nouveau_courriel)
                                self.Afficher_tableau()

        except Exception as e:
            print("ERREUR:", e)

    def supprimer_contact(self):
        try:
            conn = sqlite3.connect("carnet.db")
            cur = conn.cursor()
            rangee = self.tableau.currentRow()

            if rangee >= 0:
                prenom_item = self.tableau.item(rangee, 0)
                nom_item = self.tableau.item(rangee, 1)
                courriel_item = self.tableau.item(rangee, 2)
                tel_item = self.tableau.item(rangee, 3)

                if prenom_item and nom_item and courriel_item and tel_item:
                    prenom = prenom_item.text()
                    nom = nom_item.text()
                    courriel = courriel_item.text()
                    tel = tel_item.text()

                    cur.execute("DELETE FROM carnet WHERE prenom = ? AND nom = ? AND email = ? AND telephone = ?;",
                                (prenom, nom, courriel, tel))

                    conn.commit()
                    conn.close()

                    print("Contact supprimé avec succès!")
                    self.Afficher_tableau()

        except Exception as e:
            print("ERREUR:", e)

if __name__ == "__main__":
    app = QApplication([])
    carnet_add_app = Application()
    carnet_add_app.show()
    sys.exit(app.exec())
