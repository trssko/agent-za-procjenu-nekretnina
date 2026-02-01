# Housing Valuation Agent

Ovaj projekat je implementacija inteligentnog softverskog agenta za procjenu nekretnina, razvijena kao dio predmeta Umjetna Inteligencija.

## 🚀 Brzo Pokretanje (Windows)

Najlakši način za pokretanje aplikacije je korištenje priložene skripte:

1.  Pronađite fajl **`start_app.bat`** u ovom folderu.
2.  Dupli klik na njega.
3.  Otvorit će se dva crna prozorčića (Backend i Frontend). **Ne zatvarajte ih!**
4.  Aplikacija će se automatski otvoriti u vašem browseru na: `http://localhost:5173`

---

## 🏗️ Tehnička Struktura

Projekat prati "Clean Architecture":

*   `core/` - Osnovni interfejsi agenta.
*   `shared/` - Poslovna logika, entiteti i ML modeli.
*   `web/` - FastAPI server.
*   `frontend/` - React aplikacija.

## 📦 Zahtjevi

*   Python 3.10+
*   Node.js (v18+)

Ako pokrećete ručno:
1.  Backend: `py -m uvicorn web.main:app --reload`
2.  Frontend: `cd frontend` -> `npm run dev`

---
---

# 🇬🇧 English Version

# Housing Valuation Agent

This project is an implementation of an intelligent software agent for real estate valuation, developed as part of the Artificial Intelligence course.

## 🚀 Quick Start (Windows)

The easiest way to run the application is to use the included script:

1.  Find the **`start_app.bat`** file in this folder.
2.  Double-click it.
3.  Two black windows will open (Backend and Frontend). **Do not close them!**
4.  The application will automatically open in your browser at: `http://localhost:5173`

---

## 🏗️ Technical Structure

The project follows "Clean Architecture":

*   `core/` - Basic agent interfaces.
*   `shared/` - Business logic, entities, and ML models.
*   `web/` - FastAPI server.
*   `frontend/` - React application.

## 📦 Requirements

*   Python 3.10+
*   Node.js (v18+)

If running manually:
1.  Backend: `py -m uvicorn web.main:app --reload`
2.  Frontend: `cd frontend` -> `npm run dev`
