# Lista projektowa nr 3

Zapytania korzystają ze schematu i danych z pierwszej listy, bez zmian.
[Skrypt Oracle](sql/oracle-01_queries.sql) obejmuje zadania 1–13,
a [skrypt PostgreSQL](sql/postgres-01_queries.sql) zadania 4–10.
Uwzględniono dodatkowe podpunkty i oba wymagane warianty rozwiązań.
Zadania 1–6 nie używają podzapytań; w zadaniach 11–13 wykorzystano
mechanizm drzewa, poza wymaganym wariantem 13a opartym na złączeniach.

W zadaniu 1 kot bez incydentów nie ma w tej bazie przypisanego wroga.
Warunek końcówki imienia zastosowano więc tylko do kotów z incydentami,
zachowując wynik z przykładu. W zadaniu 2 brak męskiego przełożonego
lub podwładnego też oznaczono jako brak: dochodzą wiersze dla `ZERO`
i `ZOMBI`, pominięte w przykładzie. Zadanie 4 uwzględnia także pustą
bandę z wynikiem 0, a `COUNT(DISTINCT ...)` zapobiega liczeniu incydentów
zamiast kotów. W zadaniu 3 przydział oznacza podstawowy, jak w przykładzie;
w zadaniu 8 uwzględnia również dodatek przez `COALESCE(myszy_extra, 0)`.

Najważniejszą pułapką jest `NOT IN` przy `NULL` w kolumnie `szef`:
zapytanie nie zwraca żadnego kota. `NOT EXISTS` zwraca 13 kotów, ponieważ
sprawdza brak dopasowania. Usunięcie `NULL` z podzapytania `NOT IN`
daje ten sam wynik. W zadaniu 11 filtr płci działa po zbudowaniu drzewa,
żeby nie zgubić `ZERO`, którego bezpośrednim szefem jest kotka `KURKA`.
Staż w zadaniu 12 zależy od bieżącej daty; wcięcia są zgodne z treścią
polecenia, czyli najwyższy szef ma najmniejsze, odwrotnie niż w przykładzie.

W PostgreSQL 18.6 sprawdzono zadania 1–10 na danych z pierwszej listy,
w tym zgodność obu wariantów zadania 6 i wpływ `NULL` w zadaniu 7.
Skrypt Oracle pozostaje do uruchomienia w docelowym SZBD, szczególnie
część hierarchiczna. Przeniesienie zadań 4–10 wymaga głównie zamiany
`MINUS` na `EXCEPT` i dostosowania języka nazw miesięcy. Cała lista sprowadza
się do właściwego doboru złączeń, grupowania i kierunku przechodzenia drzewa.
