SELECT
    m.NazwaM AS Miasto,
    COUNT(u.IdU) AS LiczbaUczniow
FROM Miasta m
LEFT JOIN Uczniowie u ON u.Miasto = m.IdM
GROUP BY m.IdM, m.NazwaM
ORDER BY m.NazwaM ASC;
