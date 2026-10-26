-- Zadanie 1
SELECT imie_wroga AS wrog, opis_incydentu AS przewina
FROM wrogowie_kocurow
WHERE data_incydentu >= DATE '2009-01-01'
  AND data_incydentu < DATE '2010-01-01';

-- Zadanie 2
SELECT imie, funkcja, TO_CHAR(w_stadku_od, 'YYYY-MM-DD') AS "Z NAMI OD"
FROM kocury
WHERE plec = 'D'
  AND w_stadku_od >= DATE '2005-09-01'
  AND w_stadku_od < DATE '2007-08-01';

-- Zadanie 3
SELECT imie_wroga AS wrog, gatunek, stopien_wrogosci AS "STOPIEN WROGOSCI"
FROM wrogowie
WHERE lapowka IS NULL
ORDER BY stopien_wrogosci;

-- Zadanie 4
SELECT imie || ' zwany ' || pseudo || ' (fun. ' || funkcja
       || ') lowi myszki w bandzie ' || TO_CHAR(nr_bandy)
       || ' od ' || TO_CHAR(w_stadku_od, 'YYYY-MM-DD') AS "WSZYSTKO O KOCURACH"
FROM kocury
WHERE plec = 'M'
ORDER BY w_stadku_od DESC, pseudo;

-- Zadanie 5
SELECT pseudo, INSTR(pseudo, 'A') AS a, INSTR(pseudo, 'L') AS l,
       REGEXP_REPLACE(REGEXP_REPLACE(pseudo, 'A', '#', 1, 1),
                      'L', '%', 1, 1) AS "Po wymianie A na # oraz L na %"
FROM kocury
WHERE INSTR(pseudo, 'A') > 0 AND INSTR(pseudo, 'L') > 0
ORDER BY pseudo;

-- Zadanie 6
SELECT imie, TO_CHAR(w_stadku_od, 'YYYY-MM-DD') AS "W stadku",
       ROUND(przydzial_myszy / 1.1) AS "Zjadal",
       TO_CHAR(ADD_MONTHS(w_stadku_od, 6), 'YYYY-MM-DD') AS "Podwyzka",
       przydzial_myszy AS "Zjada"
FROM kocury
WHERE w_stadku_od <= ADD_MONTHS(TRUNC(SYSDATE), -180)
  AND EXTRACT(MONTH FROM w_stadku_od) BETWEEN 3 AND 9;

-- Zadanie 7
SELECT imie, 3 * przydzial_myszy AS "MYSZY KWRTALNIE",
       3 * COALESCE(myszy_extra, 0) AS "KWARTALNE DODATKI"
FROM kocury
WHERE przydzial_myszy > 2 * COALESCE(myszy_extra, 0)
  AND przydzial_myszy >= 55
ORDER BY przydzial_myszy DESC, imie;

-- Zadanie 8
SELECT imie,
       CASE
         WHEN 12 * (przydzial_myszy + COALESCE(myszy_extra, 0)) > 660
           THEN TO_CHAR(12 * (przydzial_myszy + COALESCE(myszy_extra, 0)))
         WHEN 12 * (przydzial_myszy + COALESCE(myszy_extra, 0)) = 660
           THEN 'Limit'
         ELSE 'Ponizej 660'
       END AS "Zjada rocznie"
FROM kocury
ORDER BY imie;

-- Zadanie 9
SELECT pseudo || ' - ' || CASE WHEN COUNT(*) = 1 THEN 'Unikalny'
                              ELSE 'nieunikalny' END AS "Unikalnosc atr. PSEUDO"
FROM kocury
GROUP BY pseudo
ORDER BY pseudo;

SELECT szef || ' - ' || CASE WHEN COUNT(*) = 1 THEN 'Unikalny'
                            ELSE 'nieunikalny' END AS "Unikalnosc atr. SZEF"
FROM kocury
WHERE szef IS NOT NULL
GROUP BY szef
ORDER BY szef;

-- Zadanie 10
SELECT pseudo AS "Pseudonim", COUNT(*) AS "Liczba wrogow"
FROM wrogowie_kocurow
GROUP BY pseudo
HAVING COUNT(*) >= 2
ORDER BY pseudo;

-- Zadanie 11: 29.10.2024
SELECT pseudo, TO_CHAR(w_stadku_od, 'YYYY-MM-DD') AS "W STADKU",
       TO_CHAR(TRUNC(LAST_DAY(
         ADD_MONTHS(DATE '2024-10-29',
                    CASE WHEN EXTRACT(DAY FROM w_stadku_od) <= 15 THEN 0 ELSE 1 END)
       ) - 2, 'IW') + 2, 'YYYY-MM-DD') AS wyplata
FROM kocury
ORDER BY w_stadku_od, pseudo;

-- Zadanie 11: 31.10.2024
SELECT pseudo, TO_CHAR(w_stadku_od, 'YYYY-MM-DD') AS "W STADKU",
       TO_CHAR(TRUNC(LAST_DAY(ADD_MONTHS(DATE '2024-10-31', 1)) - 2, 'IW') + 2,
               'YYYY-MM-DD') AS wyplata
FROM kocury
ORDER BY w_stadku_od, pseudo;

-- Zadanie 12
SELECT 'Liczba kotow=' AS opis, COUNT(*) AS liczba, 'lowi jako' AS czynnosc,
       funkcja, 'i zjada max.' AS spozycie,
       TO_CHAR(MAX(przydzial_myszy + COALESCE(myszy_extra, 0)), 'FM990.00') AS maksimum,
       'myszy miesiecznie' AS okres
FROM kocury
WHERE plec = 'D' AND funkcja <> 'SZEFUNIO'
GROUP BY funkcja
HAVING AVG(przydzial_myszy + COALESCE(myszy_extra, 0)) > 50
ORDER BY funkcja;

-- Zadanie 13
SELECT nr_bandy AS "Nr bandy", plec AS "Plec",
       MIN(przydzial_myszy) AS "Minimalny przydzial"
FROM kocury
GROUP BY nr_bandy, plec
ORDER BY nr_bandy, plec;
