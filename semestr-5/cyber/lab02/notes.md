# Cyberbezpieczeństwo laboratorium

2026-10-13

Konrad Guzek grupa 8

## 1. Szyfrowanie historyczne

### Przykład 1

Szyfrowanie Vigenere `ABC` + szyfrowanie Vigenere `DEF` można odwrócić przez odszyfrowanie Vigenere `DFH`.

### Przykład 2

Szyfrowanie Vigenere `ABC` + szyfrowanie Vigenere `DEFG` można odwrócić przez odszyfrowanie Vigenere `DFHGEGFHFEGI`.

### Przykład 3

Szyfrowanie Hill 2x `QDZI` daje ten sam wynik co szyfrowanie Hill 1x `TUCJ` dla tego samego tekstu.

### Właściwości algorytmów

| Algorytm       | Klasa                           | Klucz / przestrzeń kluczy                | Wielokrotne szyfrowanie                    | Słabe klucze i ograniczenia                             | Metoda łamania                             |
| -------------- | ------------------------------- | ---------------------------------------- | ------------------------------------------ | ------------------------------------------------------- | ------------------------------------------ |
| Cezar / ROT-13 | podstawieniowy monoalfabetyczny | 25 nietrywialnych przesunięć             | dwa przesunięcia dają jedno przesunięcie   | `k=0`; ROT-13 zastosowany dwa razy daje tekst jawny     | brute force, histogram                     |
| Vigenère       | podstawieniowy polialfabetyczny | słowo długości `L`, do `26^L` możliwości | daje Vigenère z okresowym kluczem złożonym | klucz `A...A`, klucz jednoliterowy, krótki lub okresowy | Kasiski, IC, autokorelacja, analiza kolumn |
| Playfair       | podstawieniowy digramowy        | kwadrat 5×5 zależny od hasła             | nadal działa na parach liter               | połączenie `I/J`, przewidywalne hasło                   | częstości digramów, hill climbing          |
| Hill           | blokowy, macierzowy             | odwracalna macierz modulo 26             | iloczyn macierzy tworzy nowy klucz         | macierz jednostkowa lub nieodwracalna                   | znany tekst jawny, układ równań mod 26     |
| Permutacja     | transpozycyjny                  | kolejność kolumn / permutacja pozycji    | złożenie jest kolejną permutacją           | krótki, przewidywalny klucz                             | anagramowanie, n-gramy, analiza kolumn     |
| ADFGVX         | podstawienie + transpozycja     | kwadrat 6×6 i klucz transpozycji         | łączy dwie różne operacje                  | słaba konfiguracja klucza lub kwadratu                  | analiza transpozycji i podstawienia        |

### Szyfrowanie wielokrotne

Tekst jawny użyty w przykładach: Bardzo przepraszam, ale niestety nie mowie po polsku.

| Operacja                                               | Wynik / obserwacja                                                                                                        |
| ------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------- |
| Cezar `k=3`, następnie `k=5`                           | `JIZLHWXZHMXZIAHIUITMVQMABMBGVQMUWEQMXWXWTASC`; identyczny z Cezarem `k=8`                                                |
| ROT-13 dwa razy                                        | powrót do tekstu jawnego                                                                                                  |
| Vigenère `ABC`, następnie `DEF`                        | `EFYGEVSWGHUYDXGDRHOJULJZWJABSPHRVZNLSTWRQZNZ`; równoważne pojedynczemu Vigenère z kluczem `DFH`                          |
| Vigenère `ABC`, następnie `DEFG`                       | `EFYJDUUYEIVZDXGGQGQLSMKAWJAEROJTTAOMSTWUPYPB`; równoważne kluczowi `DFHGEGFHFEGI` o okresie 12                           |
| Hill 2×2, `[[3,7],[2,5]]`, następnie `[[7,8],[11,11]]` | `LDMFNZOBHFOBQKPXCKJPXDIWTNFBXDUKGICGHVHVHRSS`; złożenie odpowiada pojedynczej macierzy będącej iloczynem macierzy kluczy |
| Permutacja `KLUCZ` dwa razy                            | `LUNATROZODNOERPAKTZWPEMSEZISPALIRYEISBEPMAOE`; nadal jest tylko permutacją pozycji                                       |

W Cezarze i Hillu złożenie daje ten sam typ szyfru z innym kluczem. W Vigenèrze powstaje dłuższy klucz okresowy. Dwie transpozycje nadal są transpozycją. ADFGVX łączy podstawienie i transpozycję.

### Najsilniejszy z przetestowanych algorytmów

Za najsilniejszy przyjęto ADFGVX: łączy podstawienie i transpozycję, utrudniając analizę częstości i sąsiedztwa liter. Hill daje dyfuzję blokową, ale jest liniowy i podatny na znany tekst jawny. Cezar jest najsłabszy.

## 2. Analiza własności dostępnych algorytmów

### 2.1 Entropia tekstów jawnych

| Język     | Tekst                                                                            | Entropia |
| --------- | -------------------------------------------------------------------------------- | -------: |
| Polski    | Bardzo przepraszam, ale niestety nie mowie po polsku.                            |     3.94 |
| Angielski | I am terribly sorry, but unfortunately, I do not speak English.                  |     4.02 |
| Japoński  | Taihen moshiwake gozaimasen ga, zan ne nagara watashi wa nihongo no hanasemasen. |     3.44 |

Dłuższe próbki:

Do zdań z tabeli dodano poniższe akapity: polski i angielski po 7 razy, japoński 9 razy. Wyniki z punktów 2.2–2.6 dotyczą tych próbek; do szyfrowania użyto polskiej. Powtórzenia wpływają na częstości n-gramów.

- Polski: Kryptografia klasyczna pokazuje, ze czestosc liter ujawnia strukture jezyka. Analiza histogramu, ngramow i indeksu koincydencji pomaga rozpoznac rodzaj szyfru. Dlugi klucz utrudnia analize, lecz powtarzany klucz tworzy okres widoczny w szyfrogramie. Badamy ten sam tekst, aby porownanie algorytmow bylo uczciwe.
- Angielski: Classical cryptography shows that letter frequencies reveal the structure of a language. Histogram, ngram and coincidence analysis help identify the cipher family. A long key makes analysis harder, but a repeated key creates a period visible in the ciphertext. We use the same text so that the comparison of algorithms is fair.
- Japoński: Kotengo no angobunseki dewa moji no shiyou hindo ga juuyou de aru. Hisutoguramu to n guramu wa gengo no tokuchou o shimesu. Nagai kagi wa bunseki o muzukashiku suru ga kurikaesu kagi wa shuuki o nokosu. Onaji tekisuto de angouhou o hikaku suru.

| Język             | Liczba liter | Entropia [bit/znak] |
| ----------------- | -----------: | ------------------: |
| Polski            |         1892 |              4,2927 |
| Angielski         |         1940 |              4,1496 |
| Japoński (romaji) |         1849 |              3,8659 |

Rozkłady liter są różne. Romaji używa mniejszego podzbioru alfabetu.

### 2.2 Entropia tekstu jawnego i szyfrogramów

| Algorytm    | Parametry                                      | Długość wyjścia | Entropia [bit/symbol] |
| ----------- | ---------------------------------------------- | --------------: | --------------------: |
| Tekst jawny | —                                              |            1892 |                4,2927 |
| Cezar       | `k=10`                                         |            1892 |                4,2927 |
| Vigenère    | `DFG`, długość 3                               |            1892 |                4,5526 |
| Vigenère    | `DFGH`, długość 4                              |            1892 |                4,6207 |
| Vigenère    | `KRYPTO`, długość 6                            |            1892 |                4,6255 |
| Hill        | macierz 2×2 `[[3,7],[2,5]]`                    |            1892 |                4,6416 |
| Hill        | macierz 3×3 `[[6,24,1],[13,16,10],[20,17,15]]` |            1893 |                4,6402 |
| Permutacja  | klucz `KLUCZ`                                  |            1892 |                4,2927 |
| ADFGVX      | klucz transpozycji `SZYFR`                     |            3784 |                2,4747 |
| Homofony    | 100 symboli `00–99`                            |    1892 symboli |                6,2929 |

Maksimum: 26 liter — `4,7004`; ADFGVX — `2,5850`; 100 homofonów — `6,6439`. Cezar i permutacja zachowują entropię. Vigenère i Hill ją zwiększają. ADFGVX ma sześć symboli, homofony sto.

ADFGVX: wiersze kwadratu `SZYFRA / BCDEGH / IJKLMN / OPQTUV / WX0123 / 456789`, etykiety `ADFGVX`. Homofony: kolejne kody `00–99` przypisano literom `A–Z` w liczbach `8,2,3,4,10,2,2,6,7,1,1,4,3,7,8,2,1,6,6,7,3,1,2,1,2,1`; kody danej litery wybierano cyklicznie. Hill: wektory kolumnowe, `C=KP mod 26`, dopełnienie `X`.

| Algorytm        | Początek szyfrogramu                  |
| --------------- | ------------------------------------- |
| Cezar           | `LKBNJYZBJOZBKCJKWKVOXSOCDODIXSOW`    |
| Vigenère `DFGH` | `EFXKCTVYCJVYDXFHPFRLQNKZWJZFQNKT`    |
| Hill 2×2        | `DCUXRQILZSILWMXYKYJQROIUHGRCROSQ`    |
| Permutacja      | `DZSLSNWPUTFANAZSLUIUEKLIRGWEODIG`    |
| ADFGVX          | `XADDVAVDAGGFVFDGAFFGVFFADAAADDDG`    |
| Homofony        | `08 00 71 13 99 60 68 72 99 17 69 73` |

### 2.3 Histogramy tekstów jawnych dla trzech języków

| Język           | Sześć najczęstszych liter histogramu             |
| --------------- | ------------------------------------------------ |
| Polski          | `A(207), O(144), Z(136), R(129), E(118), I(115)` |
| Angielski       | `E(256), A(199), T(173), I(144), S(143), R(138)` |
| Japoński romaji | `U(279), O(230), A(186), I(149), N(136), K(136)` |

W próbce angielskiej dominują `E, A, T`, w polskiej `A, O, Z`, w romaji `U, O, A`.

### 2.4 Histogram tekstu jawnego i zaszyfrowanego

| Tekst / algorytm   | Sześć najczęstszych symboli histogramu            |
| ------------------ | ------------------------------------------------- |
| Tekst jawny        | `A(207), O(144), Z(136), R(129), E(118), I(115)`  |
| Cezar `k=10`       | `K(207), Y(144), J(136), B(129), O(118), S(115)`  |
| Vigenère `DFGH`    | `F(144), Y(107), R(100), W(99), G(98), N(93)`     |
| Hill 2×2           | `Z(120), T(105), A(99), I(96), D(93), X(93)`      |
| Permutacja `KLUCZ` | `A(207), O(144), Z(136), R(129), E(118), I(115)`  |
| ADFGVX             | `A(1090), G(679), F(678), D(631), V(385), X(321)` |
| Homofony           | `99(136), 45(78), 97(46), 98(46), 44(35), 94(32)` |

Cezar przesuwa histogram, transpozycja zachowuje go dokładnie. Vigenère i Hill spłaszczają rozkład. ADFGVX zawiera wyłącznie `A,D,F,G,V,X`. W homofonach rozkład zależy od przydziału kodów: tutaj `Z` ma tylko jeden kod (`99`), dlatego nadal występuje wyraźne maksimum.

### 2.5 N-gramy tekstów jawnych w trzech językach

| Język           | Najczęstsze bigramy      | Najczęstsze trigramy        | Najczęstsze 4-gramy  |
| --------------- | ------------------------ | --------------------------- | -------------------- |
| Polski          | `CZ(49), PO(37), AM(36)` | `GRA(28), OGR(21), RAM(21)` | `OGRA(21), GRAM(21)` |
| Angielski       | `TH(56), HE(56), AL(49)` | `THE(35), GRA(21), SIS(21)` | `THEC(21), TOGR(14)` |
| Japoński romaji | `SU(63), HI(56), NG(47)` | `NGO(37), SHI(29), ONO(28)` | `OSHI(19), NGON(19)` |

W angielskim sekwencje `TH`, `HE`, `THE` są bardzo charakterystyczne. Polski zawiera inne częste kombinacje, a w romaji dominują sekwencje związane z sylabami, np. `SHI`. N-gramy pozwalają rozpoznać język i oceniać kandydatów klucza.

### 2.6 N-gramy tekstu jawnego i szyfrogramów

| Algorytm           | Najczęstsze bigramy         | Najczęstsze trigramy         |
| ------------------ | --------------------------- | ---------------------------- |
| Jawny              | `CZ(49), PO(37), AM(36)`    | `GRA(28), OGR(21), RAM(21)`  |
| Cezar `k=10`       | `MJ(49), ZY(37), KW(36)`    | `QBK(28), YQB(21), BKW(21)`  |
| Vigenère `DFGH`    | `QN(23), RB(22), WW(21)`    | `WTM(14), TMY(14), MYD(14)`  |
| Hill 2×2           | `JO(28), ZZ(28), RO(23)`    | `DXW(21), JOE(21), ZEH(14)`  |
| Permutacja `KLUCZ` | `AZ(42), NA(28), OI(28)`    | `ISA(14), AIS(14), ZSL(8)`   |
| ADFGVX             | `AA(345), AF(200), GA(194)` | `AAA(133), ADA(68), GAA(64)` |
| Homofony           | `10-99(21), 11-99(21)`      | `11-99-68(7), 11-99-12(7)`   |

Cezar zachowuje liczności n-gramów, ale przesuwa litery. Transpozycja zachowuje pojedyncze litery, niszcząc lokalne n-gramy języka. Vigenère i Hill redukują powtarzalność rozpoznawalnych sekwencji. W ADFGVX n-gramy wynikają przede wszystkim z małego alfabetu sześciu znaków, a homofony dzielą częstość jednej litery pomiędzy wiele kodów.

### 2.7 Autokorelacja XOR i Vigenère

Liczby w tabelach oznaczają liczbę zgodnych znaków przy danym przesunięciu.

Tekst wejściowy: odszyfrowany angielski tekst o Enigmie z części 3 (1088 liter). XOR wykonano na bajtach ASCII z powtarzanym hasłem.

| Szyfr i klucz       |   1 |   2 |      3 |   4 |      5 |   6 |   7 |      8 |
| ------------------- | --: | --: | -----: | --: | -----: | --: | --: | -----: |
| Vigenère `DFG`      |  37 |  48 | **67** |  31 |     35 |  63 |  40 |     36 |
| Vigenère `SZYFR`    |  44 |  30 |     43 |  52 | **80** |  37 |  42 |     38 |
| Vigenère `KRYPTOGR` |  43 |  39 |     40 |  48 |     24 |  51 |  33 | **62** |
| XOR `ABC`           |  42 |  32 | **67** |  42 |     35 |  63 |  28 |     24 |
| XOR `KLUCZ`         |  32 |  16 |     30 |  30 | **80** |  25 |  29 |     21 |
| XOR `HASLOXYZ`      |  41 |  33 |     22 |  33 |     31 |  31 |  37 | **62** |

| Szyfr i klucz       |   9 |     10 |  11 |  12 |  13 |  14 |     15 |     16 |
| ------------------- | --: | -----: | --: | --: | --: | --: | -----: | -----: |
| Vigenère `DFG`      |  66 |     40 |  44 |  58 |  33 |  40 |     66 |     42 |
| Vigenère `SZYFR`    |  30 | **84** |  33 |  39 |  45 |  26 | **66** |     37 |
| Vigenère `KRYPTOGR` |  56 |     43 |  29 |  41 |  33 |  32 |     42 | **60** |
| XOR `ABC`           |  66 |     24 |  31 |  58 |  35 |  32 |     66 |     28 |
| XOR `KLUCZ`         |  39 | **84** |  28 |  24 |  22 |  29 | **66** |     33 |
| XOR `HASLOXYZ`      |  29 |     29 |  35 |  35 |  26 |  38 |     44 | **60** |

Piki przy długości hasła i jej wielokrotnościach wynikają z powtarzania tego samego klucza. Im dłuższe hasło w stosunku do tekstu, tym trudniej odróżnić piki od przypadkowych lokalnych maksimów.

### 2.8 Zmiana obserwowanych parametrów

- Entropia nie zmienia się dla Cezara i transpozycji, rośnie dla Vigenère’a i Hilla, jest ograniczona alfabetem ADFGVX, a dla homofonów jest wyższa dzięki większej liczbie symboli.
- Histogram Cezara jest przesunięty, histogram transpozycji identyczny z jawnym, natomiast Vigenère i Hill go spłaszczają.
- Cezar zachowuje liczności n-gramów; transpozycja niszczy ich sąsiedztwo; szyfry wieloalfabetyczne i blokowe osłabiają ich przydatność.
- Autokorelacja ujawnia okres klucza powtarzanego w Vigenèrze i XOR.

### 2.9 Rozpoznawanie algorytmu na podstawie szyfrogramu

1. Sprawdzić alfabet wyjściowy: tylko `ADFGVX` jest silną wskazówką ADFGVX, a liczne kody liczbowe wskazują homofony.
2. Porównać histogram i IC z językiem naturalnym: podobny rozkład sugeruje podstawienie monoalfabetyczne albo transpozycję.
3. Jeżeli histogram jest przesuniętą wersją języka, przetestować wszystkie 25 przesunięć Cezara.
4. Jeżeli częstości liter są zachowane, lecz n-gramy zostały zniszczone, rozważyć transpozycję.
5. Dla spłaszczonego histogramu sprawdzić autokorelację i okresowość; okres wskazuje Vigenère lub XOR z powtarzanym kluczem.
6. Gdy brak czytelnego okresu, a tekst ma strukturę bloków, rozważyć Hill lub inny szyfr blokowy.

### 2.10 Ustalanie hasła

Autokorelacja, test Kasiskiego i indeks koincydencji służą najpierw do wyznaczenia długości klucza. Dla Vigenère’a szyfrogram dzieli się następnie na kolumny o tym okresie; każda kolumna jest szyfrem Cezara i można znaleźć jej przesunięcie analizą częstości. Dla Cezara wystarczy dopasować przesunięcie histogramu. W podstawieniu monoalfabetycznym wykorzystuje się zgodność pojedynczych liter i n-gramów, a dla Hilla istotny jest znany tekst jawny pozwalający odtworzyć macierz.

## 3. Analiza dostarczonych plików

Trzy pliki tekstowe zawierają po 1347 znaków i szyfrują ten sam angielski tekst o maszynie Enigma.

### 3.1 Rozpoznanie algorytmów

#### Pierwszy plik tekstowy

Początek szyfrogramu: `Usy Ifsenl geurgop qek k djpfh mxgu fmiv`.

- IC wynosi około `0,041`, czyli jest bliski wartości dla rozkładu losowego i wyraźnie niższy od angielskiego.
- Histogram jest spłaszczony.
- Autokorelacja ma piki dla przesunięć `7` i `14`.
- Podział na 7 kolumn daje IC bliski angielskiemu.

Wynik: **Vigenère z hasłem `BLUESKY`** (długość 7). Odszyfrowany początek: `The Enigma machine was a field unit used in World War II by German field agents to encrypt and decrypt messages and communications.`

#### Drugi plik tekstowy

Początek szyfrogramu: `Znk Ktomsg sginotk cgy g lokrj atoz aykj`.

- IC wynosi około `0,069`, co jest typowe dla tekstu angielskiego po podstawieniu monoalfabetycznym.
- Najczęstsze litery zachowują układ histogramu języka, lecz są przesunięte.
- Dopasowanie `Znk → The` daje stałe przesunięcie 6.

Wynik: **Cezar `k=6`**. Odszyfrowany początek: `The Enigma machine was a field unit used in World War II by German field agents to encrypt and decrypt messages and communications.`

#### Trzeci plik tekstowy

Początek szyfrogramu: `Obt Ticahq hqebcit uqn q yctgr pico pntr`.

- IC jest taki sam jak w drugim pliku tekstowym, więc rozkład pojedynczych liter został zachowany.
- Przesunięcie nie jest stałe: różne litery wymagają różnych przesunięć.
- Dopasowania `Obt → The` i `qir → and` wskazują podstawienie monoalfabetyczne.

Wynik: **szyfr podstawieniowy** z alfabetem klucza:

```text
tekst jawny: ABCDEFGHIJKLMNOPQRSTUVWXYZ
szyfrogram:  QWERTYABCDFGHIJKLMNOPSUVXZ
```

Odszyfrowany początek: `The Enigma machine was a field unit used in World War II by German field agents to encrypt and decrypt messages and communications.`

### 3.4 Od czego zależy siła algorytmu?

Siła zależy od przestrzeni kluczy, jakości i długości klucza, zdolności ukrywania histogramu i n-gramów tekstu jawnego, braku prostego okresu oraz odporności na ataki ze znanym tekstem jawnym. Ważna jest także dyfuzja: pojedyncza zmiana tekstu jawnego powinna wpływać na wiele znaków szyfrogramu.

### 3.5 Jak zwiększyć siłę znanych szyfrów?

Można używać dłuższych, losowych kluczy, unikać kluczy okresowych i słabych, zwiększać wielkość bloków, łączyć podstawienie z transpozycją oraz usuwać spacje i interpunkcję. Vigenère z prawdziwie losowym kluczem długości tekstu staje się szyfrem Vernama (one-time pad), ale wymaga bezpiecznego przekazania i jednorazowego użycia klucza.
