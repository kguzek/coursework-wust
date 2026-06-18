SELECT
    u.IdU AS NumerUcznia,
    u.Nazwisko,
    u.Imie,
    u.Klasa,
    m.NazwaM AS Miasto
FROM Uczniowie u
INNER JOIN Miasta m ON u.Miasto = m.IdM
WHERE LEFT(u.Klasa, 1) = '2'
  AND UPPER(LEFT(m.NazwaM, 1)) BETWEEN 'B' AND 'R'
ORDER BY u.Nazwisko ASC, u.Imie ASC;
