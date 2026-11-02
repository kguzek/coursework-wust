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

### 1.3 Entropia i autokorelacja

Użyto tych samych tekstów jawnych co w laboratorium 3 (po 1024 B ASCII, bez końcowego znaku nowej linii) i kluczy `Lab04-RSA-512`, `Lab04-RSA-1024`, `Lab04-RSA-2048` z punktu 1.2. Wybrano zwykłe `RSA Encryption`, nie wariant hybrydowy RSA-AES. Kryptogramy zapisano jako pliki binarne, a entropię i autokorelację obliczono z zapisanych bajtów, dla alfabetu 256 wartości.

| TJ | Konstrukcja | H(TJ) [bit/B] |
| --- | --- | ---: |
| Jednorodny | `H` × 1024 | 0,0000 |
| Średni | powtarzane `agree all use city with model ` (okres 30 B) | 3,7662 |
| Wysoki | angielski akapit o szyfrach blokowych (okres 174 B) | 4,2337 |

CrypTool dzieli TJ na bloki o jeden bajt krótsze od modułu (63, 127 albo 255 B) i każdy z nich zamienia na blok TT długości modułu (64, 128 albo 256 B). Ostatni blok jest dopełniany zerami. Stąd długości TT: 17 × 64 = 1088 B, 9 × 128 = 1152 B i 5 × 256 = 1280 B.

| TJ | H(TT) RSA-512 | H(TT) RSA-1024 | H(TT) RSA-2048 | Różne bloki TT (512 / 1024 / 2048) |
| --- | ---: | ---: | ---: | ---: |
| Jednorodny | 6,0262 | 6,9330 | 7,4424 | 2/17, 2/9, 2/5 |
| Średni | 7,6603 | 7,8322 | 7,6874 | 11/17, 9/9, 3/5 |
| Wysoki | 7,8200 | 7,8215 | 7,8648 | 17/17, 9/9, 5/5 |

| Kryptogram | Pierwsze 16 B TT (hex) |
| --- | --- |
| Jednorodny, RSA-512 | `8ba32aa0245817b5b472bfcbc4e25215` |
| Jednorodny, RSA-1024 | `4a0df522d38252e258ae81d3d10491b3` |
| Jednorodny, RSA-2048 | `ab6baa5ff78de70841c24de6ca9797b4` |
| Wysoki, RSA-2048 | `3fbf5180c642a184eea328615f69a609` |

Dla tekstu jednorodnego wszystkie pełne bloki TT są identyczne; inny jest tylko ostatni, dopełniony zerami. Szyfrowanie w tej opcji programu jest deterministyczne, bez losowego dopełnienia, więc identyczne bloki TJ dają identyczne bloki TT. To samo widać w tekście średnim: przy blokach 63 B wzorzec o okresie 30 B wraca co 10 bloków (630 = 21 × 30), a przy blokach 255 B co 2 bloki (510 = 17 × 30). Przy blokach 127 B powtórzenie wypadłoby dopiero po 30 blokach, czyli poza próbką. Wartości około 7,8 bit/B są typowe dla losowych danych tej długości (próbka ok. 1 KB nie pozwala osiągnąć 8,0).

Autokorelację policzono jako liczbę równych bajtów przy danym przesunięciu, bez zawijania końca pliku.

| Próbka | Przesunięcie [B] | Zgodne / porównane | Pozostałe przesunięcia |
| --- | ---: | ---: | --- |
| TJ jednorodny | dowolne `k` | `1024−k` / `1024−k` | wszystkie bajty zgodne |
| TJ średni | 30 | 994 / 994 | pik co 30 B |
| TJ wysoki | 174 | 850 / 850 | pik co 174 B |
| TT jednorodny, RSA-512 | 64 | 961 / 1024 | ≤ 17 dla 1–63 |
| TT jednorodny, RSA-1024 | 128 | 896 / 1024 | ≤ 23 dla 1–127 |
| TT jednorodny, RSA-2048 | 256 | 769 / 1024 | ≤ 17 dla 1–255 |
| TT średni, RSA-512 | 640 | 384 / 448 | brak piku przy 30 B |
| TT średni, RSA-1024 | — | — | brak piku, maks. 11 |
| TT średni, RSA-2048 | 512 | 513 / 768 | brak piku przy 30 B |
| TT wysoki, każdy klucz | — | — | brak piku, maks. 10 |

Okres TJ nie przenosi się bezpośrednio do TT; autokorelacja TT ma piki tylko przy wielokrotnościach długości bloku, i to wtedy, gdy całe bloki TJ się powtarzają.

Każdy kryptogram odszyfrowano tym samym kluczem. We wszystkich 9 przypadkach pierwsze 1024 B wyniku były zgodne z TJ, ale wynik miał 1071, 1143 albo 1275 B (17 × 63, 9 × 127, 5 × 255): program nie usuwa zer dopełnienia. Do odzyskania dokładnego pliku trzeba więc znać jego pierwotną długość; usuwanie wszystkich zer z końca mogłoby skasować prawidłowe dane.

### 1.4–1.5 Czas szyfrowania i deszyfrowania

Pliki 1, 2 i 5 MB (1 048 576, 2 097 152 i 5 242 880 B) zawierały powtarzany angielski akapit z punktu 1.3. Dla RSA zaznaczono `Display encryption time` / `Display decryption time` i odczytano czas podany przez CrypTool. Jako szyfr symetryczny wybrano AES (CBC) z kluczem 128-bitowym `00 01 … 0F`. CrypTool nie podaje czasu dla AES, dlatego zmierzono czas od zatwierdzenia klucza do pojawienia się okna z wynikiem; obejmuje on także utworzenie dokumentu, więc jest raczej górnym oszacowaniem.

| Algorytm | Operacja | 1 MB [s] | 2 MB [s] | 5 MB [s] |
| --- | --- | ---: | ---: | ---: |
| RSA-512 | szyfrowanie | 0,403 | 0,799 | 1,977 |
| RSA-512 | deszyfrowanie | 5,261 | 10,500 | 26,184 |
| RSA-1024 | szyfrowanie | 0,688 | 1,391 | 3,392 |
| RSA-1024 | deszyfrowanie | 15,372 | 31,029 | 77,322 |
| RSA-2048 | szyfrowanie | 1,314 | 2,525 | 6,389 |
| RSA-2048 | deszyfrowanie | 57,816 | 100,841 | 252,445 |
| AES-128 (CBC) | szyfrowanie | 0,081 | 0,076 | 0,152 |
| AES-128 (CBC) | deszyfrowanie | 0,334 | 0,574 | 1,668 |

Kryptogram RSA pliku 1 MB miał 1 065 280 B (RSA-512), 1 056 896 B (RSA-1024) i 1 052 928 B (RSA-2048), a AES 1 048 592 B (dopełnienie do pełnego bloku 16 B). Wszystkie pliki odszyfrowane przez AES były identyczne z oryginałami. W RSA, tak jak w 1.3, początek wyniku był zgodny z oryginałem, a na końcu pozostawały zera dopełnienia.

Szyfrowanie RSA korzysta z małego wykładnika publicznego, więc jest wyraźnie szybsze od deszyfrowania wykładnikiem prywatnym `d`, który ma długość zbliżoną do modułu. Pojedyncze pomiary są przybliżone, zwłaszcza dla AES, gdzie czas samego szyfrowania jest porównywalny z narzutem interfejsu.

### 1.6 Przekłamania w kryptogramie

Modyfikowano kryptogramy tekstu wysokiego z 1.3 (bajty numerowane od zera, `m` = długość modułu: 64, 128 albo 256 B). Zmiany wprowadzano w drugim bloku TT, od bajtu `m+10`. Następnie kryptogram odszyfrowano w CrypTool właściwym kluczem. Program w żadnym przypadku nie zgłosił błędu.

| Modyfikacja TT | Długość TT 512 / 1024 / 2048 [B] | Wynik deszyfrowania |
| --- | --- | --- |
| Zmiana 1 bajtu (XOR `0x01` w `C[m+10]`) | 1088 / 1152 / 1280 | tylko drugi blok TJ nieczytelny (63 / 127 / 255 B), reszta poprawna |
| Usunięcie 1 bajtu `C[m+10]` | 1087 / 1151 / 1279 | pierwszy blok poprawny, od drugiego do końca wszystko nieczytelne |
| Usunięcie 30 B od `C[m+10]` | 1058 / 1122 / 1250 | jak wyżej: od drugiego bloku do końca nieczytelne |
| Usunięcie całego bloku `C[m…2m−1]` | 1024 / 1024 / 1024 | drugi blok TJ znika, pozostałe bloki poprawne i czytelne |
| Usunięcie `m` bajtów od `C[m+10]` | 1024 / 1024 / 1024 | drugi blok nieczytelny, trzeci znika, od czwartego tekst poprawny |

Przykład dla RSA-512 po usunięciu `m` bajtów od `C[74]`: `Block ciphers provide confidentiality when used with a unique u` + 63 B śmieci + `rovide confide…`. Po usunięciu całego bloku z RSA-1024 tekst przechodzi bez śmieci z `…Repeated plaintext` do `nd authenticated encryption…`, tj. brakuje dokładnie 127 B TJ.

### Wnioski (pytania 1.7–1.15)

**1.7.** Dla tekstów zróżnicowanych entropia TT wynosiła około 7,7–7,9 bit/B niezależnie od długości klucza. Wyraźna zależność wystąpiła tylko dla tekstu jednorodnego (6,03 → 6,93 → 7,44): TT składa się wtedy z jednego powtarzanego bloku, a dłuższy moduł oznacza dłuższy blok o większej liczbie różnych bajtów. Nie wynika to z większego bezpieczeństwa dłuższego klucza.

**1.8.** Długość klucza wyznacza długość bloku, a więc miejsce pików autokorelacji TT. Dla tekstu jednorodnego piki wystąpiły przy 64, 128 i 256 B. Dla tekstu średniego to, czy blok TJ się powtórzy, zależy od relacji długości bloku i okresu tekstu (pik przy RSA-512 i RSA-2048, brak przy RSA-1024). Dla tekstu wysokiego autokorelacja TT była płaska dla każdego klucza.

**1.9.** Przy dostatecznie zróżnicowanym TJ entropia TT jest wysoka i prawie nie zależy od H(TJ). Gdy TJ zawiera powtarzające się całe bloki, entropia TT jest niższa (tekst jednorodny: 6,0–7,4 bit/B), bo deterministyczne RSA bez losowego dopełnienia zachowuje powtórzenia bloków. Dopełnienie losowe, np. RSA-OAEP, usunęłoby ten efekt.

**1.10.** Czas szyfrowania i deszyfrowania rośnie w przybliżeniu liniowo z długością pliku: 1 → 2 → 5 MB daje około 1 : 2 : 5 (np. deszyfrowanie RSA-1024: 15,4 → 31,0 → 77,3 s). Liczba bloków jest proporcjonalna do długości pliku. Czas rośnie też z długością klucza; najsilniej przy deszyfrowaniu (dla 5 MB: 26 s, 77 s i 252 s).

**1.11.** AES był o rząd lub dwa rzędy wielkości szybszy. Dla 5 MB AES potrzebował około 0,15 s na szyfrowanie i 1,7 s na deszyfrowanie (razem z wyświetleniem wyniku), a RSA-2048 6,4 s i 252 s. Nawet RSA-512 deszyfrował 5 MB przez 26 s.

**1.12.** Zmiana jednego bajtu TT niszczy cały odpowiadający blok TJ (63, 127 albo 255 B), ale nie wpływa na inne bloki. Skala uszkodzenia zależy więc od długości modułu: im dłuższy klucz, tym większy uszkodzony fragment. Usunięcie fragmentu, którego długość nie jest wielokrotnością długości bloku, przesuwa granice bloków i niszczy cały tekst od miejsca zmiany do końca, niezależnie od tego, czy usunięto 1, czy 30 B.

**1.13.** Tak. Jeżeli usunięty fragment ma długość wielokrotności bloku i zaczyna się na granicy bloku, odpowiadający fragment TJ po prostu znika, a reszta pozostaje czytelna. Usunięcie `m` bajtów w środku bloku uszkadza jeden blok, ale dalszy tekst znów jest poprawny. CrypTool nie wykrył żadnej z tych zmian, więc samo szyfrowanie nie chroni integralności; potrzebny jest podpis cyfrowy lub MAC.

**1.14.** Zalety algorytmów asymetrycznych: nie trzeba wcześniej uzgadniać tajnego klucza, klucz publiczny można jawnie rozpowszechniać, a dla `n` uczestników wystarczy `n` par kluczy zamiast osobnego klucza dla każdej pary. Umożliwiają też podpis cyfrowy. Wady: są wielokrotnie wolniejsze, wymagają znacznie dłuższych kluczy, kryptogram jest dłuższy od TJ, a wiarygodność klucza publicznego trzeba potwierdzić (PKI). Algorytmy symetryczne są szybkie i dają krótki kryptogram, ale wymagają bezpiecznej dystrybucji wspólnego klucza.

**1.15.** Asymetrycznych lepiej używać do wymiany lub uzgadniania kluczy (TLS, DH), podpisów cyfrowych, certyfikatów i uwierzytelniania oraz do szyfrowania krótkich danych, np. klucza sesyjnego. Symetrycznych — do szyfrowania dużych ilości danych: plików, dysków, transmisji w VPN i TLS. W praktyce stosuje się schemat hybrydowy, jak `RSA-AES` w CrypTool: RSA szyfruje losowy klucz AES, a AES — właściwe dane.
