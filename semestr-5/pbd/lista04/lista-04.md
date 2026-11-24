# Lista projektowa nr 4

Zapytania korzystają ze schematu i danych z pierwszej listy.
[Skrypt Oracle](sql/oracle-01_queries.sql) i
[skrypt PostgreSQL](sql/postgres-01_queries.sql) obejmują zadania 1–12.
Całkowity przydział to `przydzial_myszy + COALESCE(myszy_extra, 0)`, poza
zadaniem 9: przykład odpowiada przydziałowi podstawowemu, a z dodatkiem
w wyniku pojawiłaby się `MALA`.

W zadaniu 3a zwykłe złączenie gubi funkcję `HONOROWA`, a `LEFT JOIN`
z `COUNT(*)` przypisuje jej jednego kota i sumę `NULL`. Poprawna wersja używa
`COUNT(k.pseudo)` i `COALESCE` dla sumy. W zadaniu 5 remis na drugim miejscu
(`DAMA` i `MAN`, po 51) rozstrzyga pseudonim w `ROW_NUMBER()`, co daje wynik
z przykładu. W zadaniu 6 `RANK()` pokazałby wszystkich rekordzistów przy remisie.
W zadaniu 7 rok z liczbą równą średniej trafiłby do grupy „od dołu”.

Oba skrypty uruchomiono w Oracle Database Free 23.26.4 i PostgreSQL 18.7.
Wyniki zgadzają się z przykładami z dokładnością do kolejności wierszy
([Oracle](results/oracle.txt), [PostgreSQL](results/postgres.txt)).
Przeniesienie wymagało zamiany `MINUS` na `EXCEPT` i `DECODE` na `CASE`,
obliczenia `MAX(AVG(...))` w podzapytaniu, bo PostgreSQL nie zagnieżdża
agregatów, oraz `crosstab` z `tablefunc` zamiast `PIVOT`. Głównym problemem
listy była obsługa `NULL` w złączeniach zewnętrznych i agregatach.
