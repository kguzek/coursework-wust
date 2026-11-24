# Kartkówka – zadania z poprzednich grup

Treści odtworzone z pamięci („jakoś tak”), więc przy każdym zadaniu jest zapisana przyjęta interpretacja.
Zapytania sprawdzone w PostgreSQL na danych z `lista01`; wersje Oracle różnią się tylko tam, gdzie jest to zaznaczone
(`COALESCE` działa w obu bazach, w Oracle można też użyć `NVL`).

Przydział całkowity = `przydzial_myszy + COALESCE(myszy_extra, 0)`. Bez `COALESCE` kot z `myszy_extra IS NULL` ma
przydział `NULL` i wypada z każdego porównania.

## Spis treści

- [1. Bandy z co najmniej dwoma ponadprzeciętnymi kotami](#1-bandy-z-co-najmniej-dwoma-ponadprzeciętnymi-kotami)
- [2. Poddrzewa hierarchii z sumą przydziałów > 200](#2-poddrzewa-hierarchii-z-sumą-przydziałów--200)
- [3. Koty, które jako jedyne w bandzie miały incydent z danym gatunkiem](#3-koty-które-jako-jedyne-w-bandzie-miały-incydent-z-danym-gatunkiem)
- [Schematy do zapamiętania](#schematy-do-zapamiętania)

## 1. Bandy z co najmniej dwoma ponadprzeciętnymi kotami

**Słowa kluczowe:** zadanie 1, bandy, ponadprzeciętne, ponadprzecietne, powyżej średniej, powyzej sredniej, przydział całkowity, przydzial calkowity, ta sama płeć i funkcja, plec, funkcja, co najmniej dwa, HAVING COUNT(*) >= 2, AVG, COALESCE, CZARNI RYCERZE, SZEFOSTWO

> Wypisać bandy, w których występują co najmniej dwa koty, których całkowity przydział myszy jest większy niż średni
> przydział całkowity kotów tej samej płci i funkcji.

Schemat: **podzapytanie skorelowane** (średnia dla „mojej” grupy) → **GROUP BY banda** → **HAVING COUNT(\*) >= 2**.

Średnią liczymy po **wszystkich** kotach o tej płci i funkcji (z całego stada, nie tylko z bandy).

### Wariant A – podzapytanie skorelowane

**Słowa kluczowe:** podzapytanie skorelowane, correlated subquery, AVG w podzapytaniu, s.plec = k.plec, s.funkcja = k.funkcja, JOIN bandy, GROUP BY nazwa

```sql
SELECT b.nazwa, COUNT(*) AS "Ile ponadprzecietnych"
FROM kocury k
JOIN bandy b ON b.nr_bandy = k.nr_bandy
WHERE k.przydzial_myszy + COALESCE(k.myszy_extra, 0) >
      (SELECT AVG(s.przydzial_myszy + COALESCE(s.myszy_extra, 0))
       FROM kocury s
       WHERE s.plec = k.plec
         AND s.funkcja = k.funkcja)
GROUP BY b.nazwa
HAVING COUNT(*) >= 2;
```

### Wariant B – funkcja okna

**Słowa kluczowe:** funkcja okna, window function, AVG OVER, PARTITION BY plec, funkcja, podzapytanie w FROM, srednia

`AVG(...) OVER (PARTITION BY plec, funkcja)` dokleja średnią grupy do każdego wiersza bez zwijania go.
Funkcji okna nie można użyć w `WHERE`, dlatego jest zagnieżdżona w `FROM`.

```sql
SELECT b.nazwa, COUNT(*) AS "Ile ponadprzecietnych"
FROM (SELECT nr_bandy,
             przydzial_myszy + COALESCE(myszy_extra, 0) AS calk,
             AVG(przydzial_myszy + COALESCE(myszy_extra, 0))
                 OVER (PARTITION BY plec, funkcja) AS srednia
      FROM kocury) k
JOIN bandy b ON b.nr_bandy = k.nr_bandy
WHERE k.calk > k.srednia
GROUP BY b.nazwa
HAVING COUNT(*) >= 2;
```

Wynik na danych z listy:

| nazwa          | Ile |
| -------------- | --- |
| CZARNI RYCERZE | 4   |
| SZEFOSTWO      | 2   |

Pułapki:

- Kot, który jest jedyny w swojej grupie (np. TYGRYS – jedyny `M`/`SZEFUNIO`), ma przydział **równy** średniej, więc
  przy `>` nigdy się nie liczy.
- Jeśli treść mówi „bandy”, wypisz nazwę bandy (`JOIN bandy`), nie tylko `nr_bandy`.

## 2. Poddrzewa hierarchii z sumą przydziałów > 200

**Słowa kluczowe:** zadanie 2, drzewa, drzewo, poddrzewo, poddrzewa, hierarchia, suma > 200, suma przydziałów, suma przydzialow, co najmniej dwa koty, podwładni, podwladni, TYGRYS, LYSY, RAFA, ZOMBI 199

> Wypisać drzewa z hierarchii kotów, które mają co najmniej dwa koty i suma ich przydziałów jest większa niż 200.

Interpretacja: każdy kot jest korzeniem swojego poddrzewa (on + wszyscy podwładni, także pośredni).
„Co najmniej dwa koty” = korzeń ma przynajmniej jednego podwładnego.

Schemat: **hierarchia startująca z każdego kota** → **grupowanie po korzeniu** → **HAVING**.

### Oracle – CONNECT BY bez START WITH

**Słowa kluczowe:** CONNECT BY, bez START WITH, brak START WITH, CONNECT_BY_ROOT, PRIOR pseudo = szef, GROUP BY korzen, HAVING SUM, Oracle

Bez `START WITH` każdy wiersz zostaje korzeniem, a `CONNECT_BY_ROOT` mówi, z którego drzewa pochodzi wiersz.

```sql
SELECT korzen, COUNT(*) AS "Ile kotow", SUM(przydzial_myszy) AS "Suma"
FROM (SELECT CONNECT_BY_ROOT pseudo AS korzen, przydzial_myszy
      FROM kocury
      CONNECT BY PRIOR pseudo = szef)
GROUP BY korzen
HAVING COUNT(*) >= 2
   AND SUM(przydzial_myszy) > 200
ORDER BY 3 DESC;
```

### Rekurencyjne WITH (PostgreSQL i Oracle)

**Słowa kluczowe:** WITH RECURSIVE, rekurencyjne WITH, recursive CTE, kotwica, UNION ALL, korzen, Postgres, PostgreSQL

W Postgresie `WITH RECURSIVE`, w Oracle samo `WITH` (lista kolumn jest wymagana).

```sql
WITH RECURSIVE drzewo (korzen, pseudo, przydzial) AS (
    SELECT pseudo, pseudo, przydzial_myszy
    FROM kocury                               -- każdy kot jest korzeniem
    UNION ALL
    SELECT d.korzen, k.pseudo, k.przydzial_myszy
    FROM kocury k
    JOIN drzewo d ON k.szef = d.pseudo         -- schodzimy do podwładnych
)
SELECT korzen, COUNT(*) AS "Ile kotow", SUM(przydzial) AS "Suma"
FROM drzewo
GROUP BY korzen
HAVING COUNT(*) >= 2
   AND SUM(przydzial) > 200
ORDER BY 3 DESC;
```

Wynik na danych z listy (sam `przydzial_myszy`):

| korzen | Ile kotow | Suma |
| ------ | --------- | ---- |
| TYGRYS | 18        | 930  |
| LYSY   | 5         | 284  |
| RAFA   | 5         | 247  |

Z przydziałem całkowitym dochodzi ZOMBI (4 koty, 247). Bez myszy extra ZOMBI ma 199, więc jest tuż pod progiem –
dobrze sprawdzić, o który przydział chodzi w treści.

Pułapki:

- Ze `START WITH szef IS NULL` wyjdzie tylko jedno drzewo (TYGRYS), bo w stadzie jest jeden korzeń.
- Warunek „co najmniej dwa koty” to `COUNT(*) >= 2` po złączeniu, a nie `CONNECT_BY_ISLEAF = 0`.

## 3. Koty, które jako jedyne w bandzie miały incydent z danym gatunkiem

**Słowa kluczowe:** zadanie 3, jedyny, jako jedyny, jedyne, żaden inny, zaden inny, incydent, incydenty, gatunek, gatunek wroga, wrogowie, wrogowie_kocurow, banda, trzy tabele, złączenie, zlaczenie

> Wypisać koty, które jako jedyne ze swojej bandy miały incydent z danym gatunkiem wroga.

Gatunek siedzi w `wrogowie`, incydent w `wrogowie_kocurow`, banda w `kocury` – potrzebne złączenie trzech tabel.

### Wariant A – NOT EXISTS

**Słowa kluczowe:** NOT EXISTS, k2.pseudo <> k.pseudo, inny kot, DISTINCT, ta sama banda, ten sam gatunek

„Jako jedyny” = **nie istnieje inny kot** z tej samej bandy z incydentem z tym samym gatunkiem.

```sql
SELECT DISTINCT k.pseudo, k.nr_bandy, w.gatunek
FROM kocury k
JOIN wrogowie_kocurow wk ON wk.pseudo = k.pseudo
JOIN wrogowie w ON w.imie_wroga = wk.imie_wroga
WHERE NOT EXISTS (
    SELECT 1
    FROM kocury k2
    JOIN wrogowie_kocurow wk2 ON wk2.pseudo = k2.pseudo
    JOIN wrogowie w2 ON w2.imie_wroga = wk2.imie_wroga
    WHERE k2.nr_bandy = k.nr_bandy
      AND w2.gatunek = w.gatunek
      AND k2.pseudo <> k.pseudo
)
ORDER BY 2, 3;
```

`DISTINCT` jest potrzebne, bo kot może mieć dwa incydenty z różnymi wrogami tego samego gatunku.

### Wariant B – GROUP BY + HAVING

**Słowa kluczowe:** GROUP BY nr_bandy gatunek, HAVING COUNT(DISTINCT) = 1, COUNT(DISTINCT pseudo), MIN(pseudo), jeden kot w grupie

Grupujemy po (banda, gatunek) i zostawiamy grupy z jednym kotem; skoro kot jest jeden, `MIN(pseudo)` to on.

```sql
SELECT MIN(k.pseudo) AS pseudo, k.nr_bandy, w.gatunek
FROM kocury k
JOIN wrogowie_kocurow wk ON wk.pseudo = k.pseudo
JOIN wrogowie w ON w.imie_wroga = wk.imie_wroga
GROUP BY k.nr_bandy, w.gatunek
HAVING COUNT(DISTINCT k.pseudo) = 1
ORDER BY 2, 3;
```

Wynik na danych z listy:

| pseudo   | nr_bandy | gatunek  |
| -------- | -------- | -------- |
| MALA     | 1        | LIS      |
| PLACEK   | 2        | KOGUT    |
| ZOMBI    | 3        | CZLOWIEK |
| KURKA    | 3        | PIES     |
| PUSZYSTA | 3        | SOSNA    |
| MALY     | 4        | LIS      |
| MAN      | 4        | PIES     |

Pułapki:

- `COUNT(*) = 1` zamiast `COUNT(DISTINCT pseudo) = 1` odrzuci kota, który ma dwa incydenty z tym samym gatunkiem.
- W wariancie B `pseudo` nie jest w `GROUP BY`, więc musi być w agregacie – dlatego `MIN(pseudo)`, a nie samo `pseudo`.

## Schematy do zapamiętania

**Słowa kluczowe:** schematy, ściąga, sciaga, wzorce, większy niż średnia, co najmniej N, drzewa, jako jedyny, przydział całkowity

| Treść zadania                                     | Konstrukcja                                                   |
| ------------------------------------------------- | ------------------------------------------------------------- |
| „większy niż średnia dla tej samej X”             | podzapytanie skorelowane `WHERE s.x = k.x` albo `AVG() OVER (PARTITION BY x)` |
| „bandy, w których co najmniej N kotów …”          | filtr w `WHERE`, potem `GROUP BY banda HAVING COUNT(*) >= N`  |
| „drzewa / poddrzewa hierarchii”                   | `CONNECT BY` bez `START WITH` + `CONNECT_BY_ROOT`, albo rekurencyjne `WITH` od każdego kota |
| „jako jedyny / żaden inny”                        | `NOT EXISTS (… AND inny.pk <> ja.pk)` albo `HAVING COUNT(DISTINCT …) = 1` |
| „przydział całkowity”                             | `przydzial_myszy + COALESCE(myszy_extra, 0)`                  |
