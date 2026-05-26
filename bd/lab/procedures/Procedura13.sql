SELECT DISTINCT
    p.NazwaP AS Przedmiot
FROM Przedmioty p
INNER JOIN Oceny o ON o.IdP = p.IdP
ORDER BY p.NazwaP ASC;
