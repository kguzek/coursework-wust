SELECT
    u.IdU AS Numer,
    u.Nazwisko,
    u.Imie
FROM Uczniowie u
INNER JOIN Miasta m ON u.Miasto = m.IdM
WHERE m.NazwaM IN ('Brzeg', 'Brzeg Dolny', 'Poznań', 'Poznan')
ORDER BY u.Nazwisko ASC, u.Imie ASC;
