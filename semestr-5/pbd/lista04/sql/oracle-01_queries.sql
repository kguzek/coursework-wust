-- Zadanie 1
-- Calkowity przydzial uwzglednia myszy_extra; brak dodatku to NULL.
-- Funkcje bez kotow z obu band (DZIELCZY) zostaja z pustymi wartosciami.
SELECT k.funkcja AS "FUNKCJA",
       SUM(CASE WHEN b.nazwa = 'CZARNI RYCERZE'
                THEN k.przydzial_myszy + COALESCE(k.myszy_extra, 0) END)
         AS "Banda CZARNI RYCERZE",
       SUM(CASE WHEN b.nazwa = 'BIALI LOWCY'
                THEN k.przydzial_myszy + COALESCE(k.myszy_extra, 0) END)
         AS "Banda BIALI LOWCY"
FROM kocury k
LEFT JOIN bandy b ON b.nr_bandy = k.nr_bandy
WHERE k.funkcja <> 'SZEFUNIO'
GROUP BY k.funkcja
ORDER BY k.funkcja;

-- Zadanie 2
-- SUM(CASE ... THEN 1 END) daje NULL zamiast 0, jak puste pola w przykladzie.
SELECT k.funkcja AS "FUNKCJA", k.plec AS "P",
       SUM(CASE WHEN b.nazwa = 'CZARNI RYCERZE'
                THEN k.przydzial_myszy + COALESCE(k.myszy_extra, 0) END)
         AS "Banda CZARNI RYCERZE",
       SUM(CASE WHEN b.nazwa = 'CZARNI RYCERZE' THEN 1 END) AS "Ile",
       SUM(CASE WHEN b.nazwa = 'BIALI LOWCY'
                THEN k.przydzial_myszy + COALESCE(k.myszy_extra, 0) END)
         AS "Banda BIALI LOWCY",
       SUM(CASE WHEN b.nazwa = 'BIALI LOWCY' THEN 1 END) AS "Ile"
FROM kocury k
LEFT JOIN bandy b ON b.nr_bandy = k.nr_bandy
WHERE k.funkcja <> 'SZEFUNIO'
GROUP BY k.funkcja, k.plec
ORDER BY k.funkcja, k.plec;

-- Zadanie 3
-- COUNT(k.pseudo) pomija wiersz NULL z LEFT JOIN; pusta suma to 0,
-- a srednia z pustego zbioru pozostaje NULL zamiast dzielenia przez zero.
SELECT f.funkcja AS "FUNKCJA", COUNT(k.pseudo) AS "KOTY",
       COALESCE(SUM(k.przydzial_myszy + COALESCE(k.myszy_extra, 0)), 0) AS "RAZEM",
       ROUND(AVG(k.przydzial_myszy + COALESCE(k.myszy_extra, 0)), 4) AS "SREDNIA"
FROM funkcje f
LEFT JOIN kocury k ON k.funkcja = f.funkcja
GROUP BY f.funkcja
ORDER BY f.funkcja;

-- Zadanie 3a: bez zabezpieczen
-- Zwykly JOIN gubi funkcje HONOROWA, bo nie ma dla niej pary w kocury.
SELECT f.funkcja AS "FUNKCJA", COUNT(*) AS "KOTY",
       SUM(k.przydzial_myszy + COALESCE(k.myszy_extra, 0)) AS "RAZEM"
FROM funkcje f
JOIN kocury k ON k.funkcja = f.funkcja
GROUP BY f.funkcja
ORDER BY f.funkcja;

-- LEFT JOIN z COUNT(*) liczy wiersz uzupelniony NULL jako kota (HONOROWA: 1),
-- a SUM z samych NULL zwraca NULL zamiast 0.
SELECT f.funkcja AS "FUNKCJA", COUNT(*) AS "KOTY",
       SUM(k.przydzial_myszy + COALESCE(k.myszy_extra, 0)) AS "RAZEM"
FROM funkcje f
LEFT JOIN kocury k ON k.funkcja = f.funkcja
GROUP BY f.funkcja
ORDER BY f.funkcja;

-- Zadanie 4
-- Samozlaczenie z JACKIEM zastepuje podzapytanie o jego date.
SELECT k.imie AS "IMIE", k.w_stadku_od AS "POLUJE OD"
FROM kocury k
JOIN kocury j ON j.imie = 'JACEK' AND k.w_stadku_od < j.w_stadku_od
ORDER BY k.w_stadku_od DESC;

-- Zadanie 5
-- Remis na drugim miejscu rozstrzyga alfabetyczna kolejnosc pseudonimu:
-- w bandzie 4 DAMA i MAN zjadaja po 51, wybrana jest DAMA.
-- Pusta banda daje z LEFT JOIN jeden wiersz z numerem 1.
SELECT nr_bandy AS "NR_BANDY", nazwa AS "NAZWA", pseudo AS "PSEUDO",
       zjada AS "ZJADA"
FROM (
  SELECT b.nr_bandy, b.nazwa, k.pseudo,
         k.przydzial_myszy + COALESCE(k.myszy_extra, 0) AS zjada,
         ROW_NUMBER() OVER (
           PARTITION BY b.nr_bandy
           ORDER BY k.przydzial_myszy + COALESCE(k.myszy_extra, 0) DESC, k.pseudo
         ) AS miejsce
  FROM bandy b
  LEFT JOIN kocury k ON k.nr_bandy = b.nr_bandy
)
WHERE miejsce <= 2
ORDER BY nr_bandy, miejsce;

-- Zadanie 6
-- RANK pokazuje wszystkich rekordzistow przy remisie; HONOROWA zostaje
-- dzieki LEFT JOIN, a jej ocena jest NULL.
SELECT funkcja AS "FUNKCJA", pseudo AS "PSEUDO", zjada AS "ZJADA",
       CASE WHEN zjada > max_myszy THEN 'POWYZEJ WIDELEK'
            WHEN zjada < min_myszy THEN 'PONIZEJ WIDELEK'
            WHEN zjada IS NOT NULL THEN 'W WIDELKACH' END AS "OCENA"
FROM (
  SELECT f.funkcja, f.min_myszy, f.max_myszy, k.pseudo,
         k.przydzial_myszy + COALESCE(k.myszy_extra, 0) AS zjada,
         RANK() OVER (
           PARTITION BY f.funkcja
           ORDER BY k.przydzial_myszy + COALESCE(k.myszy_extra, 0) DESC
         ) AS miejsce
  FROM funkcje f
  LEFT JOIN kocury k ON k.funkcja = f.funkcja
)
WHERE miejsce = 1
ORDER BY funkcja;

-- Zadanie 7
-- Zamiast widoku wyrazenie WITH. Lata o liczbie rownej sredniej trafilyby
-- do grupy "od dolu" (<=). Kolumna kolejnosc ustawia srednia miedzy grupami.
WITH lata AS (
  SELECT EXTRACT(YEAR FROM w_stadku_od) AS rok, COUNT(*) AS liczba
  FROM kocury
  WHERE w_stadku_od IS NOT NULL
  GROUP BY EXTRACT(YEAR FROM w_stadku_od)
)
SELECT rok AS "ROK", liczba AS "LICZBA WSTAPIEN"
FROM (
  SELECT 1 AS kolejnosc, TO_CHAR(rok) AS rok, liczba
  FROM lata
  WHERE liczba = (SELECT MAX(liczba) FROM lata
                  WHERE liczba <= (SELECT AVG(liczba) FROM lata))
  UNION ALL
  SELECT 2, 'Srednia', ROUND(AVG(liczba), 7) FROM lata
  UNION ALL
  SELECT 3, TO_CHAR(rok), liczba
  FROM lata
  WHERE liczba = (SELECT MIN(liczba) FROM lata
                  WHERE liczba > (SELECT AVG(liczba) FROM lata))
)
ORDER BY kolejnosc, rok;

-- Zadanie 8
-- Kot jedyny w bandzie bylby jednoczesnie najstarszy i najmlodszy (2 wiersze).
-- MINUS usuwa oznaczone koty z listy kotow bez oznaczenia.
SELECT k.imie AS "IMIE", k.w_stadku_od AS "WSTAPIL DO STADKA",
       '<--- NAJSTARSZY STAZEM W BANDZIE ' || b.nazwa AS " "
FROM kocury k
JOIN bandy b ON b.nr_bandy = k.nr_bandy
WHERE k.w_stadku_od = (SELECT MIN(m.w_stadku_od) FROM kocury m
                       WHERE m.nr_bandy = k.nr_bandy)
UNION ALL
SELECT k.imie, k.w_stadku_od, '<--- NAJMLODSZY STAZEM W BANDZIE ' || b.nazwa
FROM kocury k
JOIN bandy b ON b.nr_bandy = k.nr_bandy
WHERE k.w_stadku_od = (SELECT MAX(m.w_stadku_od) FROM kocury m
                       WHERE m.nr_bandy = k.nr_bandy)
UNION ALL
(
  SELECT imie, w_stadku_od, ' ' FROM kocury
  MINUS
  SELECT k.imie, k.w_stadku_od, ' '
  FROM kocury k
  WHERE k.w_stadku_od IN (SELECT MIN(m.w_stadku_od) FROM kocury m
                          WHERE m.nr_bandy = k.nr_bandy
                          UNION
                          SELECT MAX(m.w_stadku_od) FROM kocury m
                          WHERE m.nr_bandy = k.nr_bandy)
)
ORDER BY 1;

-- Zadanie 9
-- Liczony jest przydzial podstawowy, jak w przykladzie: z dodatkiem
-- MALA (22 + 42) przekroczylaby prog funkcji MILUSIA.
SELECT k.pseudo AS "Do przeczolgania", b.nazwa AS "Nazwa bandy"
FROM kocury k
JOIN funkcje f ON f.funkcja = k.funkcja
LEFT JOIN bandy b ON b.nr_bandy = k.nr_bandy
WHERE NOT EXISTS (SELECT 1 FROM kocury p WHERE p.szef = k.pseudo)
  AND EXISTS (SELECT 1 FROM wrogowie_kocurow w WHERE w.pseudo = k.pseudo)
  AND k.przydzial_myszy >= f.min_myszy + (f.max_myszy - f.min_myszy) / 3
ORDER BY b.nazwa, k.pseudo;

-- Zadanie 10
-- Oracle pozwala zagniezdzic MAX(AVG(...)) przy GROUP BY w podzapytaniu.
SELECT funkcja AS "Funkcja",
       ROUND(AVG(przydzial_myszy + COALESCE(myszy_extra, 0)))
         AS "Srednio najw. i najm. myszy"
FROM kocury
WHERE funkcja <> 'SZEFUNIO'
GROUP BY funkcja
HAVING AVG(przydzial_myszy + COALESCE(myszy_extra, 0)) IN (
         (SELECT MAX(AVG(przydzial_myszy + COALESCE(myszy_extra, 0)))
          FROM kocury WHERE funkcja <> 'SZEFUNIO' GROUP BY funkcja),
         (SELECT MIN(AVG(przydzial_myszy + COALESCE(myszy_extra, 0)))
          FROM kocury WHERE funkcja <> 'SZEFUNIO' GROUP BY funkcja))
ORDER BY 2;

-- Zadanie 11a: zlaczenie bez podzapytan
-- Kot jest zlaczony z kazdym kotem swojej bandy, wiec AVG(m.) to srednia bandy.
SELECT k.imie AS "IMIE", k.przydzial_myszy + COALESCE(k.myszy_extra, 0) AS "ZJADA",
       k.nr_bandy AS "NR BANDY",
       ROUND(AVG(m.przydzial_myszy + COALESCE(m.myszy_extra, 0)), 2) AS "SREDNIA BANDY"
FROM kocury k
JOIN kocury m ON m.nr_bandy = k.nr_bandy
WHERE k.plec = 'M'
GROUP BY k.pseudo, k.imie, k.przydzial_myszy, k.myszy_extra, k.nr_bandy
HAVING k.przydzial_myszy + COALESCE(k.myszy_extra, 0)
       <= AVG(m.przydzial_myszy + COALESCE(m.myszy_extra, 0))
ORDER BY k.nr_bandy DESC;

-- Zadanie 11b: zlaczenie z jednym podzapytaniem w FROM
SELECT k.imie AS "IMIE", k.przydzial_myszy + COALESCE(k.myszy_extra, 0) AS "ZJADA",
       k.nr_bandy AS "NR BANDY", ROUND(s.srednia, 2) AS "SREDNIA BANDY"
FROM kocury k
JOIN (SELECT nr_bandy, AVG(przydzial_myszy + COALESCE(myszy_extra, 0)) AS srednia
      FROM kocury
      GROUP BY nr_bandy) s ON s.nr_bandy = k.nr_bandy
WHERE k.plec = 'M'
  AND k.przydzial_myszy + COALESCE(k.myszy_extra, 0) <= s.srednia
ORDER BY k.nr_bandy DESC;

-- Zadanie 11c: bez zlaczen, podzapytania w SELECT i WHERE
SELECT k.imie AS "IMIE", k.przydzial_myszy + COALESCE(k.myszy_extra, 0) AS "ZJADA",
       k.nr_bandy AS "NR BANDY",
       (SELECT ROUND(AVG(m.przydzial_myszy + COALESCE(m.myszy_extra, 0)), 2)
        FROM kocury m WHERE m.nr_bandy = k.nr_bandy) AS "SREDNIA BANDY"
FROM kocury k
WHERE k.plec = 'M'
  AND k.przydzial_myszy + COALESCE(k.myszy_extra, 0) <=
      (SELECT AVG(m.przydzial_myszy + COALESCE(m.myszy_extra, 0))
       FROM kocury m WHERE m.nr_bandy = k.nr_bandy)
ORDER BY k.nr_bandy DESC;

-- Zadanie 12a: DECODE i SUM
SELECT b.nazwa AS "NAZWA BANDY", DECODE(k.plec, 'D', 'Kotka', 'Kocor') AS "PLEC",
       COUNT(*) AS "ILE",
       SUM(DECODE(k.funkcja, 'SZEFUNIO', k.przydzial_myszy + COALESCE(k.myszy_extra, 0), 0)) AS "SZEFUNIO",
       SUM(DECODE(k.funkcja, 'BANDZIOR', k.przydzial_myszy + COALESCE(k.myszy_extra, 0), 0)) AS "BANDZIOR",
       SUM(DECODE(k.funkcja, 'LOWCZY', k.przydzial_myszy + COALESCE(k.myszy_extra, 0), 0)) AS "LOWCZY",
       SUM(DECODE(k.funkcja, 'LAPACZ', k.przydzial_myszy + COALESCE(k.myszy_extra, 0), 0)) AS "LAPACZ",
       SUM(DECODE(k.funkcja, 'KOT', k.przydzial_myszy + COALESCE(k.myszy_extra, 0), 0)) AS "KOT",
       SUM(DECODE(k.funkcja, 'MILUSIA', k.przydzial_myszy + COALESCE(k.myszy_extra, 0), 0)) AS "MILUSIA",
       SUM(DECODE(k.funkcja, 'DZIELCZY', k.przydzial_myszy + COALESCE(k.myszy_extra, 0), 0)) AS "DZIELCZY",
       SUM(k.przydzial_myszy + COALESCE(k.myszy_extra, 0)) AS "SUMA"
FROM kocury k
JOIN bandy b ON b.nr_bandy = k.nr_bandy
GROUP BY b.nazwa, k.plec
ORDER BY b.nazwa, k.plec;

-- Zadanie 12b: PIVOT
-- ILE i SUMA licza funkcje okna w zrodle; sa stale w grupie (banda, plec),
-- wiec PIVOT grupuje po nich razem z nazwa i plcia. Kolumna p nie
-- koliduje z aliasem PLEC, ktory w ORDER BY sortowalby Kocor przed Kotka.
SELECT nazwa AS "NAZWA BANDY", DECODE(p, 'D', 'Kotka', 'Kocor') AS "PLEC",
       ile AS "ILE",
       COALESCE(szefunio, 0) AS "SZEFUNIO", COALESCE(bandzior, 0) AS "BANDZIOR",
       COALESCE(lowczy, 0) AS "LOWCZY", COALESCE(lapacz, 0) AS "LAPACZ",
       COALESCE(kot, 0) AS "KOT", COALESCE(milusia, 0) AS "MILUSIA",
       COALESCE(dzielczy, 0) AS "DZIELCZY", suma AS "SUMA"
FROM (
  SELECT b.nazwa, k.plec AS p, k.funkcja,
         k.przydzial_myszy + COALESCE(k.myszy_extra, 0) AS zjada,
         COUNT(*) OVER (PARTITION BY b.nazwa, k.plec) AS ile,
         SUM(k.przydzial_myszy + COALESCE(k.myszy_extra, 0))
           OVER (PARTITION BY b.nazwa, k.plec) AS suma
  FROM kocury k
  JOIN bandy b ON b.nr_bandy = k.nr_bandy
)
PIVOT (
  SUM(zjada) FOR funkcja IN (
    'SZEFUNIO' AS szefunio, 'BANDZIOR' AS bandzior, 'LOWCZY' AS lowczy,
    'LAPACZ' AS lapacz, 'KOT' AS kot, 'MILUSIA' AS milusia,
    'DZIELCZY' AS dzielczy
  )
)
ORDER BY nazwa, p;
