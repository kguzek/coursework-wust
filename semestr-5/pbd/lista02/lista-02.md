# Lista projektowa nr 2

Zapytania korzystają z bazy przygotowanej na pierwszej liście, bez zmian
schematu i danych. [Skrypt Oracle](sql/oracle-01_queries.sql) obejmuje
zadania 1–13, w tym dodatkowe zadanie 11 dla obu wskazanych dat.
[Skrypt PostgreSQL](sql/postgres-01_queries.sql) zawiera wymagane drugie
wersje zadań 8–10. Wystarczało środowisko z poprzedniej listy - plik
`compose.yaml` nie zmienił się.

Najważniejsze pułapki to brak dodatku zapisany jako `NULL`, który
w obliczeniach zastępuje `COALESCE(..., 0)`, oraz zamiana tylko pierwszych
wystąpień liter w zadaniu 5. Początkowy przydział w zadaniu 6 wyznacza
dzielenie przez `1.1`, nie odjęcie 10%. Staż jest liczony na dzień wykonania,
więc wynik może różnić się od przykładu z 17 lipca 2024 roku. W zadaniu 11
uwzględniono, że 31 października termin październikowej wypłaty już minął.

Przeniesienie zadań 8–10 do PostgreSQL wymaga zamiany `TO_CHAR` liczby
na `CAST(... AS text)`. Pozostałe mechanizmy mają wspólny zapis.
Wszystkie zadania rozwiązano bez podzapytań i złączeń, wykorzystując
filtrowanie, funkcje SQL i grupowanie. Skryptów nie uruchomiono jeszcze
w Oracle ani PostgreSQL; pełna weryfikacja wyników pozostaje do wykonania.
