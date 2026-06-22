import setup_db
import database

setup_db.create_db()
baza = database.BazaDanych()
if baza.polacz():
    baza.utworzTabele()

import gui
