# Systemy Operacyjne — Laboratoria

## Zadanie 3 — Algorytmy Badania Stron

- sekwencje można generować na początku

### Wymagania

- błąd strony (zliczanie)
    - proces żąda strony, której nie ma w pamięci operacyjnej
    - to nie jest moment, w którym zastępujemy stronę
    - PFF (Page Fault Frequency)
    - Szamotanie (np. >= 4 błędy na 5 żądań — szamotanie)

### Algorytmy

- FIFO
- RAND (losowanie _stron_)
- OPT
- LRU
- aLRU