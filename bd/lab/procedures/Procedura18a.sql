SELECT
    n.IdN,
    n.Nazwisko,
    n.Imie,
    p.NazwaP AS Przedmiot,
    u.IleGodz
FROM Nauczyciele n
INNER JOIN Uczy u ON n.IdN = u.IdN
INNER JOIN Przedmioty p ON u.IdP = p.IdP
WHERE CONCAT(n.Nazwisko, ' ', n.Imie) = p_dane
ORDER BY p.NazwaP ASC;
