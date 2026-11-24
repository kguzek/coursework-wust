# PBD – master notatka (SQL na kartkówkę)

Wszystko w jednym miejscu, od podstaw do drzew. Przykłady i wyniki pochodzą z danych z `lista01`
(`kocury`, `bandy`, `funkcje`, `wrogowie`, `wrogowie_kocurow`).

Pozostałe notatki:

- [kartkowka.md](kartkowka.md) – rozwiązane zadania z kartkówki,
- [wzorce-zadan.md](wzorce-zadan.md) – katalog typów zadań z gotowymi zapytaniami,
- [oracle.md](oracle.md), [postgres.md](postgres.md), [mssql.md](mssql.md) – dokumentacja składni.

## Spis treści

- [1. Kolejność wykonania zapytania](#1-kolejność-wykonania-zapytania)
- [2. JOIN](#2-join)
- [3. Grupy: GROUP BY, agregaty, HAVING](#3-grupy-group-by-agregaty-having)
- [4. COUNT(\*) a COUNT(kolumna)](#4-count-a-countkolumna)
- [5. NULL](#5-null)
- [6. Podzapytania i operator >](#6-podzapytania-i-operator-)
- [7. EXISTS / NOT EXISTS](#7-exists--not-exists)
- [8. Funkcje okna (OVER)](#8-funkcje-okna-over)
- [9. Drzewa – zapytania hierarchiczne](#9-drzewa--zapytania-hierarchiczne)
- [10. Typy zadań → konstrukcja](#10-typy-zadań--konstrukcja)
- [11. Zadania z kartkówki](#11-zadania-z-kartkówki)
- [12. Checklista przed oddaniem](#12-checklista-przed-oddaniem)
- [13. Ćwiczenia](#13-ćwiczenia)

---

## 1. Kolejność wykonania zapytania

Piszemy `SELECT … FROM … WHERE …`, ale baza wykonuje to w innej kolejności:

```
FROM / JOIN  →  WHERE  →  GROUP BY  →  HAVING  →  SELECT  →  ORDER BY
```

Wynikają z tego trzy zasady:

- **`WHERE` nie widzi agregatów** (`COUNT`, `AVG`…), bo grup jeszcze nie ma. Warunki na grupy idą do `HAVING`.
- **Aliasu z `SELECT` nie użyjesz w `WHERE`**, bo `SELECT` wykonuje się później. W `ORDER BY` już tak.
- **Funkcje okna (`OVER`) liczą się w `SELECT`**, więc filtrowanie po nich wymaga podzapytania w `FROM`.

W zapytaniu hierarchicznym (Oracle) dochodzi jeden krok:
`FROM → START WITH / CONNECT BY → WHERE → GROUP BY → HAVING → SELECT → ORDER BY`.

---

## 2. JOIN

`JOIN` dokleja do wiersza z lewej tabeli **każdy** pasujący wiersz z prawej.

```sql
SELECT k.pseudo, b.nazwa
FROM kocury k
JOIN bandy b ON b.nr_bandy = k.nr_bandy;
```

| Rodzaj | Co zostaje |
|---|---|
| `JOIN` (`INNER`) | tylko pary, które pasują |
| `LEFT JOIN` | wszystko z lewej; brak pary → `NULL` po prawej |
| `FULL JOIN` | wszystko z obu stron |
| `CROSS JOIN` | każdy z każdym |

**Self join** to tabela złączona sama ze sobą, zawsze z dwoma aliasami:

```sql
FROM kocury k
JOIN kocury s  ON s.pseudo  = k.szef      -- s = szef kota k
JOIN kocury ss ON ss.pseudo = s.szef      -- ss = szef szefa
```

**Złączenie mnoży wiersze.** Kot z dwoma incydentami występuje po `JOIN wrogowie_kocurow` dwa razy:

```sql
SELECT k.nr_bandy, SUM(k.przydzial_myszy)
FROM kocury k LEFT JOIN wrogowie_kocurow wk ON wk.pseudo = k.pseudo
GROUP BY k.nr_bandy;
-- banda 1: 353, a prawdziwa suma to 200
```

Rozwiązania: `COUNT(DISTINCT …)`, `EXISTS` zamiast złączenia albo agregacja w podzapytaniu przed złączeniem.

**`LEFT JOIN` + warunek w `WHERE` na prawej tabeli zamienia złączenie w `INNER`**, bo `NULL`-e nie przechodzą
warunku. Taki warunek należy umieścić w `ON`.

---

## 3. Grupy: GROUP BY, agregaty, HAVING

**Grupa** to zbiór wierszy o tej samej wartości w kolumnie z `GROUP BY` – „worek”, z którego robi się **jeden**
wiersz wyniku.

```
pseudo    nr_bandy  przydzial            GROUP BY nr_bandy:
TYGRYS    1         103                  worek 1: TYGRYS 103, BOLEK 50, MALA 22, LOLA 25
BOLEK     1         50                   worek 2: LYSY 72, PLACEK 67, SZYBKA 65, RURA 56, LASKA 24
MALA      1         22                   worek 3: ZOMBI 75, KURKA 61, ZERO 43, PUSZYSTA 20
...                                      worek 4: RAFA 65, MAN 51, DAMA 51, MALY 40, UCHO 40
```

```sql
SELECT nr_bandy, COUNT(*), SUM(przydzial_myszy), AVG(przydzial_myszy), MAX(przydzial_myszy)
FROM kocury
GROUP BY nr_bandy;
```

```
nr_bandy  count  sum  avg    max
1         4      200  50     103
2         5      284  56.8   72
3         4      199  49.75  75
4         5      247  49.4   65
```

**Zasada:** w `SELECT` przy `GROUP BY` może być tylko kolumna z `GROUP BY` albo agregat.
`SELECT nr_bandy, pseudo … GROUP BY nr_bandy` to błąd, bo w worku jest kilka wartości `pseudo`.
Sztuczka: gdy wiesz, że w worku jest jeden kot, `MIN(pseudo)` zwraca właśnie jego.

**Kilka kolumn:** `GROUP BY plec, funkcja` tworzy worek dla każdej **kombinacji** wartości, np. (M, LOWCZY), (D, LOWCZY).

**WHERE a HAVING:**

```sql
SELECT nr_bandy, COUNT(*)
FROM kocury
WHERE plec = 'D'          -- filtr wierszy, PRZED workami
GROUP BY nr_bandy
HAVING COUNT(*) >= 2;     -- filtr całych worków, PO grupowaniu
```

| Chcesz… | Użyj |
|---|---|
| jeden wiersz na grupę | `GROUP BY` + agregaty |
| odfiltrować całe grupy | `HAVING` |
| porównać każdy wiersz z jego grupą | `OVER (PARTITION BY …)` albo podzapytanie skorelowane |

Agregaty: `COUNT`, `SUM`, `AVG`, `MIN`, `MAX` (wszystkie oprócz `COUNT(*)` pomijają `NULL`), w Oracle także
`LISTAGG(kolumna, ', ') WITHIN GROUP (ORDER BY …)`.

---

## 4. COUNT(\*) a COUNT(kolumna)

`*` w `COUNT(*)` to specjalny zapis oznaczający „policz wiersze” – nie jest ogólnym operatorem
i działa tylko z `COUNT` (`SUM(*)` to błąd).

| Zapis | Co liczy | Na danych |
|---|---|---|
| `COUNT(*)` | wszystkie wiersze | 18 |
| `COUNT(myszy_extra)` | wiersze, w których kolumna nie jest `NULL` | 7 |
| `COUNT(szef)` | jw. (TYGRYS ma `NULL`) | 17 |
| `COUNT(DISTINCT nr_bandy)` | różne wartości różne od `NULL` | 4 |
| `COUNT(1)` | to samo co `COUNT(*)` | 18 |

Kiedy to ma znaczenie:

```sql
-- po LEFT JOIN licz kolumnę z prawej tabeli, nie *
SELECT k.pseudo, COUNT(*) AS zle, COUNT(wk.imie_wroga) AS dobrze
FROM kocury k LEFT JOIN wrogowie_kocurow wk ON wk.pseudo = k.pseudo
GROUP BY k.pseudo;
-- LOLA (bez wrogów): zle = 1, dobrze = 0

-- zliczanie warunkowe: CASE bez ELSE daje NULL, którego COUNT nie liczy
COUNT(CASE WHEN plec = 'D' THEN 1 END)

-- żaden / każdy w grupie ma wartość
HAVING COUNT(myszy_extra) = 0
HAVING COUNT(myszy_extra) = COUNT(*)
```

`COUNT` nigdy nie zwraca `NULL` (pusty zbiór → 0). `SUM`, `AVG`, `MIN` i `MAX` na pustym zbiorze zwracają `NULL`.

---

## 5. NULL

`NULL` oznacza „brak wartości”, a każde porównanie z nim daje **UNKNOWN**, które `WHERE` traktuje jak fałsz.

| Wyrażenie | Wynik |
|---|---|
| `50 + NULL` | `NULL` |
| `x = NULL`, `x <> NULL`, `x > NULL` | UNKNOWN – **nigdy nie przechodzi** |
| `x IS NULL` / `x IS NOT NULL` | poprawny sposób sprawdzania |
| `COALESCE(x, 0)` / `NVL(x, 0)` (Oracle) | `x` albo `0`, gdy `x` jest `NULL` |

**Przydział całkowity** zapisuj zawsze jako `przydzial_myszy + COALESCE(myszy_extra, 0)`.

Pułapki:

- `szef <> 'TYGRYS'` pomija TYGRYSA, bo ma `szef IS NULL`,
- `x NOT IN (SELECT szef FROM kocury)` zwraca **pusty wynik**, bo lista zawiera `NULL`. Używaj `NOT EXISTS`,
- w Oracle pusty napis `''` to `NULL`.

---

## 6. Podzapytania i operator >

### Podzapytanie skalarne

Przy `>`, `<`, `=`, `>=`, `<=`, `<>` podzapytanie musi zwrócić **dokładnie jedną wartość** (jeden wiersz,
jedna kolumna).

**Nieskorelowane** liczy się raz, a jego wynik wstawia się jak liczbę:

```sql
SELECT pseudo FROM kocury
WHERE przydzial_myszy > (SELECT AVG(przydzial_myszy) FROM kocury);   -- > 51.67
-- TYGRYS, ZOMBI, LYSY, PLACEK, SZYBKA, RAFA, KURKA, RURA
```

**Skorelowane** odwołuje się do wiersza zapytania zewnętrznego, więc liczy się **dla każdego wiersza osobno**:

```sql
SELECT k.pseudo FROM kocury k
WHERE k.przydzial_myszy > (SELECT AVG(s.przydzial_myszy)
                           FROM kocury s
                           WHERE s.nr_bandy = k.nr_bandy);    -- średnia MOJEJ bandy
```

| kot `k` | banda | podzapytanie | warunek | |
|---|---|---|---|---|
| TYGRYS | 1 | 50 | 103 > 50 | ✅ |
| BOLEK | 1 | 50 | 50 > 50 | ❌ |
| LYSY | 2 | 56.8 | 72 > 56.8 | ✅ |

Czytaj: „dla tego kota `k` policz … kotów `s`, które mają to samo co `k`”.
Dodatkowy warunek `AND s.pseudo <> k.pseudo` wyklucza samego kota z jego grupy.

### Gdy podzapytanie nie zwraca jednej wartości

- **Więcej wierszy** kończy się błędem (`ORA-01427: single-row subquery returns more than one row`).
  Pomaga agregat albo `ANY` / `ALL`.
- **Zero wierszy** daje `NULL`, a porównanie z nim UNKNOWN. Wynik jest pusty, bez błędu.

### ANY / ALL – porównanie z listą

```sql
WHERE przydzial_myszy > ALL (SELECT przydzial_myszy FROM kocury WHERE nr_bandy = 4)  -- > 65
WHERE przydzial_myszy > ANY (SELECT przydzial_myszy FROM kocury WHERE nr_bandy = 4)  -- > 40
```

| Zapis | Odpowiada |
|---|---|
| `> ALL` | `> MAX` |
| `< ALL` | `< MIN` |
| `> ANY` | `> MIN` |
| `< ANY` | `< MAX` |
| `= ANY` | `IN` |
| `<> ALL` | `NOT IN` |

- `> ALL (pusta lista)` daje **TRUE** dla wszystkich, a `> ANY (pusta lista)` daje **FALSE**,
- `NULL` na liście sprawia, że `ALL` nigdy nie daje TRUE (jak `NOT IN`).

### Podzapytanie w HAVING

```sql
-- bandy ze średnią wyższą niż średnia stada
HAVING AVG(przydzial_myszy) > (SELECT AVG(przydzial_myszy) FROM kocury)        -- banda 2

-- banda z największą średnią (>=, bo banda porównuje się też ze sobą)
HAVING AVG(przydzial_myszy) >= ALL (SELECT AVG(przydzial_myszy) FROM kocury GROUP BY nr_bandy)
```

### Inne miejsca

- podzapytanie skalarne w `SELECT`: `przydzial_myszy - (SELECT AVG(…) FROM kocury)`,
- podzapytanie w `FROM` to tabela pomocnicza (musi mieć alias),
- `WITH nazwa AS (…)` to to samo, tylko nazwane i czytelniejsze.

---

## 7. EXISTS / NOT EXISTS

`EXISTS (podzapytanie)` daje TRUE, jeśli podzapytanie zwraca **jakikolwiek** wiersz. Kolumny nie mają
znaczenia, dlatego pisze się `SELECT 1`.

```sql
-- koty bez wrogów
SELECT k.pseudo FROM kocury k
WHERE NOT EXISTS (SELECT 1 FROM wrogowie_kocurow wk WHERE wk.pseudo = k.pseudo);
-- LOLA, RAFA, ZERO

-- jedyny kot w bandzie o danej funkcji: nie istnieje INNY kot z tą samą bandą i funkcją
SELECT k.pseudo FROM kocury k
WHERE NOT EXISTS (SELECT 1 FROM kocury s
                  WHERE s.nr_bandy = k.nr_bandy
                    AND s.funkcja = k.funkcja
                    AND s.pseudo <> k.pseudo);
```

**Dzielenie relacyjne („z każdym”)** to podwójne `NOT EXISTS`: nie istnieje banda, w której nie ma incydentu
z tym gatunkiem.

```sql
SELECT DISTINCT w.gatunek FROM wrogowie w
WHERE NOT EXISTS (
    SELECT 1 FROM bandy b
    WHERE EXISTS (SELECT 1 FROM kocury k WHERE k.nr_bandy = b.nr_bandy)
      AND NOT EXISTS (
          SELECT 1 FROM kocury k
          JOIN wrogowie_kocurow wk ON wk.pseudo = k.pseudo
          JOIN wrogowie w2 ON w2.imie_wroga = wk.imie_wroga
          WHERE k.nr_bandy = b.nr_bandy AND w2.gatunek = w.gatunek));
-- CZLOWIEK, PIES

-- to samo przez zliczanie
SELECT w.gatunek
FROM kocury k
JOIN wrogowie_kocurow wk ON wk.pseudo = k.pseudo
JOIN wrogowie w ON w.imie_wroga = wk.imie_wroga
GROUP BY w.gatunek
HAVING COUNT(DISTINCT k.nr_bandy) = (SELECT COUNT(DISTINCT nr_bandy) FROM kocury);
```

---

## 8. Funkcje okna (OVER)

Działają jak `GROUP BY`, ale **nie zwijają wierszy**: każdy wiersz zostaje i dostaje wartość swojej grupy.

```sql
SELECT pseudo, nr_bandy, przydzial_myszy,
       AVG(przydzial_myszy) OVER (PARTITION BY nr_bandy)                         AS srednia_bandy,
       RANK()               OVER (PARTITION BY nr_bandy ORDER BY przydzial_myszy DESC) AS miejsce,
       SUM(przydzial_myszy) OVER ()                                              AS suma_stada
FROM kocury;
```

- `PARTITION BY x` – grupa, `OVER ()` – cała tabela,
- `ORDER BY` w `OVER` – kolejność wewnątrz grupy (ranking, suma narastająca, `LAG` / `LEAD`).

| Funkcja | Remis 2× na pierwszym miejscu |
|---|---|
| `ROW_NUMBER()` | 1, 2, 3 |
| `RANK()` | 1, 1, 3 |
| `DENSE_RANK()` | 1, 1, 2 |

Filtrowanie wymaga zagnieżdżenia:

```sql
SELECT pseudo, przydzial_myszy
FROM (SELECT pseudo, przydzial_myszy,
             DENSE_RANK() OVER (ORDER BY przydzial_myszy DESC) AS r
      FROM kocury) x
WHERE r <= 3;
-- TYGRYS 103, ZOMBI 75, LYSY 72
```

---

## 9. Drzewa – zapytania hierarchiczne

### Skąd drzewo

`kocury.szef` wskazuje na `pseudo` innego kota w **tej samej tabeli**. Kot bez szefa (TYGRYS) jest **korzeniem**.

```
TYGRYS                          poziom 1 (korzeń)
├── BOLEK                       poziom 2
├── MALA
├── LOLA
├── LYSY
│   ├── SZYBKA                  poziom 3
│   ├── LASKA
│   ├── PLACEK
│   └── RURA
├── ZOMBI
│   ├── KURKA
│   │   └── ZERO                poziom 4
│   └── PUSZYSTA
└── RAFA
    ├── UCHO
    ├── DAMA
    ├── MALY
    └── MAN
```

- **korzeń** – kot bez szefa albo kot, od którego zaczynamy,
- **liść** – kot bez podwładnych (BOLEK, ZERO, MAN…),
- **poziom** – odległość od korzenia (korzeń = 1),
- **poddrzewo X** – X ze wszystkimi podwładnymi, także pośrednimi (ZOMBI → ZOMBI, KURKA, ZERO, PUSZYSTA).

Zwykły `JOIN` sięga jeden poziom (szef), dwa `JOIN`-y sięgają dwa poziomy. Drzewo może mieć dowolną głębokość,
dlatego potrzebna jest **rekurencja**.

### Oracle: START WITH … CONNECT BY PRIOR

```sql
SELECT LEVEL, LPAD(' ', 4 * (LEVEL - 1)) || pseudo AS drzewo
FROM kocury
START WITH szef IS NULL               -- 1. od czego zaczynamy
CONNECT BY PRIOR pseudo = szef;       -- 2. jak przejść do następnego wiersza
```

1. `START WITH` wybiera wiersze startowe (TYGRYS, `LEVEL = 1`).
2. `CONNECT BY PRIOR pseudo = szef` szuka dzieci. `PRIOR` oznacza **wiersz, w którym już jestem** (rodzica),
   więc warunek czyta się „pseudo rodzica = szef dziecka”. Dzieci dostają `LEVEL = 2`.
3. Krok 2 powtarza się dla każdego dziecka, aż zabraknie dzieci. Wynik przychodzi w kolejności przeszukiwania
   w głąb.

**Kierunek zależy od położenia `PRIOR`:**

| Zapis | Znaczenie | Kierunek |
|---|---|---|
| `PRIOR pseudo = szef` | moje pseudo jest szefem następnego kota | **w dół** (podwładni) |
| `PRIOR szef = pseudo` | mój szef jest następnym kotem | **w górę** (przełożeni) |

```sql
SELECT pseudo, LEVEL FROM kocury
START WITH pseudo = 'ZERO'
CONNECT BY PRIOR szef = pseudo;
-- ZERO 1, KURKA 2, ZOMBI 3, TYGRYS 4
```

**Pseudokolumny i funkcje:**

| Co | Co zwraca |
|---|---|
| `LEVEL` | poziom wiersza |
| `CONNECT_BY_ROOT pseudo` | pseudo korzenia, z którego wyszła ścieżka |
| `SYS_CONNECT_BY_PATH(pseudo, '/')` | ścieżka jako tekst: `/TYGRYS/ZOMBI/KURKA/ZERO` |
| `CONNECT_BY_ISLEAF` | 1, jeśli wiersz jest liściem |
| `ORDER SIBLINGS BY imie` | sortuje rodzeństwo, zachowując kształt drzewa |

**WHERE a warunek w CONNECT BY:**

```sql
-- WHERE: przechodzi całe drzewo, potem ukrywa pojedyncze wiersze
-- (kotki znikają, ale ZERO pod KURKĄ zostaje)
START WITH szef IS NULL CONNECT BY PRIOR pseudo = szef
WHERE plec = 'M'

-- CONNECT BY: nie wchodzi do kotek, więc odcina całe gałęzie (KURKA i ZERO znikają)
START WITH szef IS NULL CONNECT BY PRIOR pseudo = szef AND plec = 'M'
```

### Najważniejszy trik: brak START WITH

Bez `START WITH` **każdy wiersz jest korzeniem**, więc powstaje osobne drzewo dla każdego kota.
`CONNECT_BY_ROOT` mówi, do którego drzewa należy wiersz:

```
korzen   pseudo
ZOMBI    ZOMBI
ZOMBI    KURKA
ZOMBI    ZERO
ZOMBI    PUSZYSTA
KURKA    KURKA
KURKA    ZERO
ZERO     ZERO        ← liść to drzewo z jednym kotem
```

Po `GROUP BY korzen` można policzyć dowolny agregat dla każdego poddrzewa:

```sql
SELECT korzen,
       COUNT(*) - 1   AS podwladni,
       SUM(przydzial) AS suma,
       MAX(poziom)    AS glebokosc
FROM (SELECT CONNECT_BY_ROOT pseudo AS korzen,
             przydzial_myszy      AS przydzial,
             LEVEL - 1            AS poziom
      FROM kocury
      CONNECT BY PRIOR pseudo = szef)
GROUP BY korzen
HAVING COUNT(*) > 1;
```

### Standard SQL: rekurencyjne WITH (PostgreSQL i Oracle)

```sql
WITH RECURSIVE drzewo (pseudo, poziom) AS (   -- Oracle: bez słowa RECURSIVE
    SELECT pseudo, 1 FROM kocury WHERE szef IS NULL         -- (1) kotwica = START WITH
    UNION ALL
    SELECT k.pseudo, d.poziom + 1                           -- (2) krok = CONNECT BY
    FROM kocury k
    JOIN drzewo d ON k.szef = d.pseudo
)
SELECT * FROM drzewo;
```

Wykonanie w rundach:

| Runda | Co robi | Nowe wiersze |
|---|---|---|
| 0 | kotwica | TYGRYS |
| 1 | koty z szefem z rundy 0 | BOLEK, MALA, LOLA, LYSY, ZOMBI, RAFA |
| 2 | koty z szefem z rundy 1 | SZYBKA, LASKA, PLACEK, RURA, KURKA, PUSZYSTA, UCHO, DAMA, MALY, MAN |
| 3 | koty z szefem z rundy 2 | ZERO |
| 4 | brak nowych wierszy | koniec |

| Oracle | Rekurencyjne WITH |
|---|---|
| `LEVEL` | kolumna `poziom`, zwiększana o 1 |
| `CONNECT_BY_ROOT` | kolumna `korzen`, przepisywana z rodzica |
| `SYS_CONNECT_BY_PATH` | kolumna `sciezka`: `d.sciezka \|\| '/' \|\| k.pseudo` |
| `PRIOR szef = pseudo` (w górę) | `JOIN drzewo d ON k.pseudo = d.szef` |
| brak `START WITH` | kotwica bez `WHERE` |

```sql
-- każdy kot jest korzeniem
WITH RECURSIVE d (korzen, pseudo, poziom) AS (
    SELECT pseudo, pseudo, 0 FROM kocury
    UNION ALL
    SELECT d.korzen, k.pseudo, d.poziom + 1
    FROM kocury k JOIN d ON k.szef = d.pseudo
)
SELECT korzen,
       COUNT(CASE WHEN poziom = 1 THEN 1 END) AS bezposredni,
       COUNT(*) - 1                           AS wszyscy,
       MAX(poziom)                            AS glebokosc
FROM d
GROUP BY korzen
HAVING COUNT(*) > 1;
-- TYGRYS 6/17/3, LYSY 4/4/1, RAFA 4/4/1, ZOMBI 2/3/2, KURKA 1/1/1
```

### Rozpoznawanie zadań na drzewo

| Treść | Rozwiązanie |
|---|---|
| „wszyscy podwładni X”, „pod X” | `START WITH pseudo = X`, w dół |
| „przełożeni X”, „ścieżka do szefa” | `START WITH pseudo = X`, w górę |
| „dla każdego kota liczba / suma podwładnych”, „drzewa, które…” | **bez START WITH** + `GROUP BY CONNECT_BY_ROOT` |
| „koty na poziomie N” | `WHERE LEVEL = N` |
| „koty bez podwładnych” | `CONNECT_BY_ISLEAF = 1` / `NOT EXISTS (… s.szef = k.pseudo)` |
| „bezpośredni szef / podwładni” | wystarczy self join, bez drzewa |
| „hierarchia bez kotek i ich podwładnych” | warunek w `CONNECT BY`, nie w `WHERE` |

---

## 10. Typy zadań → konstrukcja

### Procedura

1. **Co jest wierszem wyniku?** Koty, bandy, gatunki, pary, drzewa? To wyznacza `SELECT` i `GROUP BY`.
2. **Na jakim poziomie jest warunek?** Pojedynczy kot → `WHERE`. Grupa → `HAVING`.
   Porównanie z innymi → podzapytanie skorelowane, `EXISTS` albo `OVER`.
3. **Skąd dane?** Gatunek → `wrogowie`, incydent → `wrogowie_kocurow`, nazwa bandy → `bandy`,
   limity → `funkcje`.
4. **Rozbij na kroki** w `WITH` albo w podzapytaniu w `FROM`.
5. **Przejdź [checklistę](#12-checklista-przed-oddaniem).**

### Słownik

| W treści | Konstrukcja |
|---|---|
| „większy niż średnia dla tej samej X” | podzapytanie skorelowane `WHERE s.x = k.x` / `AVG() OVER (PARTITION BY x)` |
| „większy niż średnia w stadzie” | `(SELECT AVG(…) FROM kocury)` / `AVG() OVER ()` |
| „bandy, w których co najmniej N kotów …” | `WHERE …` + `GROUP BY` + `HAVING COUNT(*) >= N` |
| „bandy, w których wszystkie koty …” | `HAVING COUNT(*) = COUNT(CASE WHEN … THEN 1 END)` / `MIN` / `MAX` |
| „bandy, w których żaden kot …” | `HAVING COUNT(CASE WHEN … THEN 1 END) = 0` / `NOT EXISTS` |
| „jako jedyny”, „żaden inny” | `NOT EXISTS (… AND s.pseudo <> k.pseudo)` / `HAVING COUNT(DISTINCT …) = 1` |
| „nie mające”, „bez” | `NOT EXISTS` / `LEFT JOIN … WHERE prawa.pk IS NULL` |
| „z każdym”, „ze wszystkimi” | podwójne `NOT EXISTS` / `COUNT(DISTINCT) = (SELECT COUNT …)` |
| „najwięcej w każdej bandzie” | `= (SELECT MAX(…) … WHERE s.nr_bandy = k.nr_bandy)` / `RANK() OVER (PARTITION BY …)` |
| „N największych” | `DENSE_RANK() <= N` / `(SELECT COUNT(DISTINCT większych)) < N` |
| „banda z największą średnią / sumą” | `HAVING AVG(…) >= ALL (SELECT AVG(…) … GROUP BY …)` |
| „niż jego szef” | `JOIN kocury s ON s.pseudo = k.szef` |
| „podwładni”, „drzewo”, „poddrzewo” | `CONNECT BY PRIOR pseudo = szef` / rekurencyjne `WITH` w dół |
| „przełożeni”, „ścieżka do szefa” | `CONNECT BY PRIOR szef = pseudo` / rekurencyjne `WITH` w górę |
| „pary kotów” | self join z `a.pseudo < b.pseudo` |
| „dla każdej bandy liczba X i Y” | `COUNT(CASE …)`, `SUM(CASE … ELSE 0 END)` / `PIVOT` (Oracle) |
| „przydział całkowity” | `przydzial_myszy + COALESCE(myszy_extra, 0)` |

### Maksimum w grupie

```sql
SELECT k.nr_bandy, k.pseudo, k.przydzial_myszy
FROM kocury k
WHERE k.przydzial_myszy = (SELECT MAX(s.przydzial_myszy)
                           FROM kocury s
                           WHERE s.nr_bandy = k.nr_bandy);
-- 1 TYGRYS, 2 LYSY, 3 ZOMBI, 4 RAFA
```

`GROUP BY nr_bandy` z `MAX` nie wystarczy, bo nie wypisze `pseudo`. Przy remisie zapytanie zwraca wszystkich
remisujących.

### Pary

```sql
SELECT a.pseudo, b.pseudo
FROM kocury a
JOIN kocury b ON a.nr_bandy = b.nr_bandy AND a.pseudo < b.pseudo   -- każda para raz
WHERE ABS(a.przydzial_myszy - b.przydzial_myszy) <= 5;
```

### Pivot przez CASE

```sql
SELECT nr_bandy,
       COUNT(CASE WHEN plec = 'M' THEN 1 END)                    AS kocury,
       COUNT(CASE WHEN plec = 'D' THEN 1 END)                    AS kotki,
       SUM(CASE WHEN plec = 'D' THEN przydzial_myszy ELSE 0 END) AS myszy_kotek
FROM kocury
GROUP BY nr_bandy;
```

---

## 11. Zadania z kartkówki

Pełne opisy i wyniki są w [kartkowka.md](kartkowka.md).

**1. Bandy z co najmniej dwoma kotami, których przydział całkowity przekracza średnią dla tej samej płci i funkcji.**

```sql
SELECT b.nazwa, COUNT(*)
FROM kocury k
JOIN bandy b ON b.nr_bandy = k.nr_bandy
WHERE k.przydzial_myszy + COALESCE(k.myszy_extra, 0) >
      (SELECT AVG(s.przydzial_myszy + COALESCE(s.myszy_extra, 0))
       FROM kocury s
       WHERE s.plec = k.plec AND s.funkcja = k.funkcja)
GROUP BY b.nazwa
HAVING COUNT(*) >= 2;
-- CZARNI RYCERZE 4, SZEFOSTWO 2
```

**2. Drzewa hierarchii z co najmniej dwoma kotami i sumą przydziałów > 200.**

```sql
SELECT korzen, COUNT(*), SUM(przydzial_myszy)
FROM (SELECT CONNECT_BY_ROOT pseudo AS korzen, przydzial_myszy
      FROM kocury
      CONNECT BY PRIOR pseudo = szef)
GROUP BY korzen
HAVING COUNT(*) >= 2 AND SUM(przydzial_myszy) > 200;
-- TYGRYS 18/930, LYSY 5/284, RAFA 5/247
-- z przydziałem całkowitym dochodzi ZOMBI (bez myszy extra ma 199)
```

**3. Koty, które jako jedyne w swojej bandzie miały incydent z danym gatunkiem wroga.**

```sql
SELECT MIN(k.pseudo) AS pseudo, k.nr_bandy, w.gatunek
FROM kocury k
JOIN wrogowie_kocurow wk ON wk.pseudo = k.pseudo
JOIN wrogowie w ON w.imie_wroga = wk.imie_wroga
GROUP BY k.nr_bandy, w.gatunek
HAVING COUNT(DISTINCT k.pseudo) = 1;
-- MALA/1/LIS, PLACEK/2/KOGUT, ZOMBI/3/CZLOWIEK, KURKA/3/PIES,
-- PUSZYSTA/3/SOSNA, MALY/4/LIS, MAN/4/PIES
```

---

## 12. Checklista przed oddaniem

- [ ] **NULL w arytmetyce:** `myszy_extra` owinięte w `COALESCE` / `NVL`?
- [ ] **NULL w porównaniu:** czy `<>`, `NOT IN` albo `> ALL` nie gubi wierszy z `NULL`?
- [ ] **Złączenie mnoży wiersze:** czy `SUM` / `COUNT` nie są zawyżone? Może `COUNT(DISTINCT)` albo `EXISTS`?
- [ ] **`COUNT(*)` po `LEFT JOIN`:** czy nie powinno być `COUNT(prawa.kolumna)`?
- [ ] **`>` czy `>=`:** „większy niż” to `>`. Kot sam w grupie jest równy średniej.
- [ ] **Remisy:** czy przy „najwięcej” i „top N” pojawią się wszyscy remisujący?
- [ ] **Agregat w `WHERE`:** jeśli jest, przenieś do `HAVING` albo do podzapytania.
- [ ] **`GROUP BY`:** czy każda kolumna w `SELECT` jest w `GROUP BY` albo w agregacie?
- [ ] **`LEFT JOIN` + `WHERE` na prawej tabeli:** czy warunek nie powinien być w `ON`?
- [ ] **Podzapytanie skalarne:** czy na pewno zwraca jedną wartość?
- [ ] **Średnia „swojej” grupy:** czy kot ma być w niej uwzględniony (jeśli nie, `s.pseudo <> k.pseudo`)?
- [ ] **Drzewo:** właściwy kierunek `PRIOR`? `START WITH` potrzebne czy nie? Warunek w `WHERE` czy w `CONNECT BY`?
- [ ] **Wynik:** nazwy band (`JOIN bandy`) zamiast numerów, jeśli treść mówi „bandy”?

---

## 13. Ćwiczenia

1. Wypisz wszystkich podwładnych LYSEGO z ich poziomem.
2. Dla każdego kota, który ma podwładnych, wypisz ich liczbę (wszystkich poziomów).
3. Wypisz koty, które mają większy przydział niż średnia ich bandy.
4. Wypisz bandy, w których żaden kot nie ma `myszy_extra`.
5. Wypisz koty, które mają w swojej bandzie co najmniej jednego kota z mniejszym przydziałem i innej płci.
6. Wypisz ścieżkę od każdego liścia do korzenia.

<details>
<summary>Odpowiedzi</summary>

```sql
-- 1
SELECT pseudo, LEVEL - 1 AS poziom FROM kocury
WHERE pseudo <> 'LYSY'
START WITH pseudo = 'LYSY' CONNECT BY PRIOR pseudo = szef;

-- 2
SELECT korzen, COUNT(*) - 1
FROM (SELECT CONNECT_BY_ROOT pseudo AS korzen FROM kocury CONNECT BY PRIOR pseudo = szef)
GROUP BY korzen
HAVING COUNT(*) > 1;

-- 3
SELECT k.pseudo FROM kocury k
WHERE k.przydzial_myszy > (SELECT AVG(s.przydzial_myszy) FROM kocury s
                           WHERE s.nr_bandy = k.nr_bandy);

-- 4
SELECT nr_bandy FROM kocury GROUP BY nr_bandy HAVING COUNT(myszy_extra) = 0;

-- 5
SELECT k.pseudo FROM kocury k
WHERE EXISTS (SELECT 1 FROM kocury s
              WHERE s.nr_bandy = k.nr_bandy
                AND s.plec <> k.plec
                AND s.przydzial_myszy < k.przydzial_myszy);

-- 6 (start od liści, kierunek w górę)
SELECT CONNECT_BY_ROOT pseudo AS lisc, SYS_CONNECT_BY_PATH(pseudo, ' -> ') AS sciezka
FROM kocury
WHERE szef IS NULL                                   -- zostaw tylko pełne ścieżki
START WITH pseudo NOT IN (SELECT szef FROM kocury WHERE szef IS NOT NULL)
CONNECT BY PRIOR szef = pseudo;
```

</details>
