# Lista projektowa nr 4

Zapytania korzystają ze schematu i danych z pierwszej listy, bez zmian.
[Skrypt Oracle](sql/oracle-01_queries.sql) i
[skrypt PostgreSQL](sql/postgres-01_queries.sql) obejmują wszystkie zadania
1–12, łącznie z podpunktami 3a, 11a–c i 12a–b. Zadania 1–4 nie używają
podzapytań. „Całkowity przydział” oznacza wszędzie
`przydzial_myszy + COALESCE(myszy_extra, 0)`, bo brak dodatku zapisano jako
`NULL`. Wyjątkiem jest zadanie 9, w którym przykład odpowiada przydziałowi
podstawowemu: z dodatkiem `MALA` (22 + 42) przekroczyłaby próg funkcji
`MILUSIA` i pojawiłaby się w wyniku.

Tabele przestawne z zadań 1 i 2 zbudowano z `SUM(CASE ...)` po złączeniu,
bez podzapytań. Brak `ELSE` daje `NULL` zamiast 0, więc puste pola odpowiadają
przykładowi; dotyczy to również liczby kotów, liczonej jako
`SUM(CASE ... THEN 1 END)`. W zadaniu 3 funkcja bez kotów wymaga trzech
zabezpieczeń: `LEFT JOIN`, `COUNT(k.pseudo)` zamiast `COUNT(*)` i
`COALESCE` dla sumy. Wariant 3a pokazuje oba błędy: zwykłe złączenie gubi
funkcję `HONOROWA`, a `LEFT JOIN` z `COUNT(*)` przypisuje jej jednego kota,
bo liczy wiersz uzupełniony wartościami `NULL`, i pustą sumę zamiast 0.
`AVG` pomija `NULL`, więc średnia pustej funkcji pozostaje pusta bez dzielenia
przez zero. W zadaniu 4 podzapytanie o datę Jacka zastępuje samozłączenie.

W zadaniu 5 remis na drugim miejscu rozstrzyga `ROW_NUMBER()` z sortowaniem
po pseudonimie: w bandzie `LACIACI MYSLIWI` `DAMA` i `MAN` zjadają po 51,
wybrana jest `DAMA`, jak w przykładzie. `RANK()` zwróciłby oba koty. W zadaniu
6 użyto właśnie `RANK()`, aby przy remisie pokazać wszystkich rekordzistów.
Puste bandy i funkcje zachowuje `LEFT JOIN`, a ocena `NULL` pozostaje pusta.
Zadanie 7 zamiast widoku używa wyrażenia `WITH`; liczba równa średniej
trafiłaby do grupy „od dołu”. W zadaniu 8 kolejne części łączy `UNION ALL`,
a koty bez oznaczenia wyznacza `MINUS` (`EXCEPT`). Zadanie 10 bez operatorów
zbiorowych porównuje średnie w `HAVING` z ich maksimum i minimum. Zadanie 11
rozwiązano trzema wymaganymi sposobami; samozłączenie z kotami tej samej bandy
pozwala policzyć jej średnią bez podzapytania.

Oba skrypty uruchomiono na danych z pierwszej listy w Oracle Database Free
23.26.4 oraz PostgreSQL 18.7. Wyniki zgadzają się z przykładami z dokładnością
do kolejności wierszy i powtarzanej nazwy bandy w zadaniu 12. Zapis wykonania
zawierają pliki [Oracle](results/oracle.txt) i
[PostgreSQL](results/postgres.txt); pierwszy powstaje skryptem
[`oracle-02_results.sql`](sql/oracle-02_results.sql). Przeniesienie wymagało
zamiany `TO_CHAR` na `CAST(... AS text)`, `MINUS` na `EXCEPT` i `DECODE` na
`CASE`. PostgreSQL nie zagnieżdża agregatów, więc `MAX(AVG(...))` z zadania 10
liczy się w podzapytaniu. Odpowiednikiem `PIVOT` jest `crosstab` z rozszerzenia
`tablefunc`, który wymaga jawnych typów kolumn wyniku. Cała lista sprowadza się
do świadomej obsługi `NULL` w złączeniach zewnętrznych i agregatach oraz
właściwego doboru funkcji okna przy remisach.
