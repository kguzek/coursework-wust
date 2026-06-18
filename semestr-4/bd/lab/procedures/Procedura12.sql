SELECT DISTINCT
    m.NazwaM AS Miasto
FROM Miasta m
INNER JOIN Uczniowie u ON u.Miasto = m.IdM
ORDER BY m.NazwaM ASC;
