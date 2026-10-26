-- Zadanie 8
SELECT imie,
       CASE
         WHEN 12 * (przydzial_myszy + COALESCE(myszy_extra, 0)) > 660
           THEN CAST(12 * (przydzial_myszy + COALESCE(myszy_extra, 0)) AS text)
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
