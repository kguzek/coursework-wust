# Database Schema Documentation

This document describes the structure of a school management database (MS Access dialect). It is designed to provide context for AI agents generating SQL queries.

## Tables and Fields

### 1. Uczniowie (Students)
* **IdU** (Primary Key): Unique identifier for a student.
* **Nazwisko**: Student's last name.
* **Imie**: Student's first name.
* **DUr**: Date of birth (*Data Urodzenia*).
* **Plec**: Gender.
* **Klasa** (Foreign Key): Links to `Klasy.Symbol`.
* **Miasto** (Foreign Key): Implicit from relationships, links to `Miasta.IdM` (Note: scrolled out of view in the ERD diagram, but the relationship line exists).

### 2. Klasy (Classes)
* **Symbol** (Primary Key): Unique class identifier (e.g., '1A').
* **Profil**: Class profile/specialization.
* **Wych** (Foreign Key): Form tutor / homeroom teacher. Links to `Nauczyciele.IdN`.

### 3. Miasta (Cities)
* **IdM** (Primary Key): Unique identifier for a city.
* **NazwaM**: Name of the city.

### 4. Nauczyciele (Teachers)
* **IdN** (Primary Key): Unique identifier for a teacher.
* **Nazwisko**: Teacher's last name.
* **Imie**: Teacher's first name.
* **DZatr**: Date of employment (*Data Zatrudnienia*).
* **DUr**: Date of birth (*Data Urodzenia*).
* **Plec**: Gender.
* **Pensja**: Base salary.
* **Premia**: Bonus.
* **Pensum**: Teaching hours quota.
* **Telefon**: Phone number.

### 5. Oceny (Grades)
* **IdU** (Primary Key / Foreign Key): Links to `Uczniowie.IdU`.
* **IdP** (Primary Key / Foreign Key): Links to `Przedmioty.IdP`.
* **Ocena**: The grade value.
* **DataO**: Date the grade was given (*Data Oceny*).

### 6. Przedmioty (Subjects)
* **IdP** (Primary Key): Unique identifier for a subject.
* **NazwaP**: Name of the subject.

### 7. Uczy (Teaches - Junction Table)
* **IdN** (Primary Key / Foreign Key): Links to `Nauczyciele.IdN`.
* **IdP** (Primary Key / Foreign Key): Links to `Przedmioty.IdP`.
* **IleGodz**: Number of hours taught.

---

## Relationships (Joins)

When constructing SQL queries, use the following `ON` clauses for `JOIN` operations:

1.  **Uczniowie & Klasy** (Many-to-1):
    `Uczniowie.Klasa = Klasy.Symbol`
2.  **Uczniowie & Miasta** (Many-to-1):
    `Uczniowie.Miasto = Miasta.IdM` *(Assuming the foreign key in Uczniowie is named 'Miasto' based on standard conventions and previous context)*
3.  **Uczniowie & Oceny** (1-to-Many):
    `Uczniowie.IdU = Oceny.IdU`
4.  **Klasy & Nauczyciele** (Many-to-1):
    `Klasy.Wych = Nauczyciele.IdN`
5.  **Oceny & Przedmioty** (Many-to-1):
    `Oceny.IdP = Przedmioty.IdP`
6.  **Nauczyciele & Uczy** (1-to-Many):
    `Nauczyciele.IdN = Uczy.IdN`
7.  **Przedmioty & Uczy** (1-to-Many):
    `Przedmioty.IdP = Uczy.IdP`

## Notes for AI Agents
* **Dialect**: Use standard SQL compatible with **MS Access** (Jet SQL).
* **String Literals**: Use single quotes (`'string'`) or double quotes (`"string"`) for text values.
* **Wildcards**: MS Access traditionally uses `*` for multiple characters and `?` for single characters in `LIKE` clauses (though `%` and `_` may work in ADO/OLEDB contexts; default to standard SQL `%` unless strict Access UI syntax is requested).
* **Joins**: MS Access requires parentheses when chaining multiple `INNER JOIN` clauses. E.g., `FROM ((Table1 INNER JOIN Table2 ON ...) INNER JOIN Table3 ON ...)`.
* **Polish locale**: Be mindful of sql differences between polish vs english sql in access. Use polish one.

## Example working query
SELECT
    Uczniowie.[IdU],
    Uczniowie.[Nazwisko],
    Uczniowie.[Imie]
FROM
    Uczniowie
    INNER JOIN Miasta ON Uczniowie.[Miasto] = Miasta.[IdM]
WHERE
    Miasta.[NazwaM] IN ('Brzeg', 'Brzeg Dolny', 'Poznań');