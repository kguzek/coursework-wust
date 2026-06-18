SELECT
    u.IdU AS Numer,
    u.Nazwisko,
    u.Imie,
    AVG(o.Ocena) AS SredniaOcen
FROM Uczniowie u
INNER JOIN Oceny o ON u.IdU = o.IdU
GROUP BY u.IdU, u.Nazwisko, u.Imie
ORDER BY u.Nazwisko ASC, u.Imie ASC;
