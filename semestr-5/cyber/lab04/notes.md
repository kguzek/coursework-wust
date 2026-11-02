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

Klucz publiczny to para `(N,e)`, a prywatny zawiera `d`. Wykładnik `e` musi być względnie pierwszy z `φ(N)`, czyli `NWD(e,φ(N))=1`. Przy tak małym `N` każdy może rozłożyć 3233 na 61 × 53 i od razu policzyć `d`, dlatego w praktyce stosuje się moduły długości co najmniej 2048 bitów.

### 1.2 Generowanie kluczy

Wybrano `Digital Signatures/PKI/PKI/Generate/Import Keys`, algorytm RSA i kolejno trzy długości modułu. Dla każdej pary CrypTool potwierdził utworzenie i zapisanie kluczy w magazynie chronionym testowym PIN-em.

| Długość modułu | Identyfikator | Czas generowania pary [s] |
| --- | --- | ---: |
| 512 bitów | `Lab04-RSA-512` | 0,024 |
| 1024 bity | `Lab04-RSA-1024` | 0,176 |
| 2048 bitów | `Lab04-RSA-2048` | 1,224 |

Generowanie wyraźnie wydłuża się wraz z długością klucza: para 2048-bitowa powstawała ok. 50 razy dłużej niż 512-bitowa. To czas samego generowania kluczy, szyfrowanie mierzono osobno w 1.4.

### 1.3 Entropia i autokorelacja

Użyto tych samych tekstów jawnych co w laboratorium 3 (po 1024 B ASCII) oraz kluczy z punktu 1.2. Teksty zaszyfrowano opcją `RSA Encryption`, a kryptogramy zapisano jako pliki binarne.

| TJ | Konstrukcja | H(TJ) [bit/B] |
| --- | --- | ---: |
| Jednorodny | `H` × 1024 | 0,00 |
| Średni | powtarzane `agree all use city with model ` (okres 30 B) | 3,77 |
| Wysoki | powtarzany angielski akapit o szyfrach blokowych (okres 174 B) | 4,23 |

Początek tekstu wysokiego: `Block ciphers provide confidentiality when used with a unique unpredictable IV and authenticated encryption. Repeated plaintext should not reveal repeated ciphertext blocks.`

CrypTool dzieli TJ na bloki o jeden bajt krótsze od modułu (63, 127 albo 255 B), a każdy z nich szyfruje do bloku o długości modułu. Ostatni blok jest dopełniany zerami, stąd kryptogramy mają 1088, 1152 i 1280 B, czyli więcej niż TJ.

| TJ | H(TT) RSA-512 | H(TT) RSA-1024 | H(TT) RSA-2048 |
| --- | ---: | ---: | ---: |
| Jednorodny | 6,03 | 6,93 | 7,44 |
| Średni | 7,66 | 7,83 | 7,69 |
| Wysoki | 7,82 | 7,82 | 7,86 |

| Kryptogram | Pierwsze 16 B TT (hex) |
| --- | --- |
| Jednorodny, RSA-512 | `8ba32aa0245817b5b472bfcbc4e25215` |
| Jednorodny, RSA-1024 | `4a0df522d38252e258ae81d3d10491b3` |
| Jednorodny, RSA-2048 | `ab6baa5ff78de70841c24de6ca9797b4` |
| Średni, RSA-1024 | `3ae56143f6013e772e9780ddbdeede00` |
| Wysoki, RSA-2048 | `3fbf5180c642a184eea328615f69a609` |

W kryptogramie tekstu jednorodnego ten sam blok powtarza się przez cały plik i dopiero końcówka wygląda inaczej. Opcja `RSA Encryption` szyfruje bez losowego dopełnienia, więc identyczne bloki TJ dają identyczne bloki TT. W tekście średnim powtórzenia bloków pojawiły się przy RSA-512 i RSA-2048, gdzie okres tekstu dobrze pasuje do długości bloku, natomiast przy RSA-1024 wszystkie bloki były różne.

Autokorelacja TJ zachowuje się zgodnie z oczekiwaniami. Dla tekstu jednorodnego jest maksymalna przy każdym przesunięciu, dla średniego ma piki co 30 B, a dla wysokiego co 174 B. W TT tych okresów już nie widać. Pojawia się za to pik przy przesunięciu równym długości bloku (64, 128 i 256 B) dla tekstu jednorodnego oraz słabsze piki dla tekstu średniego przy RSA-512 i RSA-2048. Dla tekstu średniego z RSA-1024 i dla tekstu wysokiego wykres autokorelacji TT jest płaski.

Każdy kryptogram odszyfrowano tym samym kluczem i tekst się zgadzał, tyle że na końcu pliku zostały zera z dopełnienia ostatniego bloku. CrypTool ich nie usuwa.

### 1.4 i 1.5 Czas szyfrowania i deszyfrowania

Pliki 1, 2 i 5 MB powstały przez powtarzanie akapitu z tekstu wysokiego. Dla RSA zaznaczono `Display encryption time` i `Display decryption time` i zapisano czas podany przez CrypTool. Jako szyfr symetryczny wybrano AES (CBC) z kluczem 128-bitowym `00 01 … 0F`. CrypTool nie wyświetla czasu dla AES, więc mierzono go stoperem od zatwierdzenia klucza do pojawienia się wyniku i podane wartości są tylko orientacyjne.

| Algorytm | Operacja | 1 MB [s] | 2 MB [s] | 5 MB [s] |
| --- | --- | ---: | ---: | ---: |
| RSA-512 | szyfrowanie | 0,403 | 0,799 | 1,977 |
| RSA-512 | deszyfrowanie | 5,261 | 10,500 | 26,184 |
| RSA-1024 | szyfrowanie | 0,688 | 1,391 | 3,392 |
| RSA-1024 | deszyfrowanie | 15,372 | 31,029 | 77,322 |
| RSA-2048 | szyfrowanie | 1,314 | 2,525 | 6,389 |
| RSA-2048 | deszyfrowanie | 57,816 | 100,841 | 252,445 |
| AES-128 (CBC) | szyfrowanie | < 0,5 | < 0,5 | < 0,5 |
| AES-128 (CBC) | deszyfrowanie | < 0,5 | ok. 0,5 | ok. 1,5 |

Pliki odszyfrowane AES były identyczne z oryginałami, a przy RSA, podobnie jak w 1.3, na końcu zostawały zera dopełnienia.

Deszyfrowanie RSA trwało wielokrotnie dłużej niż szyfrowanie. Wynika to z tego, że wykładnik publiczny jest mały, a prywatny `d` ma długość zbliżoną do modułu.

### 1.6 Przekłamania w kryptogramie

Zmieniano kryptogramy tekstu wysokiego z 1.3 w edytorze hex, każdą modyfikację osobno dla RSA-512, RSA-1024 i RSA-2048. Wszystkie zmiany dotyczyły drugiego bloku TT, ok. 10 bajtów od jego początku (oprócz usunięcia całego bloku). Potem kryptogram odszyfrowano w CrypTool właściwym kluczem. Program ani razu nie zgłosił błędu.

| Modyfikacja TT | Wynik deszyfrowania |
| --- | --- |
| Zmiana wartości 1 bajtu | nieczytelny tylko drugi blok TJ (63 / 127 / 255 B), reszta poprawna |
| Usunięcie 1 bajtu | pierwszy blok poprawny, od drugiego do końca wszystko nieczytelne |
| Usunięcie 30 B | tak samo: od drugiego bloku do końca nieczytelne |
| Usunięcie całego drugiego bloku | drugi blok TJ znika, pozostałe bloki poprawne |
| Usunięcie fragmentu o długości modułu ze środka bloku | drugi blok nieczytelny, trzeci znika, od czwartego tekst poprawny |

Przykład dla RSA-512 po usunięciu 64 B ze środka drugiego bloku: `Block ciphers provide confidentiality when used with a unique u`, potem 63 B śmieci i dalej `rovide confide...`. Po usunięciu całego bloku z kryptogramu RSA-1024 tekst przechodzi bez żadnych śmieci z `...Repeated plaintext` do `nd authenticated encryption...`.

### Wnioski (pytania 1.7 do 1.15)

**1.7.** Dla tekstów zróżnicowanych entropia TT wynosiła ok. 7,7–7,9 bit/B i długość klucza praktycznie nie miała znaczenia. Wyraźną różnicę widać tylko przy tekście jednorodnym (6,03, 6,93 i 7,44), bo TT składa się wtedy z jednego powtarzanego bloku, a dłuższy blok zawiera więcej różnych bajtów.

**1.8.** Długość klucza wyznacza długość bloku, a więc miejsca, w których mogą wystąpić piki autokorelacji TT. Dla tekstu jednorodnego piki były przy 64, 128 i 256 B. Dla tekstu średniego zależało to od tego, czy długość bloku pasuje do okresu tekstu: pik wystąpił przy RSA-512 i RSA-2048, a przy RSA-1024 go nie było. Tekst wysoki dał płaską autokorelację TT przy każdym kluczu.

**1.9.** Jeśli TJ jest wystarczająco zróżnicowany, entropia TT jest wysoka i prawie nie zależy od H(TJ). Kiedy w TJ powtarzają się całe bloki, entropia TT spada (tekst jednorodny: 6,0–7,4 bit/B), bo RSA bez losowego dopełnienia szyfruje takie bloki identycznie.

**1.10.** Czas rośnie mniej więcej liniowo z rozmiarem pliku, np. deszyfrowanie RSA-1024 trwało 15,4 s, 31,0 s i 77,3 s dla 1, 2 i 5 MB. Rośnie też z długością klucza, najmocniej przy deszyfrowaniu (dla 5 MB: 26 s, 77 s i 252 s).

**1.11.** AES był szybszy o jeden lub dwa rzędy wielkości. Plik 5 MB AES zaszyfrował i odszyfrował w czasie poniżej 2 s, podczas gdy RSA-2048 potrzebował 6,4 s na szyfrowanie i ponad 4 minuty na deszyfrowanie. Nawet RSA-512 deszyfrował ten plik przez 26 s.

**1.12.** Zmiana jednego bajtu TT psuje cały odpowiadający mu blok TJ (63, 127 albo 255 B), a pozostałe bloki są w porządku, więc im dłuższy klucz, tym większy zepsuty fragment. Usunięcie bajtów w liczbie niebędącej wielokrotnością bloku przesuwa granice bloków i cały tekst od miejsca zmiany do końca staje się nieczytelny, niezależnie od tego, czy usunięto 1 B, czy 30 B.

**1.13.** Tak. Jeśli usunięty fragment ma długość będącą wielokrotnością bloku i zaczyna się na granicy bloku, odpowiedni kawałek TJ po prostu znika, a reszta jest czytelna. Usunięcie fragmentu o długości modułu ze środka bloku psuje jeden blok, ale dalej tekst jest znowu poprawny. CrypTool w żadnym z tych przypadków nie wykrył, że kryptogram był zmieniany.

**1.14.** Zalety algorytmów asymetrycznych: nie trzeba wcześniej uzgadniać tajnego klucza, klucz publiczny można udostępnić każdemu, a przy `n` uczestnikach wystarczy `n` par kluczy zamiast osobnego klucza dla każdej pary osób. Pozwalają też na podpis cyfrowy. Wady: są dużo wolniejsze, potrzebują znacznie dłuższych kluczy, kryptogram jest dłuższy od TJ, a autentyczność klucza publicznego trzeba jakoś potwierdzić (PKI). Algorytmy symetryczne są szybkie i dają kryptogram prawie tej samej długości co TJ, ale wymagają bezpiecznego przekazania wspólnego klucza.

**1.15.** Algorytmy asymetryczne stosuje się do wymiany lub uzgadniania kluczy (np. DH w TLS), podpisów cyfrowych, certyfikatów i uwierzytelniania, a także do szyfrowania krótkich danych, takich jak klucz sesyjny, który RSA może zaszyfrować dla AES (tak działa `RSA-AES` w CrypTool). Symetryczne lepiej nadają się do szyfrowania dużych ilości danych: plików, dysków czy ruchu w VPN i TLS.
