import customtkinter as ctk
from tkinter import messagebox, Listbox, END
from datetime import datetime

import uzytkownik

def wyczysc_okno():
    for widget in root.winfo_children():
        widget.destroy()
    
def okno_menu():
    wyczysc_okno()

    button_logowanie = ctk.CTkButton(root, text="logowanie", command=okno_logowanie, **BUTTON)
    button_logowanie.pack(pady=150)

    button_rejestracja = ctk.CTkButton(root, text="rejestracja", command=okno_rejestracja, **BUTTON)
    button_rejestracja.pack(pady=25)

def okno_logowanie():
    wyczysc_okno()

    label_email = ctk.CTkLabel(root, text="e-mail", font=("Arial", 20))
    label_email.pack(pady=(75, 10))
    entry_email = ctk.CTkEntry(root, **ENTRY)
    entry_email.pack()

    label_haslo = ctk.CTkLabel(root, text="haslo", font=("Arial", 20))
    label_haslo.pack(pady=(25, 10))
    entry_haslo = ctk.CTkEntry(root, show="*", **ENTRY)
    entry_haslo.pack()

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

    button_zaloguj = ctk.CTkButton(root, text="zaloguj", command=zaloguj, **BUTTON)
    button_zaloguj.pack(pady=25)

    button_powrot = ctk.CTkButton(root, text="powrot", command=okno_menu, **BUTTON)
    button_powrot.pack(pady=25)
    
def okno_rejestracja():
    wyczysc_okno()

    label_login = ctk.CTkLabel(root, text="login", font=("Arial", 20))
    label_login.pack(pady=(50, 10))
    entry_login = ctk.CTkEntry(root, **ENTRY)
    entry_login.pack()
    
    label_email = ctk.CTkLabel(root, text="e-mail", font=("Arial", 20))
    label_email.pack(pady=(25, 10))
    entry_email = ctk.CTkEntry(root, **ENTRY)
    entry_email.pack()

    label_haslo = ctk.CTkLabel(root, text="haslo", font=("Arial", 20))
    label_haslo.pack(pady=(25, 10))
    entry_haslo = ctk.CTkEntry(root, show="*", **ENTRY)
    entry_haslo.pack()
 
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

    button_zarejestruj = ctk.CTkButton(root, text="zarejestruj", command=zarejestruj, **BUTTON)
    button_zarejestruj.pack(pady=25)

    button_powrot = ctk.CTkButton(root, text="powrot", command=okno_menu, **BUTTON)
    button_powrot.pack(pady=25)

def okno_pracownik(pracownik):
    wyczysc_okno()

    label_nazwa_pracownika = ctk.CTkLabel(root, text=f"panel pracownika: {pracownik.nazwa}", font=("Arial", 20))
    label_nazwa_pracownika.pack(pady=(75, 10))

    root.czas_pracy = 0
    root.licznik = False
    label_czas_pracy = ctk.CTkLabel(root, text="00:00:00", font=("Arial", 40))
    label_czas_pracy.pack(pady=(50, 10))

    def aktualizuj_licznik():
        if root.licznik:
            root.czas_pracy += 1

            h = root.czas_pracy // 3600
            m = (root.czas_pracy%3600) // 60
            s = root.czas_pracy % 60
            label_czas_pracy.configure(text=f"{h:02}:{m:02}:{s:02}")
            root.after(1000, aktualizuj_licznik)
            
    def rozpocznij_prace():
        wynik = pracownik.rozpocznijPrace()

        if wynik is True:
            root.czas_pracy = 0
            root.licznik = True
            label_czas_pracy.configure(text="00:00:00")
            root.after(1000, aktualizuj_licznik)
            button_wyloguj.configure(state="disabled", fg_color="#686868")
            messagebox.showinfo("sukces", "rozpoczeto prace!")
        else:
            messagebox.showinfo("blad", wynik)

    def zakoncz_prace():
        wynik = pracownik.zakonczPrace()

        if wynik is True:
            root.licznik = False
            button_wyloguj.configure(state="normal", fg_color="white")
            messagebox.showinfo("sukces", "zakonczono prace!")
        else:
            messagebox.showinfo("blad", wynik)

    button_start = ctk.CTkButton(root, text="rozpocznij prace", command=rozpocznij_prace, **BUTTON)
    button_start.pack(pady=(50, 25))

    button_stop = ctk.CTkButton(root, text="zakoncz prace", command=zakoncz_prace, **BUTTON)
    button_stop.pack(pady=25)

    button_wyloguj = ctk.CTkButton(root, text="wyloguj", command=okno_menu, **BUTTON)
    button_wyloguj.pack(pady=25)

def okno_administrator(administrator):
    wyczysc_okno()

    label_nazwa_administratora = ctk.CTkLabel(root, text=f"panel administratora: {administrator.nazwa}", font=("Arial", 20))
    label_nazwa_administratora.pack(pady=(75, 10))

    lista = Listbox(root, width=90, height=15, font=("Arial", 12))
    lista.pack(pady=20)

    def pokaz_raport():
        lista.delete(0, END)

        raport = administrator.wyswietlRaporty()
        if len(raport) == 0:
            lista.insert(END, "brak danych!")
            return

        for pracownik in raport:
            pracownik_id = pracownik[0]
            nazwa = pracownik[1]
            email = pracownik[2]
            czasy_pracy = pracownik[3]

            lista.insert(END, f"pracownik: {nazwa}, e-mail: {email}")
            if len(czasy_pracy) == 0:
                lista.insert(END, "brak wpisow czasu pracy!")
            else:
                for czas_pracy in czasy_pracy:
                    rejestr = uzytkownik.RejestrCzasu(pracownik_id)
                    liczba_godzin = rejestr.obliczCzas(czas_pracy[0], czas_pracy[1])
                    lista.insert(END, f"start: {czas_pracy[0]}, koniec: {czas_pracy[1]}, czas: {liczba_godzin}")
            lista.insert(END, "=========================")

    button_raport = ctk.CTkButton(root, text="wyswietl raport", command=pokaz_raport, **BUTTON)
    button_raport.pack(pady=15)

    button_wyloguj = ctk.CTkButton(root, text="wyloguj", command=okno_menu, **BUTTON)
    button_wyloguj.pack(pady=15)
        
ctk.set_appearance_mode("dark")    
root = ctk.CTk()
root.title("System rejestracji czasu pracy")
root.geometry("800x600")

BUTTON = {
    "width": 200,
    "height": 50,
    "corner_radius": 25,
    "border_width": 3,
    "border_color": "#242424",
    "fg_color": "white",
    "hover_color": "#686868", 
    "text_color": "black",
    "font": ("Arial", 20)
}
ENTRY = {
    "width": 300,
    "height": 50,
    "corner_radius": 25,
    "border_width": 3,
    "border_color": "#242424",
    "fg_color": "white",
    "text_color": "black",
    "font": ("Arial", 20)
}

okno_menu()
root.mainloop()
