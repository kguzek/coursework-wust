-- Expected counts: 8 functions, 5 gangs, 18 cats, 10 enemies, 18 incidents.
SELECT 'funkcje' AS relacja, count(*) AS liczba_wierszy FROM funkcje
UNION ALL SELECT 'bandy', count(*) FROM bandy
UNION ALL SELECT 'kocury', count(*) FROM kocury
UNION ALL SELECT 'wrogowie', count(*) FROM wrogowie
UNION ALL SELECT 'wrogowie_kocurow', count(*) FROM wrogowie_kocurow
ORDER BY relacja;

-- Referential integrity should hold: each result is zero.
SELECT
  (SELECT count(*) FROM kocury k LEFT JOIN bandy b ON b.nr_bandy = k.nr_bandy WHERE k.nr_bandy IS NOT NULL AND b.nr_bandy IS NULL) AS cats_without_gang,
  (SELECT count(*) FROM bandy b LEFT JOIN kocury k ON k.pseudo = b.szef_bandy WHERE b.szef_bandy IS NOT NULL AND k.pseudo IS NULL) AS gangs_without_leader,
  (SELECT count(*) FROM wrogowie_kocurow wk LEFT JOIN kocury k ON k.pseudo = wk.pseudo WHERE k.pseudo IS NULL) AS incidents_without_cat,
  (SELECT count(*) FROM wrogowie_kocurow wk LEFT JOIN wrogowie w ON w.imie_wroga = wk.imie_wroga WHERE w.imie_wroga IS NULL) AS incidents_without_enemy;
