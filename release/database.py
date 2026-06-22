import setup_db

import mysql.connector

class BazaDanych:
    def __init__(self):
        self.mydb = None
        self.cursor = None

    def polacz(self):
        self.mydb = mysql.connector.connect(
            host = "localhost",
            user = "root",
            password = "",
            database = setup_db.db
        )

        self.cursor = self.mydb.cursor()
        return True

    def zapisz(self, dane):
        sql = """
            INSERT INTO Uzytkownicy (nazwa_uzytkownika, email, zahashowane_haslo, salt)
            VALUES (%s, %s, %s, %s)"""
        try:
            self.cursor.execute(sql, dane)
            self.mydb.commit()
            return True
        except Exception as e:
            print(e)
            return False
        
    def pobierz(self, zapytanie, dane=None):
        if dane is None:
            self.cursor.execute(zapytanie)
        else:
            self.cursor.execute(zapytanie, dane)
        return self.cursor.fetchall()

    def utworzTabele(self):
        uzytkownicy_sql = """
            CREATE TABLE IF NOT EXISTS Uzytkownicy
            (id INT PRIMARY KEY AUTO_INCREMENT,
            nazwa_uzytkownika VARCHAR(255),
            email VARCHAR(255) UNIQUE,
            zahashowane_haslo VARCHAR(255),
            salt VARCHAR(255),
            rola ENUM('pracownik', 'administrator') DEFAULT 'pracownik')
            """
        self.cursor.execute(uzytkownicy_sql)

        czas_pracy_sql = """
            CREATE TABLE IF NOT EXISTS Czas_pracy
            (id INT PRIMARY KEY AUTO_INCREMENT,
            pracownik_id INT,
            godzina_rozpoczecia DATETIME,
            godzina_zakonczenia DATETIME,
            FOREIGN KEY (pracownik_id) REFERENCES Uzytkownicy(id))
            """
        self.cursor.execute(czas_pracy_sql)
        
        self.mydb.commit()
        print("utworzono tabele Uzytkownicy")
        print("utworzono tabele Czas_pracy")
        return True
        
