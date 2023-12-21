import sqlite3
from PyQt6.QtWidgets import (QApplication, QWidget, QPushButton, QLabel,
                             QLineEdit, QGridLayout, QTableWidget, QTableWidgetItem)


class AddressBook (QWidget):
    def __init__(self):
        super ().__init__ ()
        self.initUI ()
        self.createDB ()
        self.setWindowTitle ("AddressBook")
        self.setGeometry (100, 100, 600, 400)

    def initUI(self):
        # Create GUI elements
        self.nameLabel = QLabel ("Name")
        self.nameEdit = QLineEdit ()

        self.emailLabel = QLabel ("Email")
        self.emailEdit = QLineEdit ()

        self.addButton = QPushButton ("Add")
        self.addButton.clicked.connect (self.addContact)

        self.displayButton = QPushButton ("Display Contacts")
        self.displayButton.clicked.connect (self.displayContacts)

        # Set layout
        layout = QGridLayout ()
        layout.addWidget (self.nameLabel, 0, 0)
        layout.addWidget (self.nameEdit, 0, 1)

        layout.addWidget (self.emailLabel, 1, 0)
        layout.addWidget (self.emailEdit, 1, 1)

        layout.addWidget (self.addButton, 2, 0)
        layout.addWidget (self.displayButton, 2, 1)

        self.contactsTable = QTableWidget ()
        layout.addWidget (self.contactsTable, 3, 0, 1, 2)

        self.setLayout (layout)

    def createDB(self):
        # Create database and table
        self.conn = sqlite3.connect ("contacts.db")
        q = """CREATE TABLE IF NOT EXISTS 
             contacts(id integer PRIMARY KEY, name text, email text)"""
        self.conn.execute (q)

    def addContact(self):
        name = self.nameEdit.text ()
        email = self.emailEdit.text ()

        q = f"INSERT INTO contacts (name, email) VALUES ('{name}','{email}')"
        self.conn.execute (q)
        self.conn.commit ()

    def displayContacts(self):
        contacts = self.conn.execute ("SELECT * FROM contacts")
        self.contactsTable.setRowCount (0)

        for row_number, row_data in enumerate (contacts):
            self.contactsTable.insertRow (row_number)
            for column_number, data in enumerate (row_data):
                self.contactsTable.setItem (row_number,
                                            column_number,
                                            QTableWidgetItem (str (data)))


app = QApplication ([])
ab = AddressBook ()
ab.show ()
app.exec ()