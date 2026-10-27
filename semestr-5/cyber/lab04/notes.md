# Cyberbezpieczeństwo laboratorium

2026-10-27

Konrad Guzek grupa 8

## 1. Algorytmy asymetryczne

### 1.1 Demonstracja RSA

W CrypTool 1.4.42 wybrano `Encrypt/Decrypt → Asymmetric → RSA Demonstration`. Do demonstracji użyto małych liczb, żeby można było łatwo sprawdzić obliczenia.

| Parametr | Wartość |
| --- | ---: |
| Liczba pierwsza `p` | 61 |
| Liczba pierwsza `q` | 53 |
| Moduł `N=pq` | 3233 |
| `φ(N)=(p−1)(q−1)` | 3120 |
| Wykładnik publiczny `e` | 17 |
| Wykładnik prywatny `d` | 2753 |

Po wybraniu `Update parameters` program obliczył `N`, `φ(N)` i `d`. Dla wejścia liczbowego `M=65` szyfrowanie dało `C=2790`. Następnie wpisano `2790` jako wejście do deszyfrowania: wynik wynosił `0065`, a odpowiadający mu znak to `A`. Początkowa wartość została więc odzyskana.

```text
C = 65^17 mod 3233 = 2790
M = 2790^2753 mod 3233 = 65
17 × 2753 mod 3120 = 1
```

Klucz publiczny to para `(N,e)`, a prywatny zawiera `d`. Wykładnik `e` musi być względnie pierwszy z `φ(N)`, czyli `NWD(e,φ(N))=1`; samo stwierdzenie, że nie jest dzielnikiem `φ(N)`, nie wystarcza. Tak małe liczby służą tylko do pokazania działania RSA, nie do bezpiecznego szyfrowania.

### 1.2 Generowanie kluczy

Wybrano `Digital Signatures/PKI → PKI → Generate/Import Keys`, algorytm RSA i kolejno trzy długości modułu. Dla każdej pary CrypTool potwierdził utworzenie i zapisanie kluczy w magazynie chronionym testowym PIN-em.

| Długość modułu | Identyfikator | Czas generowania pary [s] |
| --- | --- | ---: |
| 512 bitów | `Lab04-RSA-512` | 0,024 |
| 1024 bity | `Lab04-RSA-1024` | 0,176 |
| 2048 bitów | `Lab04-RSA-2048` | 1,224 |

W tej próbie wygenerowanie dłuższej pary trwało dłużej. Są to pojedyncze pomiary czasu **generowania kluczy**, a nie szyfrowania lub deszyfrowania pliku. RSA-512 i RSA-1024 wykorzystano zgodnie z instrukcją wyłącznie do porównania laboratoryjnego; nie są odpowiednie do nowych zastosowań wymagających bezpieczeństwa.

### 1.3 Entropia i autokorelacja — pierwsza próbka

Przygotowano i otwarto w CrypTool plik `uniform.txt`: 1024 bajty ASCII, znak `H` powtórzony 1024 razy, bez końcowego znaku nowej linii. Entropia takiego TJ wynosi dokładnie `0 bit/B`. Wszystkie bajty są jednakowe, więc przy przesunięciu o `k` bajtów zgadza się każde z `1024−k` porównań, dla `1≤k<1024`; jest to własność próbki, nie odczyt z wykresu programu.

Do pierwszej próby użyto istniejącego klucza `Konrad Guzek`, RSA-1024, bez dodatkowego identyfikatora. Jest to inna para niż `Lab04-RSA-1024` z punktu 1.2. Wybrano zwykłe `RSA Encryption`, nie wariant hybrydowy RSA-AES. Kryptogram zapisano jako `uniform-user1024.hex`; mimo rozszerzenia plik zawiera surowe bajty, a nie tekstowy zapis szesnastkowy. Statystyki obliczono z zapisanych bajtów, dla alfabetu 256 wartości, poza interfejsem CrypTool.

| TJ | Klucz | H(TJ) [bit/B] | Długość TT [B] | H(TT) [bit/B] | Różne bloki TT po 128 B |
| --- | --- | ---: | ---: | ---: | ---: |
| `H` × 1024 | RSA-1024, istniejący `Konrad Guzek` | 0,0000 | 1152 | 6,7934 | 2 |

Pierwsze 16 B kryptogramu: `9e6c29b471b9cf4a15b447668c275199`.

Osiem pierwszych bloków TT po 128 B jest identycznych; dziewiąty jest inny. Entropia wzrosła, ale nadal widać regularność. W tej opcji programu powtarzające się pełne bloki są szyfrowane tak samo, więc samo RSA nie ukryło wzorca tekstu jednorodnego. Nie jest to zachowanie oczekiwane od szyfrowania z losowym dopełnieniem, np. RSA-OAEP.

Autokorelację policzono jako liczbę równych bajtów przy danym przesunięciu, bez zawijania końca pliku.

| Przesunięcie [B] | TJ: zgodne / porównane | TT: zgodne / porównane |
| --- | ---: | ---: |
| 1 | 1023 / 1023 | 0 / 1151 |
| 2 | 1022 / 1022 | 9 / 1150 |
| 16 | 1008 / 1008 | 8 / 1136 |
| 64 | 960 / 960 | 1 / 1088 |
| 128 | 896 / 896 | 898 / 1024 |
| 256 | 768 / 768 | 770 / 896 |

Przy przesunięciach 128 i 256 B występują wyraźne piki, wynikające z powtarzania bloków kryptogramu. Długość modułu RSA-1024 wynosi właśnie 128 B.

### Kontrola deszyfrowania

Zapisany kryptogram odszyfrowano w CrypTool tym samym kluczem i zapisano jako `uniform-user1024-recovered.bin`. Porównanie plików wykazało, że pierwsze 1024 B są dokładnie zgodne z oryginałem, ale wynik zawiera dodatkowo 119 zerowych bajtów na końcu, czyli łącznie 1143 B. Nie jest więc identyczny bajtowo z plikiem wejściowym.

Rozmiary odpowiadają podziałowi TJ na bloki po 127 B: `9 × 127 = 1143 B` po deszyfrowaniu i `9 × 128 = 1152 B` kryptogramu. Ostatni blok został uzupełniony zerami, których program nie usunął. Przy takim dopełnieniu do odzyskania dokładnego pliku trzeba znać jego pierwotną długość; usuwanie wszystkich zer z końca mogłoby skasować prawidłowe dane.

### Dalsze pomiary

Do wykonania pozostają pełne porównania dla trzech tekstów i trzech długości klucza (1.3), pomiary czasu dla plików 1, 2 i 5 MB oraz porównanie z szyfrem symetrycznym (1.4–1.5), a także próby uszkadzania kryptogramów (1.6). Wnioski 1.7–1.15 należy uzupełnić po tych eksperymentach.
