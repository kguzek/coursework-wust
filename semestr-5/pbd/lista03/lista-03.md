# Lista projektowa nr 3

Zapytania korzystają ze schematu i danych z pierwszej listy, bez zmian.
[Skrypt Oracle](sql/oracle-01_queries.sql) obejmuje zadania 1–13,
a [skrypt PostgreSQL](sql/postgres-01_queries.sql) zadania 4–10.
Uwzględniono dodatkowe podpunkty i oba wymagane warianty rozwiązań.
Zadania 1–6 nie używają podzapytań; w zadaniach 11–13 wykorzystano
mechanizm drzewa, poza wymaganym wariantem 13a opartym na złączeniach.

W zadaniu 1 kot bez incydentów nie ma wroga, więc warunek końcówki imienia
wroga dotyczy tylko kotów wcześniejszych od szefa, co odtwarza wynik
z przykładu. W zadaniu 2 płeć jest filtrowana dopiero po złączeniu, dlatego
„brak” oznacza brak jakiegokolwiek przełożonego lub podwładnego - kotki
przy `ZOMBI` i `ZERO` nie dają dodatkowych wierszy. Zadanie 4 uwzględnia
także pustą bandę z wynikiem 0, a `COUNT(DISTINCT ...)` zapobiega liczeniu
incydentów zamiast kotów. W zadaniu 3 przydział oznacza podstawowy, jak
w przykładzie; w zadaniu 8 uwzględnia również dodatek przez
`COALESCE(myszy_extra, 0)`. Kot bez bandy w zadaniu 7 jest porównywany
z innymi kotami bez bandy: w Oracle przez `DECODE`, w PostgreSQL przez
`IS NOT DISTINCT FROM`, którego Oracle nie obsługuje.

Najważniejszą pułapką jest `NOT IN` przy `NULL` w kolumnie `szef`:
zapytanie nie zwraca żadnego kota. `NOT EXISTS` zwraca 13 kotów, ponieważ
sprawdza brak dopasowania. Usunięcie `NULL` z podzapytania `NOT IN`
daje ten sam wynik. W zadaniu 11 filtr płci działa po zbudowaniu drzewa,
żeby nie zgubić `ZERO`, którego bezpośrednim szefem jest kotka `KURKA`.
W zadaniu 12 wcięcia odpowiadają przykładowi, a staż jest liczony od
bieżącej daty, więc wynik zawiera więcej kotów. Data `2024-07-17` daje
dokładnie wynik z polecenia.

Oba skrypty uruchomiono na danych z pierwszej listy w Oracle Database Free
23.26.3 oraz PostgreSQL 18.4. Wyniki zgadzają się z przykładami z dokładnością
do kolejności wierszy, pustej bandy w zadaniu 4 i daty w zadaniu 12. Zapis
wykonania zawierają pliki [Oracle](results/oracle.txt) i
[PostgreSQL](results/postgres.txt); pierwszy powstaje skryptem
[`oracle-02_results.sql`](sql/oracle-02_results.sql). Przeniesienie zadań
4–10 wymaga jedynie zamiany `MINUS` na `EXCEPT`, `DECODE` na
`IS NOT DISTINCT FROM` i usunięcia parametru języka nazw miesięcy. Cała lista
sprowadza się do właściwego doboru złączeń, grupowania i kierunku
przechodzenia drzewa.
