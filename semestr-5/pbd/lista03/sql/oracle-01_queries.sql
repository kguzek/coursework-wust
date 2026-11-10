-- Zadanie 1
-- Kot bez incydentow nie ma wroga, wiec warunek imienia wroga dotyczy tylko
-- kotow wczesniejszych od szefa - jak w przykladzie.
SELECT DISTINCT k.imie AS "W stadku przed szefem lub bez incydentu",
       CASE WHEN k.w_stadku_od < j.w_stadku_od THEN 'Tak'
            ELSE 'Nie' END AS "Przed Jackiem"
FROM kocury k
LEFT JOIN kocury s ON s.pseudo = k.szef
LEFT JOIN wrogowie_kocurow w ON w.pseudo = k.pseudo
CROSS JOIN kocury j
WHERE j.imie = 'JACEK'
  AND (k.w_stadku_od < s.w_stadku_od AND w.imie_wroga LIKE '%A'
       OR w.pseudo IS NULL)
ORDER BY 1;

-- Zadanie 2
-- Plec filtrujemy po zlaczeniu, wiec brak oznacza brak jakiegokolwiek
-- przelozonego/podwladnego: kotki przy ZOMBI i ZERO nie daja wierszy "Brak".
SELECT COALESCE(s.pseudo, 'Brak przelozonego') AS "Przelozony",
       COALESCE(k.pseudo, 'Brak podwladnego') AS "Podwladny"
FROM kocury s
FULL JOIN kocury k ON k.szef = s.pseudo
WHERE (s.plec = 'M' OR s.pseudo IS NULL)
  AND (k.plec = 'M' OR k.pseudo IS NULL)
ORDER BY 1, 2;

-- Zadanie 3
-- Jak w przykladzie liczymy przydzial podstawowy, bez myszy_extra.
-- Dzielenie przez liczbe wrogow usuwa powielenie sumy przez zlaczenie;
-- klucz (pseudo, imie_wroga) gwarantuje, ze wrogowie kota sa rozni.
SELECT k.pseudo, k.przydzial_myszy,
       SUM(m.przydzial_myszy) / COUNT(DISTINCT w.imie_wroga) AS sum_w_bandzie,
       ROUND(100 * k.przydzial_myszy * COUNT(DISTINCT w.imie_wroga)
             / NULLIF(SUM(m.przydzial_myszy), 0)) AS proc_w_bandzie
FROM kocury k
JOIN bandy b ON b.nr_bandy = k.nr_bandy
JOIN kocury m ON m.nr_bandy = k.nr_bandy
JOIN wrogowie_kocurow wk ON wk.pseudo = k.pseudo
JOIN wrogowie w ON w.imie_wroga = wk.imie_wroga
WHERE b.teren IN ('POLE', 'CALOSC')
  AND w.stopien_wrogosci BETWEEN 6 AND 10
GROUP BY k.pseudo, k.przydzial_myszy
ORDER BY k.pseudo;

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

-- Zadanie 6b
SELECT nr_bandy AS "Nr bandy", nazwa AS "Nazwa", teren AS "Teren"
FROM bandy
MINUS
SELECT b.nr_bandy, b.nazwa, b.teren
FROM bandy b
JOIN kocury k ON k.nr_bandy = b.nr_bandy
ORDER BY 1;

-- Zadanie 7: prominenci i szaraki; remisy na minimum zostaja.
-- DECODE porownuje NULL jak zwykla wartosc, wiec koty bez bandy tworza grupe.
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
    WHERE DECODE(m.nr_bandy, k.nr_bandy, 1) = 1
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

-- Zadanie 9: nazwy jak w przykladzie, niezaleznie od jezyka sesji.
SELECT TO_CHAR(w_stadku_od, 'FMMONTH', 'NLS_DATE_LANGUAGE=ENGLISH') AS "Miesiac",
       COUNT(*) AS "Liczba rekrutow"
FROM kocury
WHERE w_stadku_od IS NOT NULL
GROUP BY EXTRACT(MONTH FROM w_stadku_od),
         TO_CHAR(w_stadku_od, 'FMMONTH', 'NLS_DATE_LANGUAGE=ENGLISH')
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

-- Zadanie 11
-- Plec filtrujemy po zbudowaniu drzewa: ZERO ma po drodze kotke KURKA.
SELECT LEVEL AS "Poziom", pseudo AS "Pseudonim", funkcja AS "Funkcja",
       nr_bandy AS "Nr bandy"
FROM kocury
WHERE plec = 'M'
START WITH plec = 'M' AND funkcja = 'BANDZIOR'
CONNECT BY PRIOR pseudo = szef
ORDER SIBLINGS BY pseudo;

-- Zadanie 12
-- Wciecia jak w przykladzie. Staz liczony od biezacej daty; wynik z PDF
-- daje zamiana TRUNC(SYSDATE) na DATE '2024-07-17'.
SELECT LPAD(' ', 4 * (LEVEL - 1)) || pseudo AS "Droga sluzbowa"
FROM kocury
START WITH plec = 'M' AND w_stadku_od < ADD_MONTHS(TRUNC(SYSDATE), -180)
           AND COALESCE(myszy_extra, 0) = 0
CONNECT BY PRIOR szef = pseudo
ORDER BY CONNECT_BY_ROOT pseudo, LEVEL;

-- Zadanie 13a: trzy poziomy szefow wystarczaja dla danych z listy.
SELECT k.imie AS "Imie", k.funkcja AS "Funkcja",
       s1.imie AS "Szef 1", s2.imie AS "Szef 2", s3.imie AS "Szef 3"
FROM kocury k
LEFT JOIN kocury s1 ON s1.pseudo = k.szef
LEFT JOIN kocury s2 ON s2.pseudo = s1.szef
LEFT JOIN kocury s3 ON s3.pseudo = s2.szef
WHERE k.funkcja IN ('KOT', 'MILUSIA')
ORDER BY k.imie;

-- Zadanie 13b: pelna sciezka, bez stalego limitu liczby szefow.
-- Sciezka zaczyna sie od imienia kota; ucinamy ja do drugiego separatora.
SELECT CONNECT_BY_ROOT imie AS "Imie", CONNECT_BY_ROOT funkcja AS "Funkcja",
       SUBSTR(SYS_CONNECT_BY_PATH(imie, ' | '),
              INSTR(SYS_CONNECT_BY_PATH(imie, ' | '), ' | ', 1, 2) + 3)
         AS "Imiona kolejnych szefow"
FROM kocury
WHERE CONNECT_BY_ISLEAF = 1
START WITH funkcja IN ('KOT', 'MILUSIA')
CONNECT BY PRIOR szef = pseudo
ORDER BY 1;
