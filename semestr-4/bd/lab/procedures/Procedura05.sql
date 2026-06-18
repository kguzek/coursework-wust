SELECT
    IdN,
    Nazwisko,
    Imie,
    DZatr,
    TIMESTAMPDIFF(YEAR, DZatr, CURDATE()) AS StazLata,
    DUr,
    Plec,
    Pensja,
    Premia,
    Pensum,
    Telefon
FROM Nauczyciele
WHERE TIMESTAMPDIFF(YEAR, DZatr, CURDATE()) < p_staz_lata
ORDER BY StazLata ASC, Nazwisko ASC, Imie ASC;
