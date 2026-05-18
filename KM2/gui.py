from tkinter import *
from tkinter import messagebox
from datetime import datetime

import uzytkownik

def wyczysc_okno():
    for widget in root.winfo_children():
        widget.destroy()
    
def okno_menu():
    wyczysc_okno()

    button_logowanie = Button(root, text="logowanie", font=("Arial", 20), command=okno_logowanie)
    button_logowanie.pack(pady=100)

    button_rejestracja = Button(root, text="rejestracja", font=("Arial", 20), command=okno_rejestracja)
    button_rejestracja.pack(pady=50)

def okno_logowanie():
    wyczysc_okno()

    label_email = Label(root, text="e-mail", font=("Arial", 20))
    label_email.pack()
    entry_email = Entry(root, font=("Arial", 20))
    entry_email.pack(pady=25)

    label_haslo = Label(root, text="haslo", font=("Arial", 20))
    label_haslo.pack()
    entry_haslo = Entry(root, show="*", font=("Arial", 20))
    entry_haslo.pack(pady=25)

    def zaloguj():
        email = entry_email.get()
        haslo = entry_haslo.get()

        user = uzytkownik.Uzytkownik()
        wynik = user.zaloguj(email, haslo)

        if wynik:
            messagebox.showinfo("sukces", f"witaj, {wynik.nazwa}!")
            if isinstance(wynik, uzytkownik.Pracownik):
                okno_pracownik(wynik)
            elif isinstance(wynik, uzytkownik.Administrator):
                okno_administrator(wynik)
        else:
            messagebox.showinfo("blad", "nieprawidlowy e-mail lub haslo!")

    button_zaloguj = Button(root, text="zaloguj", font=("Arial", 20), command=zaloguj)
    button_zaloguj.pack(pady=25)

    button_powrot = Button(root, text="powrot", font=("Arial", 20), command=okno_menu)
    button_powrot.pack(pady=25)
    
def okno_rejestracja():
    wyczysc_okno()

    label_login = Label(root, text="login", font=("Arial", 20))
    label_login.pack()
    entry_login = Entry(root, font=("Arial", 20))
    entry_login.pack(pady=10)
    
    label_email = Label(root, text="e-mail", font=("Arial", 20))
    label_email.pack()
    entry_email = Entry(root, font=("Arial", 20))
    entry_email.pack(pady=10)

    label_haslo = Label(root, text="haslo", font=("Arial", 20))
    label_haslo.pack()
    entry_haslo = Entry(root, show="*", font=("Arial", 20))
    entry_haslo.pack(pady=10)
 
    def zarejestruj():
        login = entry_login.get()
        email = entry_email.get()
        haslo = entry_haslo.get()

        user = uzytkownik.Uzytkownik()
        wynik = user.zarejestruj(login, email, haslo)

        if wynik is True:
            messagebox.showinfo("sukces", "pomyslnie zarejestrowano uzytkownika!")
            okno_menu()
        else:
            messagebox.showinfo("blad", wynik)

    button_zarejestruj = Button(root, text="zarejestruj", font=("Arial", 20), command=zarejestruj)
    button_zarejestruj.pack(pady=25)

    button_powrot = Button(root, text="powrot", font=("Arial", 20), command=okno_menu)
    button_powrot.pack(pady=25)

def okno_pracownik(pracownik):
    wyczysc_okno()

    label_nazwa_pracownika = Label(root, text=f"panel pracownika: {pracownik.nazwa}", font=("Arial", 20))
    label_nazwa_pracownika.pack()

    root.czas_pracy = 0
    root.licznik = False
    label_czas_pracy = Label(root, text="00:00:00", font=("Arial", 20))
    label_czas_pracy.pack()

    def aktualizuj_licznik():
        if root.licznik:
            root.czas_pracy += 1

            h = root.czas_pracy // 3600
            m = (root.czas_pracy%3600) // 60
            s = root.czas_pracy % 60
            label_czas_pracy.config(text=f"{h:02}:{m:02}:{s:02}")
            root.after(1000, aktualizuj_licznik)
            
    def rozpocznij_prace():
        wynik = pracownik.rozpocznijPrace()

        if wynik is True:
            root.czas_pracy = 0
            root.licznik = True
            label_czas_pracy.config(text="00:00:00")
            aktualizuj_licznik()
            
            messagebox.showinfo("sukces", "rozpoczeto prace!")
        else:
            messagebox.showinfo("blad", wynik)

    def zakoncz_prace():
        wynik = pracownik.zakonczPrace()

        if wynik is True:
            root.licznik = False
            messagebox.showinfo("sukces", "zakonczono prace!")
        else:
            messagebox.showinfo("blad", wynik)

    button_start = Button(root, text="rozpocznij prace", font=("Arial", 20), command=rozpocznij_prace)
    button_start.pack(pady=15)

    button_stop = Button(root, text="zakoncz prace", font=("Arial", 20), command=zakoncz_prace)
    button_stop.pack(pady=15)

    button_wyloguj = Button(root, text="wyloguj", font=("Arial", 20), command=okno_menu)
    button_wyloguj.pack(pady=15)

def okno_administrator(administrator):
    wyczysc_okno()

    label_nazwa_administratora = Label(root, text=f"panel administratora: {administrator.nazwa}", font=("Arial", 20))
    label_nazwa_administratora.pack()

    lista = Listbox(root, width=90, height=15, font=("Arial", 12))
    lista.pack(pady=20)

    def pokaz_raport():
        lista.delete(0, END)

        raport = administrator.wyswietlRaporty()
        if len(raport) == 0:
            lista.insert(END, "brak danych!")
            return

        for pracownik in raport:
            nazwa = pracownik[0]
            email = pracownik[1]
            czasy_pracy = pracownik[2]

            lista.insert(END, f"pracownik: {nazwa}, e-mail: {email}")
            if len(czasy_pracy) == 0:
                lista.insert(END, "brak wpisow czasu pracy!")
            else:
                for czas_pracy in czasy_pracy:
                    lista.insert(END, f"start: {czas_pracy[0]}, koniec: {czas_pracy[1]}")
            lista.insert(END, "=========================")

    button_raport = Button(root, text="wyswietl raport", font=("Arial", 20), command=pokaz_raport)
    button_raport.pack(pady=15)

    button_wyloguj = Button(root, text="wyloguj", font=("Arial", 20), command=okno_menu)
    button_wyloguj.pack(pady=15)
        
root = Tk()
root.title("System rejestracji czasu pracy")
root.geometry("640x480")

okno_menu()
root.mainloop()
