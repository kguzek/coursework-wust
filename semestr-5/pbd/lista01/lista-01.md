# Lista projektowa nr 1

Najważniejszym problemem schematu jest wzajemna zależność tabel `Bandy`
i `Kocury`: kot należy do bandy, a jej szef jest kotem. Nie da się więc
utworzyć obu tabel ze wszystkimi kluczami obcymi od razu. Odwołanie
`bandy.szef_bandy → kocury.pseudo` dodano jedynym `ALTER TABLE`, po utworzeniu
obu relacji. Przy wstawianiu danych bandy początkowo mają szefów ustawionych
na `NULL`; po dodaniu kotów uzupełnia je `UPDATE`. Pozwala to zachować
kontrolę kluczy obcych bez czasowego wyłączania ograniczeń.

W Oracle warunek `max_myszy >= min_myszy` wymaga ograniczenia tabelowego,
ponieważ kolumnowy `CHECK` nie może odwoływać się do innej kolumny.
Pozostałe proste warunki pozostają przy kolumnach, a klucz pary
`(pseudo, imie_wroga)` jest złożony i zapobiega zapisaniu kolejnego incydentu
tej samej pary. Zgodnie z poleceniem pola bez wymogu obowiązkowości dopuszczają
`NULL`: sam `CHECK` nie zastępuje `NOT NULL`.

Przeniesienie skryptu do PostgreSQL wymaga zamiany `VARCHAR2(n)` na
`varchar(n)`, `NUMBER(p)` na `numeric(p)` oraz `SYSDATE` na `CURRENT_DATE`.
Ta ostatnia zmiana nie jest całkowicie równoważna: Oracle `DATE` przechowuje
także czas, a PostgreSQL `date` tylko datę. Dla danych z zadania wystarcza
dokładność do dnia. W skrypcie Oracle zastosowano pokazane w materiałach
`INSERT ALL … SELECT 1 FROM dual`, a w PostgreSQL wielowierszowe `VALUES`.
To wybór zapisu, nie ograniczenie nowszych Oracle: od wersji 23ai dostępne
jest również wielowierszowe `VALUES`. Literały `DATE 'YYYY-MM-DD'` działają
w obu systemach i uniezależniają wstawianie dat od ustawień ich formatu.

Skrypty uruchomiono w PostgreSQL 18.4 przez pgAdmin oraz Oracle
Database Free (23.26.3) przez SQL Developer. W obu uzyskano 8 funkcji,
5 band, 18 kotów, 10 wrogów i 18 incydentów, bez brakujących powiązań.
Każdy system odrzucił 12 prób naruszenia ograniczeń; poprawnie działały też
domyślna data, opcjonalne pola i wielokrotne `NULL` w kolumnach unikalnych.
Inicjalizację Oracle ograniczono do pierwszego uruchomienia i osobnego
użytkownika `KONRAD`, zamiast tworzyć tabele jako `SYS` przy każdym starcie.
Restart zachował dane i nie powtórzył inicjalizacji. Pełne dane i wyniki testów
Oracle zawiera [zapis wykonania](results/oracle.txt). Oba SZBD wystarczają do realizacji zadania;
przeniesienie schematu wymaga niewielkich zmian, ale różnice w regułach
`CHECK` i znaczeniu typu `DATE` nie pozwalają traktować dialektów jako identycznych.
