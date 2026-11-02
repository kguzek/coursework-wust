# Cyberbezpieczeństwo laboratorium

2026-10-27

Konrad Guzek grupa 8

## 1. Algorytmy asymetryczne

### 1.1 Demonstracja RSA

W CrypTool 1.4.42 wybrano `Encrypt/Decrypt/Asymmetric/RSA Demonstration`. Do demonstracji użyto małych liczb, żeby można było łatwo sprawdzić obliczenia.


| Parametr | Wartość |
| --- | ---: |
| Liczba pierwsza `p` | 61 |
| Liczba pierwsza `q` | 53 |
| Moduł `N=pq` | 3233 |
| `φ(N)=(p-1)(q-1)` | 3120 |
| Wykładnik publiczny `e` | 17 |
| Wykładnik prywatny `d` | 2753 |

Po wybraniu `Update parameters` program obliczył `N`, `φ(N)` i `d`. Dla wejścia liczbowego `M=65` szyfrowanie dało `C=2790`. Następnie wpisano `2790` jako wejście do deszyfrowania: wynik wynosił `0065`, a odpowiadający mu znak to `A`. Początkowa wartość została więc odzyskana.

```text
C = 65^17 mod 3233 = 2790
M = 2790^2753 mod 3233 = 65
17 × 2753 mod 3120 = 1
```

Klucz publiczny to para `(N,e)`, a prywatny zawiera `d`. Wykładnik `e` musi być względnie pierwszy z `φ(N)`, czyli `NWD(e,φ(N))=1`. Samo to, że `e` nie dzieli `φ(N)`, nie wystarcza. Tak małe liczby nadają się tylko do pokazania, jak działa RSA, a nie do prawdziwego szyfrowania.

### 1.2 Generowanie kluczy

Wybrano `Digital Signatures/PKI/PKI/Generate/Import Keys`, algorytm RSA i kolejno trzy długości modułu. Dla każdej pary CrypTool potwierdził utworzenie i zapisanie kluczy w magazynie chronionym testowym PIN-em.

| Długość modułu | Identyfikator | Czas generowania pary [s] |
| --- | --- | ---: |
| 512 bitów | `Lab04-RSA-512` | 0,024 |
| 1024 bity | `Lab04-RSA-1024` | 0,176 |
| 2048 bitów | `Lab04-RSA-2048` | 1,224 |

Im dłuższy klucz, tym dłużej trwało generowanie. Są to pojedyncze pomiary czasu **generowania kluczy**, a nie szyfrowania czy deszyfrowania pliku. RSA-512 i RSA-1024 użyto tylko dlatego, że wymaga tego instrukcja. Do prawdziwych zastosowań są już za słabe.

### 1.3 Entropia i autokorelacja

Użyto tych samych tekstów jawnych co w laboratorium 3 (po 1024 B ASCII, bez znaku nowej linii na końcu) oraz kluczy `Lab04-RSA-512`, `Lab04-RSA-1024` i `Lab04-RSA-2048` z punktu 1.2. Wybrano zwykłe `RSA Encryption`, a nie wariant hybrydowy RSA-AES. Kryptogramy zapisano jako pliki binarne. Entropię i autokorelację policzono z zapisanych bajtów, dla alfabetu 256 wartości.

| TJ | Konstrukcja | H(TJ) [bit/B] |
| --- | --- | ---: |
| Jednorodny | `H` × 1024 | 0,0000 |
| Średni | powtarzane `agree all use city with model ` (okres 30 B) | 3,7662 |
| Wysoki | powtarzany angielski akapit o szyfrach blokowych (okres 174 B) | 4,2337 |

Początek tekstu wysokiego: `Block ciphers provide confidentiality when used with a unique unpredictable IV and authenticated encryption. Repeated plaintext should not reveal repeated ciphertext blocks.`

CrypTool dzieli TJ na bloki o jeden bajt krótsze od modułu (63, 127 albo 255 B). Każdy taki blok daje blok TT o długości modułu (64, 128 albo 256 B), a ostatni blok TJ jest dopełniany zerami. Dlatego TT ma 17 × 64 = 1088 B, 9 × 128 = 1152 B albo 5 × 256 = 1280 B.

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
| Średni, RSA-1024 | `3ae56143f6013e772e9780ddbdeede00` |
| Wysoki, RSA-2048 | `3fbf5180c642a184eea328615f69a609` |

W tekście jednorodnym wszystkie pełne bloki TT są takie same, różni się tylko ostatni, dopełniony zerami. Ta opcja programu szyfruje deterministycznie, bez losowego dopełnienia, więc identyczne bloki TJ dają identyczne bloki TT. Podobnie jest w tekście średnim. Przy blokach 63 B wzorzec o okresie 30 B wraca co 10 bloków (630 = 21 × 30), a przy blokach 255 B co 2 bloki (510 = 17 × 30). Przy blokach 127 B powtórzenie pojawiłoby się dopiero po 30 blokach, czyli poza próbką. Wynik około 7,8 bit/B jest typowy dla losowych danych tej długości. Przy próbce około 1 KB nie da się dojść do 8,0.

Autokorelację policzono jako liczbę równych bajtów przy danym przesunięciu, bez zawijania końca pliku.

| Próbka | Przesunięcie [B] | Zgodne / porównane | Pozostałe przesunięcia |
| --- | ---: | ---: | --- |
| TJ jednorodny | dowolne `k` | `1024-k` / `1024-k` | wszystkie bajty zgodne |
| TJ średni | 30 | 994 / 994 | pik co 30 B |
| TJ wysoki | 174 | 850 / 850 | pik co 174 B |
| TT jednorodny, RSA-512 | 64 | 961 / 1024 | najwyżej 17 dla przesunięć od 1 do 63 |
| TT jednorodny, RSA-1024 | 128 | 896 / 1024 | najwyżej 23 dla przesunięć od 1 do 127 |
| TT jednorodny, RSA-2048 | 256 | 769 / 1024 | najwyżej 17 dla przesunięć od 1 do 255 |
| TT średni, RSA-512 | 640 | 384 / 448 | brak piku przy 30 B |
| TT średni, RSA-1024 | brak | brak | brak piku, najwyżej 11 |
| TT średni, RSA-2048 | 512 | 513 / 768 | brak piku przy 30 B |
| TT wysoki, każdy klucz | brak | brak | brak piku, najwyżej 10 |

Okres TJ nie przechodzi wprost do TT. Piki autokorelacji TT pojawiają się tylko przy wielokrotnościach długości bloku i tylko wtedy, gdy powtarzają się całe bloki TJ.

Każdy kryptogram odszyfrowano tym samym kluczem. We wszystkich 9 przypadkach pierwsze 1024 B wyniku zgadzały się z TJ, ale cały wynik miał 1071, 1143 albo 1275 B (17 × 63, 9 × 127, 5 × 255). Program nie usuwa zer dopełnienia, więc żeby odzyskać dokładnie ten sam plik, trzeba znać jego pierwotną długość. Obcięcie wszystkich zer z końca mogłoby usunąć też prawdziwe dane.

### 1.4 i 1.5 Czas szyfrowania i deszyfrowania

Pliki 1, 2 i 5 MB (1 048 576, 2 097 152 i 5 242 880 B) zawierały powtarzany akapit z tekstu wysokiego. Dla RSA zaznaczono `Display encryption time` i `Display decryption time` i zapisano czas podany przez CrypTool. Jako szyfr symetryczny wybrano AES (CBC) z kluczem 128-bitowym `00 01 … 0F`. Dla AES program nie pokazuje czasu, więc zmierzono go od zatwierdzenia klucza do pojawienia się okna z wynikiem. Ten czas obejmuje też utworzenie dokumentu, więc jest raczej zawyżony.

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

Kryptogram pliku 1 MB miał 1 065 280 B dla RSA-512, 1 056 896 B dla RSA-1024 i 1 052 928 B dla RSA-2048. Dla AES było to 1 048 592 B, czyli plik dopełniony do pełnego bloku 16 B. Pliki odszyfrowane AES były identyczne z oryginałami. Przy RSA, tak jak w 1.3, początek wyniku zgadzał się z oryginałem, a na końcu zostawały zera dopełnienia.

Szyfrowanie RSA używa małego wykładnika publicznego, dlatego jest dużo szybsze od deszyfrowania, w którym wykładnik prywatny `d` ma długość zbliżoną do modułu. Każdą operację zmierzono raz, więc wyniki są przybliżone. Dotyczy to szczególnie AES, gdzie samo szyfrowanie trwa mniej więcej tyle, co obsługa okien programu.

### 1.6 Przekłamania w kryptogramie

Zmieniano kryptogramy tekstu wysokiego z 1.3. Bajty są numerowane od zera, a `m` oznacza długość modułu w bajtach (64, 128 albo 256). Zmiany wprowadzano w drugim bloku TT, od bajtu `m+10`. Potem kryptogram odszyfrowano w CrypTool właściwym kluczem. Program ani razu nie zgłosił błędu.

| Modyfikacja TT | Długość TT 512 / 1024 / 2048 [B] | Wynik deszyfrowania |
| --- | --- | --- |
| Zmiana 1 bajtu (XOR `0x01` w `C[m+10]`) | 1088 / 1152 / 1280 | nieczytelny tylko drugi blok TJ (63 / 127 / 255 B), reszta poprawna |
| Usunięcie 1 bajtu `C[m+10]` | 1087 / 1151 / 1279 | pierwszy blok poprawny, od drugiego do końca wszystko nieczytelne |
| Usunięcie 30 B od `C[m+10]` | 1058 / 1122 / 1250 | tak samo: od drugiego bloku do końca nieczytelne |
| Usunięcie całego drugiego bloku `C[m]` do `C[2m-1]` | 1024 / 1024 / 1024 | drugi blok TJ znika, pozostałe bloki poprawne |
| Usunięcie `m` bajtów od `C[m+10]` | 1024 / 1024 / 1024 | drugi blok nieczytelny, trzeci znika, od czwartego tekst poprawny |

Przykład dla RSA-512 po usunięciu `m` bajtów od `C[74]`: `Block ciphers provide confidentiality when used with a unique u`, potem 63 B śmieci i dalej `rovide confide...`. Po usunięciu całego bloku z kryptogramu RSA-1024 tekst przechodzi bez żadnych śmieci z `...Repeated plaintext` do `nd authenticated encryption...`. Brakuje dokładnie 127 B TJ.

### Wnioski (pytania 1.7 do 1.15)

**1.7.** Dla tekstów zróżnicowanych entropia TT wynosiła około 7,7 do 7,9 bit/B, niezależnie od długości klucza. Wyraźną różnicę widać tylko przy tekście jednorodnym (6,03, 6,93 i 7,44). TT składa się wtedy z jednego powtarzanego bloku, a przy dłuższym module ten blok jest dłuższy i ma więcej różnych bajtów. Nie oznacza to, że dłuższy klucz lepiej ukrywa tekst.

**1.8.** Długość klucza wyznacza długość bloku, a więc miejsca, w których mogą wystąpić piki autokorelacji TT. Dla tekstu jednorodnego piki były przy 64, 128 i 256 B. Dla tekstu średniego zależało to od tego, czy długość bloku pasuje do okresu tekstu: pik wystąpił przy RSA-512 i RSA-2048, a przy RSA-1024 go nie było. Dla tekstu wysokiego autokorelacja TT była płaska przy każdym kluczu.

**1.9.** Jeśli TJ jest wystarczająco zróżnicowany, entropia TT jest wysoka i prawie nie zależy od H(TJ). Gdy w TJ powtarzają się całe bloki, entropia TT spada (tekst jednorodny: od 6,0 do 7,4 bit/B), bo RSA bez losowego dopełnienia szyfruje te bloki tak samo. Losowe dopełnienie, np. RSA-OAEP, usunęłoby ten efekt.

**1.10.** Czas rośnie mniej więcej liniowo z długością pliku, bo liczba bloków jest do niej proporcjonalna. Dla 1, 2 i 5 MB czasy mają się do siebie w przybliżeniu jak 1 : 2 : 5, np. deszyfrowanie RSA-1024 trwało 15,4 s, 31,0 s i 77,3 s. Czas rośnie też z długością klucza, najmocniej przy deszyfrowaniu (dla 5 MB: 26 s, 77 s i 252 s).

**1.11.** AES był szybszy o jeden lub dwa rzędy wielkości. Dla 5 MB AES potrzebował około 0,15 s na szyfrowanie i 1,7 s na deszyfrowanie, razem z wyświetleniem wyniku. RSA-2048 potrzebował na to samo 6,4 s i 252 s, a nawet RSA-512 deszyfrował ten plik przez 26 s.

**1.12.** Zmiana jednego bajtu TT psuje cały odpowiadający mu blok TJ (63, 127 albo 255 B), ale inne bloki zostają nienaruszone. Skala uszkodzenia zależy więc od długości modułu: im dłuższy klucz, tym większy zepsuty fragment. Usunięcie fragmentu, którego długość nie jest wielokrotnością bloku, przesuwa granice bloków. Wtedy cały tekst od miejsca zmiany do końca jest nieczytelny, bez względu na to, czy usunięto 1 B, czy 30 B.

**1.13.** Tak. Jeśli usunięty fragment ma długość będącą wielokrotnością bloku i zaczyna się na granicy bloku, odpowiedni kawałek TJ po prostu znika, a reszta jest czytelna. Usunięcie `m` bajtów ze środka bloku psuje jeden blok, ale dalej tekst jest znowu poprawny. CrypTool nie zauważył żadnej z tych zmian, więc samo szyfrowanie nie chroni integralności danych. Do tego potrzebny jest podpis cyfrowy albo MAC.

**1.14.** Zalety algorytmów asymetrycznych: nie trzeba wcześniej uzgadniać tajnego klucza, klucz publiczny można udostępnić każdemu, a przy `n` uczestnikach wystarczy `n` par kluczy zamiast osobnego klucza dla każdej pary osób. Pozwalają też na podpis cyfrowy. Wady: są dużo wolniejsze, potrzebują znacznie dłuższych kluczy, kryptogram jest dłuższy od TJ, a autentyczność klucza publicznego trzeba jakoś potwierdzić (PKI). Algorytmy symetryczne są szybkie i dają kryptogram prawie tej samej długości co TJ, ale wymagają bezpiecznego przekazania wspólnego klucza.

**1.15.** Algorytmy asymetryczne sprawdzają się przy wymianie lub uzgadnianiu kluczy (TLS, DH), podpisach cyfrowych, certyfikatach, uwierzytelnianiu i szyfrowaniu krótkich danych, np. klucza sesyjnego. Symetryczne lepiej nadają się do szyfrowania dużych ilości danych: plików, dysków, ruchu w VPN i TLS. W praktyce łączy się oba podejścia, tak jak w `RSA-AES` w CrypTool. RSA szyfruje losowy klucz AES, a AES szyfruje właściwe dane.
