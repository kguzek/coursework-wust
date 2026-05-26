SELECT
    IdN,
    Nazwisko,
    Imie,
    DZatr,
    TIMESTAMPDIFF(YEAR, DZatr, CURDATE()) AS LataPracy,
    DUr,
    Plec,
    Pensja,
    Premia,
    Pensum,
    Telefon
FROM Nauczyciele
WHERE DZatr >= '2014-09-01';
