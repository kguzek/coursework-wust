# Lista projektowa nr 1

Utworzono relacje wraz z kluczami, ograniczeniami dziedzinowymi i danymi
podanymi w zadaniu.

Jedyny `ALTER TABLE` dodaje klucz obcy `bandy.szef_bandy -> kocury.pseudo`.
Przy zachowaniu zadanego schematu jest potrzebny z powodu cyklu zależności:
`kocury.nr_bandy` wskazuje na `bandy`, a `bandy.szef_bandy` na `kocury`.
Wariant bez `ALTER TABLE` wymaga zmiany modelu, np. wyznaczania lidera bandy
na podstawie danych `kocury`; usuwa to cykl, ale wymaga dodatkowej kontroli
jednego lidera i nie zachowuje dosłownie zadanego schematu.

W PostgreSQL zmieniono `VARCHAR2` na `varchar`, `NUMBER` na `numeric`,
`SYSDATE` na `CURRENT_DATE`, a `INSERT ALL` na wielowierszowe `VALUES`.

Podsumowanie: oba SZBD pozwalają zrealizować model i ograniczenia
integralności. PostgreSQL ma krótszą składnię wstawiania wielu wierszy,
natomiast Oracle wymaga kilku zmian typów i składni.
