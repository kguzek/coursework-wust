-- Zadanie 4
-- DISTINCT liczy koty, nie incydenty; pusta banda ma wynik 0.
SELECT b.nazwa AS "Nazwa bandy", COUNT(DISTINCT w.pseudo) AS "Koty z wrogami"
FROM bandy b
LEFT JOIN kocury k ON k.nr_bandy = b.nr_bandy
LEFT JOIN wrogowie_kocurow w ON w.pseudo = k.pseudo
GROUP BY b.nr_bandy, b.nazwa
ORDER BY b.nr_bandy;

-- Zadanie 5: wiecej niz jeden wrog
SELECT k.funkcja AS "Funkcja", k.pseudo AS "Pseudonim kota",
       COUNT(*) AS "Liczba wrogow"
FROM kocury k
JOIN wrogowie_kocurow w ON w.pseudo = k.pseudo
GROUP BY k.funkcja, k.pseudo
HAVING COUNT(*) > 1
ORDER BY k.pseudo;

-- Zadanie 5: jednoczesnie czlowiek i pies
SELECT k.funkcja AS "Funkcja", k.pseudo AS "Pseudonim kota",
       COUNT(*) AS "Liczba wrogow"
FROM kocury k
JOIN wrogowie_kocurow wk ON wk.pseudo = k.pseudo
JOIN wrogowie w ON w.imie_wroga = wk.imie_wroga
WHERE w.gatunek IN ('CZLOWIEK', 'PIES')
GROUP BY k.funkcja, k.pseudo
HAVING COUNT(DISTINCT w.gatunek) = 2
ORDER BY k.pseudo;

-- Zadanie 6a
SELECT b.nr_bandy AS "Nr bandy", b.nazwa AS "Nazwa", b.teren AS "Teren"
FROM bandy b
LEFT JOIN kocury k ON k.nr_bandy = b.nr_bandy
WHERE k.pseudo IS NULL
ORDER BY b.nr_bandy;

-- Zadanie 6b: EXCEPT zamiast Oracle'owego MINUS.
SELECT nr_bandy AS "Nr bandy", nazwa AS "Nazwa", teren AS "Teren"
FROM bandy
EXCEPT
SELECT b.nr_bandy, b.nazwa, b.teren
FROM bandy b
JOIN kocury k ON k.nr_bandy = b.nr_bandy
ORDER BY 1;

-- Zadanie 7: prominenci i szaraki; remisy na minimum zostaja.
-- IS NOT DISTINCT FROM porownuje NULL jak zwykla wartosc.
SELECT pseudo AS "Pseudonim", przydzial_myszy AS "Zjada", nr_bandy AS "Banda",
       'Prominent' AS "Typ",
       CASE WHEN przydzial_myszy > 60 THEN 'powyzej 60'
            ELSE 'ponizej 60' END AS "Ocena"
FROM kocury
WHERE przydzial_myszy > (SELECT AVG(przydzial_myszy) FROM kocury)
UNION ALL
SELECT k.pseudo, k.przydzial_myszy, k.nr_bandy, 'Szarak',
       CASE WHEN k.przydzial_myszy > 60 THEN 'powyzej 60'
            ELSE 'ponizej 60' END
FROM kocury k
WHERE k.przydzial_myszy IS NOT NULL
  AND NOT EXISTS (
    SELECT 1 FROM kocury m
    WHERE m.nr_bandy IS NOT DISTINCT FROM k.nr_bandy
      AND m.przydzial_myszy < k.przydzial_myszy
  )
ORDER BY 4, 3, 2 DESC, 1;

-- Zadanie 7: NOT IN z NULL w kolumnie szef nie zwraca zadnego kota.
SELECT pseudo AS "Nie sa niczyim szefem"
FROM kocury
WHERE pseudo NOT IN (SELECT szef FROM kocury)
ORDER BY pseudo;

-- NOT EXISTS sprawdza tylko dopasowania, wiec NULL mu nie przeszkadza.
SELECT k.pseudo AS "Nie sa niczyim szefem"
FROM kocury k
WHERE NOT EXISTS (SELECT 1 FROM kocury p WHERE p.szef = k.pseudo)
ORDER BY k.pseudo;

-- Odfiltrowanie NULL sprawia, ze NOT IN daje ten sam wynik co NOT EXISTS.
SELECT pseudo AS "Nie sa niczyim szefem"
FROM kocury
WHERE pseudo NOT IN (SELECT szef FROM kocury WHERE szef IS NOT NULL)
ORDER BY pseudo;

-- Zadanie 8: bez sredniej calego stada w wyniku
SELECT nr_bandy AS "Lepsze bandy",
       ROUND(AVG(przydzial_myszy + COALESCE(myszy_extra, 0)), 1)
         AS "Sredni przydzial w bandzie"
FROM kocury
GROUP BY nr_bandy
HAVING AVG(przydzial_myszy + COALESCE(myszy_extra, 0)) >
       (SELECT AVG(przydzial_myszy + COALESCE(myszy_extra, 0)) FROM kocury)
ORDER BY nr_bandy;

-- Zadanie 8: ze srednia calego stada w wyniku
SELECT nr_bandy AS "Lepsze bandy",
       ROUND(AVG(przydzial_myszy + COALESCE(myszy_extra, 0)), 1)
         AS "Sredni przydzial w bandzie",
       (SELECT ROUND(AVG(przydzial_myszy + COALESCE(myszy_extra, 0)), 1)
        FROM kocury) AS "Sredni przydzial"
FROM kocury
GROUP BY nr_bandy
HAVING AVG(przydzial_myszy + COALESCE(myszy_extra, 0)) >
       (SELECT AVG(przydzial_myszy + COALESCE(myszy_extra, 0)) FROM kocury)
ORDER BY nr_bandy;

-- Zadanie 9: MONTH bez TM daje angielskie nazwy jak w przykladzie.
SELECT TO_CHAR(w_stadku_od, 'FMMONTH') AS "Miesiac", COUNT(*) AS "Liczba rekrutow"
FROM kocury
WHERE w_stadku_od IS NOT NULL
GROUP BY EXTRACT(MONTH FROM w_stadku_od), TO_CHAR(w_stadku_od, 'FMMONTH')
ORDER BY EXTRACT(MONTH FROM w_stadku_od);

-- Zadanie 10: >= ALL zamiast MAX; CALOSC obejmuje tez sad.
SELECT imie AS "Imie", funkcja AS "Funkcja", przydzial_myszy AS "Przydzial myszy"
FROM kocury
WHERE przydzial_myszy >= ALL (
  SELECT 3 * k.przydzial_myszy
  FROM kocury k
  JOIN bandy b ON b.nr_bandy = k.nr_bandy
  WHERE k.funkcja = 'MILUSIA' AND b.teren IN ('SAD', 'CALOSC')
    AND k.przydzial_myszy IS NOT NULL
)
ORDER BY imie;
