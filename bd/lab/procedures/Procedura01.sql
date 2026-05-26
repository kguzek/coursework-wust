SELECT
    u.Nazwisko,
    u.Imie,
    u.IdU AS NumerUcznia,
    u.Klasa,
    m.NazwaM AS Miasto
FROM Uczniowie u
LEFT JOIN Miasta m ON u.Miasto = m.IdM
WHERE LEFT(u.Klasa, 1) IN ('1', '2', '3');
