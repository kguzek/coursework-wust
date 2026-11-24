# Wzorce zadań SQL – jak rozwiązywać zadania typu kartkówkowego

Ogólne podejście do zadań na schemacie `kocury` / `bandy` / `funkcje` / `wrogowie` / `wrogowie_kocurow`.
Rozwiązane przykłady z kartkówki są w [kartkowka.md](kartkowka.md).

Zapytania są pisane tak, żeby działały w PostgreSQL i Oracle (`COALESCE`, `CASE`, `EXISTS`). Wyjątki są oznaczone.
Wyniki w komentarzach pochodzą z danych z `lista01`.

## Spis treści

- [0. Procedura](#0-procedura)
- [1. Porównanie z agregatem „swojej” grupy](#1-porównanie-z-agregatem-swojej-grupy)
- [2. Grupy, w których co najmniej N / wszystkie / żaden](#2-grupy-w-których-co-najmniej-n--wszystkie--żaden)
- [3. „Jedyny” / „żaden inny”](#3-jedyny--żaden-inny)
- [4. „Nie mający” – anti-join](#4-nie-mający--anti-join)
- [5. „Wszystkie” – dzielenie relacyjne](#5-wszystkie--dzielenie-relacyjne)
- [6. Maksimum w grupie / top-N](#6-maksimum-w-grupie--top-n)
- [7. Grupa z największym agregatem](#7-grupa-z-największym-agregatem)
- [8. Porównanie z szefem – self join](#8-porównanie-z-szefem--self-join)
- [9. Hierarchia](#9-hierarchia)
- [10. Pary kotów](#10-pary-kotów)
- [11. Zliczanie warunkowe / pivot](#11-zliczanie-warunkowe--pivot)
- [12. Checklista pułapek](#12-checklista-pułapek)
- [13. Słownik: treść → konstrukcja](#13-słownik-treść--konstrukcja)

## 0. Procedura

**Słowa kluczowe:** procedura, krok po kroku, jak zacząć, jak zaczac, wiersz wyniku, WHERE, HAVING, EXISTS, OVER, WITH, skąd dane, skad dane, pułapki

1. **Co jest wierszem wyniku?** Koty, bandy, gatunki, pary, drzewa? To wyznacza `SELECT` i ewentualne `GROUP BY`.
2. **Jaki warunek i na jakim poziomie?**
   - dotyczy pojedynczego kota → `WHERE`,
   - dotyczy grupy (bandy, funkcji, drzewa) → `GROUP BY … HAVING`,
   - porównuje z innymi wierszami → podzapytanie skorelowane, `EXISTS` / `NOT EXISTS` albo funkcja okna.
3. **Skąd biorą się dane?** Gatunek jest w `wrogowie`, incydent w `wrogowie_kocurow`, nazwa bandy w `bandy`,
   limity myszy w `funkcje`. Dołącz tylko potrzebne tabele.
4. **Złożone warunki rozbij na kroki** w `WITH` albo w podzapytaniu w `FROM`: najpierw policz wartość
   pomocniczą, potem filtruj.
5. **Sprawdź pułapki** z [sekcji 12](#12-checklista-pułapek): `NULL`, duplikaty po złączeniu, `>` czy `>=`, remisy.

## 1. Porównanie z agregatem „swojej” grupy

**Słowa kluczowe:** większy niż średnia, wiekszy niz srednia, ponad średnią, powyżej średniej, swoja grupa, ta sama, podzapytanie skorelowane, correlated, AVG OVER, PARTITION BY, OVER (), średnia stada, średnia innych, s.pseudo <> k.pseudo

„Kot ma więcej niż średnia / maksimum / suma dla kotów o tej samej X.”

```sql
-- podzapytanie skorelowane: dla każdego kota liczymy agregat jego grupy
SELECT k.pseudo
FROM kocury k
WHERE k.przydzial_myszy > (SELECT AVG(s.przydzial_myszy)
                           FROM kocury s
                           WHERE s.nr_bandy = k.nr_bandy);

-- funkcja okna: agregat grupy doklejony do wiersza; WHERE wymaga zagnieżdżenia
SELECT pseudo
FROM (SELECT pseudo, przydzial_myszy,
             AVG(przydzial_myszy) OVER (PARTITION BY nr_bandy) AS sr
      FROM kocury) x
WHERE przydzial_myszy > sr;
```

- „tej samej płci i funkcji” → kilka warunków w podzapytaniu albo `PARTITION BY plec, funkcja`.
- „niż średnia w stadzie” → podzapytanie nieskorelowane `(SELECT AVG(…) FROM kocury)` albo `OVER ()`.
- „niż średnia **innych** kotów z bandy” → w podzapytaniu dodaj `AND s.pseudo <> k.pseudo`.

## 2. Grupy, w których co najmniej N / wszystkie / żaden

**Słowa kluczowe:** co najmniej N, co najmniej dwa, wszystkie, wszyscy, każdy kot, kazdy kot, żaden, zaden, HAVING COUNT, COUNT(CASE), MIN, MAX, próg, prog, COUNT(DISTINCT), bandy w których

**Co najmniej N spełnia** – filtr w `WHERE`, licznik w `HAVING`:

```sql
SELECT nr_bandy
FROM kocury
WHERE plec = 'D'
GROUP BY nr_bandy
HAVING COUNT(*) >= 2;
```

**Wszyscy spełniają** – liczba spełniających równa liczbie wszystkich, albo warunek na `MIN` / `MAX`:

```sql
SELECT nr_bandy
FROM kocury
GROUP BY nr_bandy
HAVING COUNT(*) = COUNT(CASE WHEN przydzial_myszy >= 40 THEN 1 END);   -- banda 4

-- to samo prościej, gdy warunek jest progiem
SELECT nr_bandy FROM kocury GROUP BY nr_bandy HAVING MIN(przydzial_myszy) >= 40;
```

**Żaden nie spełnia** – `HAVING COUNT(CASE WHEN … THEN 1 END) = 0` albo `NOT EXISTS`.

Warunek z innej tabeli (np. „co najmniej 2 koty z incydentem”) liczymy przez `COUNT(DISTINCT k.pseudo)`, bo po
złączeniu kot z dwoma incydentami występuje dwa razy.

## 3. „Jedyny” / „żaden inny”

**Słowa kluczowe:** jedyny, jako jedyny, jedyna, żaden inny, zaden inny, NOT EXISTS, s.pseudo <> k.pseudo, HAVING COUNT(DISTINCT) = 1, MIN(pseudo), najstarszy, unikalny, unique

„Kot jako jedyny w bandzie / funkcji / … ma cechę X.” Kluczem jest warunek `inny.pk <> ja.pk`.

```sql
-- jedyny kot w swojej bandzie o danej funkcji
SELECT k.pseudo, k.nr_bandy, k.funkcja
FROM kocury k
WHERE NOT EXISTS (SELECT 1
                  FROM kocury s
                  WHERE s.nr_bandy = k.nr_bandy
                    AND s.funkcja = k.funkcja
                    AND s.pseudo <> k.pseudo);

-- alternatywa: grupy z dokładnie jednym kotem
SELECT nr_bandy, funkcja, MIN(pseudo) AS pseudo
FROM kocury
GROUP BY nr_bandy, funkcja
HAVING COUNT(DISTINCT pseudo) = 1;
```

Pochodne:

- „najstarszy w bandzie” = nie istnieje kot z bandy z wcześniejszą datą `w_stadku_od`,
- „jako jedyny ma więcej niż…” = spełnia warunek **i** `NOT EXISTS` innego, który też spełnia.

## 4. „Nie mający” – anti-join

**Słowa kluczowe:** nie mający, nie majacy, bez, brak, anti-join, antijoin, NOT EXISTS, LEFT JOIN IS NULL, NOT IN, NOT IN NULL pułapka, koty bez wrogów, bez wrogow, funkcje bez kotów

„Koty bez wrogów / funkcje, których nikt nie pełni / bandy bez kotów.”

```sql
SELECT k.pseudo
FROM kocury k
WHERE NOT EXISTS (SELECT 1 FROM wrogowie_kocurow wk WHERE wk.pseudo = k.pseudo);
-- LOLA, RAFA, ZERO

-- to samo przez LEFT JOIN
SELECT k.pseudo
FROM kocury k
LEFT JOIN wrogowie_kocurow wk ON wk.pseudo = k.pseudo
WHERE wk.pseudo IS NULL;
```

`NOT IN (podzapytanie)` zwraca **pusty wynik**, jeśli podzapytanie zawiera choć jeden `NULL`
(np. `NOT IN (SELECT szef FROM kocury)`, bo TYGRYS ma `szef = NULL`). Bezpieczniej używać `NOT EXISTS`.

## 5. „Wszystkie” – dzielenie relacyjne

**Słowa kluczowe:** wszystkie, z każdym, z kazdym, ze wszystkimi, każda banda, kazda banda, dzielenie relacyjne, relational division, podwójne NOT EXISTS, podwojne NOT EXISTS, COUNT(DISTINCT) = (SELECT COUNT), pusty zbiór, gatunki

„Gatunki, z którymi incydent miała **każda** banda.” „Koty, które walczyły ze **wszystkimi** wrogami szefa.”

Dwa sposoby:

```sql
-- (a) podwójne NOT EXISTS: nie istnieje banda, w której nie ma incydentu z tym gatunkiem
SELECT DISTINCT w.gatunek
FROM wrogowie w
WHERE NOT EXISTS (
    SELECT 1
    FROM bandy b
    WHERE EXISTS (SELECT 1 FROM kocury k WHERE k.nr_bandy = b.nr_bandy)   -- tylko bandy z kotami
      AND NOT EXISTS (
          SELECT 1
          FROM kocury k
          JOIN wrogowie_kocurow wk ON wk.pseudo = k.pseudo
          JOIN wrogowie w2 ON w2.imie_wroga = wk.imie_wroga
          WHERE k.nr_bandy = b.nr_bandy
            AND w2.gatunek = w.gatunek));
-- CZLOWIEK, PIES

-- (b) zliczanie: liczba różnych band z incydentem = liczba wszystkich band
SELECT w.gatunek
FROM kocury k
JOIN wrogowie_kocurow wk ON wk.pseudo = k.pseudo
JOIN wrogowie w ON w.imie_wroga = wk.imie_wroga
GROUP BY w.gatunek
HAVING COUNT(DISTINCT k.nr_bandy) = (SELECT COUNT(DISTINCT nr_bandy) FROM kocury);
```

Uwaga na „wszystkie” w stosunku do pustego zbioru: przy podwójnym `NOT EXISTS` warunek „ze wszystkimi wrogami szefa”
jest spełniony, gdy szef nie ma żadnych wrogów. Przy zliczaniu taki kot nie wyjdzie.

## 6. Maksimum w grupie / top-N

**Słowa kluczowe:** maksimum, max, największy, najwiekszy, najwięcej, najwiecej, w każdej bandzie, top N, top-N, N największych, trzy największe, ranking, ROW_NUMBER, RANK, DENSE_RANK, remis, remisy, ties, COUNT(DISTINCT większych)

„Kot z największym przydziałem w każdej bandzie”:

```sql
SELECT k.nr_bandy, k.pseudo, k.przydzial_myszy
FROM kocury k
WHERE k.przydzial_myszy = (SELECT MAX(s.przydzial_myszy)
                           FROM kocury s
                           WHERE s.nr_bandy = k.nr_bandy);
-- 1 TYGRYS, 2 LYSY, 3 ZOMBI, 4 RAFA
```

Przy remisie zwraca wszystkich remisujących, co zwykle jest pożądane. `GROUP BY nr_bandy` + `MAX` nie wystarczy,
bo nie da się z nim wypisać `pseudo`.

„Koty z trzema największymi (różnymi) przydziałami”:

```sql
-- bez funkcji okna: mniej niż 3 różne większe wartości
SELECT pseudo, przydzial_myszy
FROM kocury k
WHERE (SELECT COUNT(DISTINCT s.przydzial_myszy)
       FROM kocury s
       WHERE s.przydzial_myszy > k.przydzial_myszy) < 3;

-- z funkcją okna (per grupa: PARTITION BY nr_bandy)
SELECT pseudo, przydzial_myszy
FROM (SELECT pseudo, przydzial_myszy,
             DENSE_RANK() OVER (ORDER BY przydzial_myszy DESC) AS r
      FROM kocury) x
WHERE r <= 3;
-- TYGRYS 103, ZOMBI 75, LYSY 72
```

- `ROW_NUMBER` – zawsze dokładnie N wierszy, remisy ucinane losowo,
- `RANK` – remisy dostają ten sam numer, potem jest dziura (1, 1, 3),
- `DENSE_RANK` – remisy dostają ten sam numer, bez dziur (1, 1, 2); pasuje do „N największych wartości”.

## 7. Grupa z największym agregatem

**Słowa kluczowe:** banda z największą średnią, największa suma, najwieksza, >= ALL, MAX(AVG()), zagnieżdżony agregat, FETCH FIRST, WITH TIES, HAVING ALL

„Banda z największym średnim przydziałem”:

```sql
SELECT nr_bandy, AVG(przydzial_myszy)
FROM kocury
GROUP BY nr_bandy
HAVING AVG(przydzial_myszy) >= ALL (SELECT AVG(przydzial_myszy)
                                    FROM kocury
                                    GROUP BY nr_bandy);
-- banda 2
```

Inne zapisy:

- `HAVING AVG(…) = (SELECT MAX(AVG(…)) FROM kocury GROUP BY nr_bandy)` – zagnieżdżony agregat działa
  **tylko w Oracle**,
- `ORDER BY … FETCH FIRST 1 ROWS WITH TIES` – działa w Oracle i w PostgreSQL 13+.

## 8. Porównanie z szefem – self join

**Słowa kluczowe:** szef, szefem, przełożony, przelozony, self join, samozłączenie, szef szefa, dłużej w stadzie, w_stadku_od, więcej niż szef, LEFT JOIN bez szefa

„Koty, które mają więcej myszy niż ich szef / są w stadzie dłużej niż szef / są w innej bandzie niż szef.”

```sql
SELECT k.pseudo, s.pseudo AS szef
FROM kocury k
JOIN kocury s ON s.pseudo = k.szef           -- s = szef kota k
WHERE k.w_stadku_od < s.w_stadku_od;
```

- „szef szefa” → drugi self join: `JOIN kocury ss ON ss.pseudo = s.szef`,
- „również koty bez szefa” → `LEFT JOIN`, a warunek na `s` przenieś do `ON`.

## 9. Hierarchia

**Słowa kluczowe:** hierarchia, drzewo, drzewa, poddrzewo, CONNECT BY, PRIOR, START WITH, LEVEL, CONNECT_BY_ROOT, SYS_CONNECT_BY_PATH, CONNECT_BY_ISLEAF, WITH RECURSIVE, rekurencja, w dół, w górę, podwładni, przełożeni, przodkowie, głębokość, glebokosc, liście, poziom

Relacja `kocury.szef → kocury.pseudo`. Najpierw ustal kierunek: **w dół** (podwładni) czy **w górę** (przełożeni).

| Kierunek       | Oracle                          | Rekurencyjne WITH – krok rekurencyjny |
| -------------- | ------------------------------- | ------------------------------------- |
| w dół          | `CONNECT BY PRIOR pseudo = szef` | `JOIN drzewo d ON k.szef = d.pseudo`  |
| w górę         | `CONNECT BY PRIOR szef = pseudo` | `JOIN drzewo d ON k.pseudo = d.szef`  |

**Poddrzewo każdego kota** (podwładni wszystkich poziomów, liczba bezpośrednich, głębokość):

```sql
WITH RECURSIVE d (korzen, pseudo, poziom) AS (     -- Oracle: samo WITH
    SELECT pseudo, pseudo, 0 FROM kocury           -- każdy kot jest korzeniem
    UNION ALL
    SELECT d.korzen, k.pseudo, d.poziom + 1
    FROM kocury k
    JOIN d ON k.szef = d.pseudo
)
SELECT korzen,
       COUNT(CASE WHEN poziom = 1 THEN 1 END) AS bezposredni,
       COUNT(*) - 1                           AS wszyscy_podwladni,
       MAX(poziom)                            AS glebokosc
FROM d
GROUP BY korzen
HAVING COUNT(*) > 1;
-- TYGRYS 6/17/3, LYSY 4/4/1, RAFA 4/4/1, ZOMBI 2/3/2, KURKA 1/1/1
```

W Oracle to samo bez `WITH`: `CONNECT BY PRIOR pseudo = szef` **bez** `START WITH`, a następnie
`GROUP BY CONNECT_BY_ROOT pseudo`. Głębokość liczymy jako `MAX(LEVEL) - 1`.

**Przełożeni danego kota** (ścieżka w górę):

```sql
WITH RECURSIVE g (pseudo, szef, poziom) AS (
    SELECT pseudo, szef, 0 FROM kocury WHERE pseudo = 'ZERO'
    UNION ALL
    SELECT k.pseudo, k.szef, g.poziom + 1
    FROM kocury k
    JOIN g ON k.pseudo = g.szef
)
SELECT * FROM g;
-- ZERO → KURKA → ZOMBI → TYGRYS
```

Typowe pytania:

| Pytanie                                     | Oracle                                                     |
| ------------------------------------------- | ---------------------------------------------------------- |
| liście (bez podwładnych)                    | `CONNECT_BY_ISLEAF = 1` albo `NOT EXISTS (… s.szef = k.pseudo)` |
| koty na poziomie N                          | `WHERE LEVEL = N` (`WHERE` filtruje wiersze, nie ucina gałęzi) |
| odcięcie gałęzi (np. bez podwładnych kotek) | warunek w `CONNECT BY … AND plec = 'M'`                    |
| ścieżka jako tekst                          | `SYS_CONNECT_BY_PATH(pseudo, '/')`                         |
| korzeń drzewa dla wiersza                   | `CONNECT_BY_ROOT pseudo`                                   |
| suma / liczba w poddrzewie                  | brak `START WITH` + `GROUP BY CONNECT_BY_ROOT …`           |

## 10. Pary kotów

**Słowa kluczowe:** pary, para, self join, a.pseudo < b.pseudo, każda para raz, duplikaty, ABS, podobny przydział

„Pary kotów z tej samej bandy o podobnym przydziale.”

```sql
SELECT a.pseudo, b.pseudo
FROM kocury a
JOIN kocury b
  ON a.nr_bandy = b.nr_bandy
 AND a.pseudo < b.pseudo                -- każda para raz, bez (X, X)
WHERE ABS(a.przydzial_myszy - b.przydzial_myszy) <= 5;
```

`<>` zamiast `<` zwróci każdą parę dwa razy: (A, B) i (B, A).

## 11. Zliczanie warunkowe / pivot

**Słowa kluczowe:** zliczanie warunkowe, pivot, PIVOT, tabela przestawna, COUNT(CASE), SUM(CASE), ELSE 0, płeć, plec, kocury i kotki

„Dla każdej bandy liczba kocurów, kotek i suma myszy kotek.”

```sql
SELECT nr_bandy,
       COUNT(CASE WHEN plec = 'M' THEN 1 END)                     AS kocury,
       COUNT(CASE WHEN plec = 'D' THEN 1 END)                     AS kotki,
       SUM(CASE WHEN plec = 'D' THEN przydzial_myszy ELSE 0 END)  AS myszy_kotek
FROM kocury
GROUP BY nr_bandy;
```

`COUNT(CASE …)` liczy tylko wartości różne od `NULL`, więc brak `ELSE` jest celowy.
W `SUM` dajemy `ELSE 0`, żeby grupa bez pasujących wierszy dała `0`, a nie `NULL`.

## 12. Checklista pułapek

**Słowa kluczowe:** pułapki, pulapki, błędy, bledy, checklista, NULL, COALESCE, NVL, NOT IN, mnożenie wierszy, duplikaty, > czy >=, remisy, agregat w WHERE, GROUP BY, LEFT JOIN WHERE

- **NULL w arytmetyce.** `przydzial_myszy + myszy_extra` daje `NULL`, gdy `myszy_extra` jest `NULL`.
  Używaj `COALESCE(myszy_extra, 0)` (w Oracle też `NVL`).
- **NULL w porównaniach.** `szef <> 'TYGRYS'` pomija TYGRYSA, bo ma `szef IS NULL`. Do tego `NOT IN` z `NULL`
  w podzapytaniu daje pusty wynik.
- **Mnożenie wierszy przez złączenie.** `SUM(przydzial_myszy)` po `JOIN wrogowie_kocurow` liczy kota tyle razy,
  ile ma incydentów (banda 1: 353 zamiast 200). Najpierw agreguj w podzapytaniu albo użyj `EXISTS`.
  Pomaga też `COUNT(DISTINCT …)`.
- **`>` czy `>=`.** „Większy niż średnia” oznacza `>`. Kot jedyny w swojej grupie jest równy średniej grupy.
- **Remisy.** Przy „najwięcej” i „top N” sprawdź, czy remisujący mają się pojawić (`=` MAX, `DENSE_RANK`, `WITH TIES`).
- **Agregat w WHERE.** Agregatów i funkcji okna nie wolno używać w `WHERE`. Agregat idzie do `HAVING`,
  a funkcję okna zagnieżdżamy w podzapytaniu.
- **Kolumny w SELECT przy GROUP BY.** Każda kolumna musi być w `GROUP BY` albo w agregacie.
- **LEFT JOIN + WHERE.** Warunek na prawej tabeli w `WHERE` zamienia złączenie w `INNER`. Taki warunek należy do `ON`.
- **Średnia w podzapytaniu skorelowanym.** Upewnij się, czy grupa ma obejmować samego kota.
  Jeśli nie, dodaj `s.pseudo <> k.pseudo`.
- **Hierarchia.** `WHERE` przy `CONNECT BY` filtruje pojedyncze wiersze, a warunek w `CONNECT BY` ucina całe gałęzie.

## 13. Słownik: treść → konstrukcja

**Słowa kluczowe:** słownik, slownik, treść, tresc, konstrukcja, ściąga, sciaga, jak przetłumaczyć treść, wzorce

| W treści                                    | Konstrukcja                                                       |
| ------------------------------------------- | ----------------------------------------------------------------- |
| „większy niż średnia dla tej samej X”       | podzapytanie skorelowane po X / `AVG() OVER (PARTITION BY X)`     |
| „większy niż średnia w stadzie”             | `(SELECT AVG(…) FROM kocury)` / `AVG() OVER ()`                   |
| „bandy, w których co najmniej N kotów …”    | `WHERE …` + `GROUP BY` + `HAVING COUNT(*) >= N`                   |
| „bandy, w których wszystkie koty …”         | `HAVING COUNT(*) = COUNT(CASE WHEN … THEN 1 END)` / `MIN` / `MAX` |
| „jako jedyny”, „żaden inny”                 | `NOT EXISTS (… AND inny.pseudo <> k.pseudo)` / `HAVING COUNT(DISTINCT) = 1` |
| „nie mające”, „bez”                         | `NOT EXISTS` / `LEFT JOIN … IS NULL`                              |
| „z każdym”, „ze wszystkimi”                 | podwójne `NOT EXISTS` / `COUNT(DISTINCT) = (SELECT COUNT …)`      |
| „najwięcej w każdej bandzie”                | `= (SELECT MAX(…) … WHERE s.grupa = k.grupa)` / `RANK() OVER (PARTITION BY …)` |
| „N największych”                            | `DENSE_RANK() <= N` / `COUNT(DISTINCT większych) < N`             |
| „banda z największą średnią/sumą”           | `HAVING AVG(…) >= ALL (SELECT AVG(…) … GROUP BY …)`               |
| „niż jego szef”                             | self join `JOIN kocury s ON s.pseudo = k.szef`                    |
| „podwładni”, „drzewo”, „poddrzewo”          | `CONNECT BY PRIOR pseudo = szef` / rekurencyjne `WITH` w dół      |
| „przełożeni”, „ścieżka do szefa”            | `CONNECT BY PRIOR szef = pseudo` / rekurencyjne `WITH` w górę     |
| „pary”                                      | self join z `a.pk < b.pk`                                         |
| „dla każdej bandy liczba X i Y”             | `COUNT(CASE …)`, `SUM(CASE …)` / `PIVOT` (Oracle)                 |
| „przydział całkowity”                       | `przydzial_myszy + COALESCE(myszy_extra, 0)`                      |
