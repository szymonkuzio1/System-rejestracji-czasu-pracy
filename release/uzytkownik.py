import database

import secrets
import argon2

password_hasher = argon2.PasswordHasher(memory_cost=12288, time_cost=3, parallelism=1)

class Uzytkownik:
    def __init__(self, id=None, nazwa=None, email=None, rola=None):
        self.id = id
        self.nazwa = nazwa
        self.email = email
        self.rola = rola

    def zarejestruj(self, nazwa_uzytkownika, email, haslo):
        wynik_polityki = self.polityka_hasel(haslo)
        if wynik_polityki is not True:
            return wynik_polityki
    
        salt = secrets.token_hex(4)
        haslo_z_sola = haslo+salt
        zahashowane_haslo = password_hasher.hash(haslo_z_sola)

        dane = (nazwa_uzytkownika, email, zahashowane_haslo, salt)
        baza = database.BazaDanych()
        if baza.polacz():
            if baza.zapisz(dane):
                print(f"zarejestrowano uzytkownika {nazwa_uzytkownika}!\n")
                return True
            else:
                return "konto o podanym adresie e-mail juz istnieje!"
        return False

    def zaloguj(self, email, haslo):
        baza = database.BazaDanych()
        if not baza.polacz():
            return False
    
        sql = """
            SELECT id, nazwa_uzytkownika, email, zahashowane_haslo, salt, rola
            FROM Uzytkownicy
            WHERE email = %s"""

        wynik = baza.pobierz(sql, (email,))

        if len(wynik) == 0:
            print("nieprawidlowy e-mail lub haslo!\n")
            return False

        user = wynik[0]
        id = user[0]
        nazwa_uzytkownika = user[1]
        email = user[2]
        zahashowane_haslo = user[3]
        salt = user[4]
        rola=user[5]

        haslo_z_sola = haslo+salt

        try:
            password_hasher.verify(zahashowane_haslo, haslo_z_sola)
            if rola == "pracownik":
                return Pracownik(id, nazwa_uzytkownika, email, rola)
            if rola == "administrator":
                return Administrator(id, nazwa_uzytkownika, email, rola)
        except:
            return False
    
    def czy_popularne_haslo(self, haslo):
        with open("wordlist_pl.txt", 'r', encoding="utf-8") as file:
            popularne_hasla = file.read().splitlines()
            return haslo.lower() in [h.lower() for h in popularne_hasla]
    
    def polityka_hasel(self, haslo):
        if len(haslo)<12:
            return "haslo musi miec minimum 12 znakow!"
        if len(haslo)>128:
            return "haslo nie moze miec wiecej niz 128 znakow!"
        if self.czy_popularne_haslo(haslo):
            return "zbyt popularne haslo!"
        return True

class Pracownik(Uzytkownik):
    def rozpocznijPrace(self):
        rejestr = RejestrCzasu(self.id)
        return rejestr.zapiszStart()

    def zakonczPrace(self):
        rejestr = RejestrCzasu(self.id)
        return rejestr.zapiszKoniec()

class Administrator(Uzytkownik):
    def wyswietlRaporty(self):
        baza = database.BazaDanych()
        if not baza.polacz():
            return []

        sql_pracownicy = """
            SELECT id, nazwa_uzytkownika, email
            FROM Uzytkownicy
            WHERE rola = %s
            """

        pracownicy = baza.pobierz(sql_pracownicy, ("pracownik",))
        raport = []

        for pracownik in pracownicy:
            pracownik_id = pracownik[0]
            nazwa = pracownik[1]
            email = pracownik[2]

            sql_czas_pracy = """
            SELECT godzina_rozpoczecia, godzina_zakonczenia
            FROM czas_pracy
            WHERE pracownik_id = %s
            ORDER BY id DESC
            """

            czas_pracy = baza.pobierz(sql_czas_pracy, (pracownik_id,))
            raport.append((pracownik_id, nazwa, email, czas_pracy))

        return raport

class RejestrCzasu:
    def __init__(self, pracownik_id):
        self.pracownik_id = pracownik_id

    def zapiszStart(self):
        baza = database.BazaDanych()
        if not baza.polacz():
            return False

        sql_aktywnosc_pracownika = """
            SELECT id
            FROM czas_pracy
            WHERE pracownik_id = %s AND godzina_zakonczenia IS NULL
            ORDER BY id DESC
            LIMIT 1
            """
        aktywnosc_pracownika = baza.pobierz(sql_aktywnosc_pracownika, (self.pracownik_id,))

        if len(aktywnosc_pracownika) > 0:
            return "rozpoczeto prace!"

        sql_rozpoczecie_pracy = """
            INSERT INTO czas_pracy (pracownik_id, godzina_rozpoczecia, godzina_zakonczenia)
            VALUES (%s, NOW(), NULL)
            """
        baza.cursor.execute(sql_rozpoczecie_pracy, (self.pracownik_id,))
        baza.mydb.commit()
        return True

    def zapiszKoniec(self):
        baza = database.BazaDanych()
        if not baza.polacz():
            return False

        sql_aktywnosc_pracownika = """
            SELECT id
            FROM czas_pracy
            WHERE pracownik_id = %s AND godzina_zakonczenia IS NULL
            ORDER BY id DESC
            LIMIT 1
            """
        aktywnosc_pracownika = baza.pobierz(sql_aktywnosc_pracownika, (self.pracownik_id,))

        if len(aktywnosc_pracownika) == 0:
            return "rozpocznij prace!"

        id_rejestru = aktywnosc_pracownika[0][0]
        
        sql_zakonczenie_pracy = """
            UPDATE czas_pracy SET godzina_zakonczenia = NOW()
            WHERE id = %s
            """
        baza.cursor.execute(sql_zakonczenie_pracy, (id_rejestru,))
        baza.mydb.commit()
        return True

    def obliczCzas(self, godzina_rozpoczecia, godzina_zakonczenia):
        if godzina_rozpoczecia is None or godzina_zakonczenia is None:
            return "00:00:00"
        roznica = godzina_zakonczenia - godzina_rozpoczecia
        sekundy = int(roznica.total_seconds())
        
        h = sekundy // 3600
        m = (sekundy%3600) // 60
        s = sekundy % 60
        return f"{h:02}:{m:02}:{s:02}"
