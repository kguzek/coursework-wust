# Cyberbezpieczeństwo laboratorium

2026-10-20

Konrad Guzek grupa 8

## 1. Algorytmy blokowe

### 1.1 Teksty jawne

| Tekst (1024 B UTF-8) | Konstrukcja | Entropia TJ [bit/B] |
| --- | --- | ---: |
| Jednorodny | `H` × 1024 | 0,0000 |
| Średni | powtarzane `agree all use city with model ` | 3,7662 |
| Wysoki | angielski akapit o szyfrach blokowych | 4,2337 |

Do porównania wybrano AES z blokiem 128-bitowym i 3DES, który korzysta z bloków 64-bitowych. Są to dość różne algorytmy, chociaż oba służą do tego samego typu szyfrowania. 3DES jest już raczej rozwiązaniem historycznym.

### 1.2 Entropia po szyfrowaniu

AES i 3DES badano w trybie CBC. Dla AES-128 A użyto klucza `00 01 … 0f`, a dla AES-128 B `10 11 … 1f`. Klucze AES-192 i AES-256 miały odpowiednio 24 i 32 kolejne bajty od `00`; 3DES używał 24 bajtów. IV AES wynosił `f0…ff`, a IV 3DES `f0…f7`.

AES udostępnia trzy długości klucza: 128, 192 i 256 bitów; dlatego porównano wszystkie trzy warianty oraz dwie wartości klucza 128-bitowego. Zastosowany 3DES korzystał z klucza 24-bajtowego, tj. 168 bitów efektywnego klucza DES po pominięciu bitów parzystości.

| TJ | H(TJ) | AES-128 A | AES-128 B | AES-192 | AES-256 | 3DES-168 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Jednorodny | 0,0000 | 7,79 | 7,7832 | 7,7844 | 7,7988 | 7,8370 |
| Średni | 3,7662 | 7,8202 | 7,8206 | 7,8153 | 7,7965 | 7,8153 |
| Wysoki | 4,2337 | 7,7981 | 7,8163 | 7,8157 | 7,8253 | 7,7852 |

| Algorytm, tekst jednorodny | Pierwsze 16 B TT (hex) |
| --- | --- |
| AES-128 A | `c776a80e515f9d192ffcc72c2ff5b9d0` |
| AES-192 | `7dbd2af6c1207ecbf84e10c087ba8480` |
| AES-256 | `4cb96108002975920e4ba660705e3c39` |
| 3DES-168 | `7eef4256e15d70bd360db84ea9bcf3dc` |

W histogramie tekstu jednorodnego występuje tylko `48(1024)`, czyli kod znaku `H`. Po zaszyfrowaniu rozkład jest już dużo bardziej płaski: najczęstszy bajt pojawia się około 8–12 razy na próbce ponad 1000 bajtów. Entropia wychodzi blisko 8,0, ale nie dokładnie tyle.

### 1.3 Wnioski (pytania 1.3–1.9)

**1.3.** Algorytmy blokowe są używane np. w TLS i VPN-ach, przy szyfrowaniu dysków, archiwów oraz danych przechowywanych na serwerach. Najczęściej spotykany jest obecnie AES z blokiem 128-bitowym i kluczem 128 albo 256 bitów (AES-192 jest również dostępny). Blok 128-bitowy jest współczesnym standardem dla AES; 3DES z blokiem 64-bitowym jest już wycofywany.

**1.4–1.5.** Szyfr blokowy w odpowiednim trybie dobrze ukrywa histogram tekstu. Nawet dla `H×1024` po szyfrowaniu otrzymano około 7,8 bit/bajt. Dla porównania w Cezarze histogram jest tylko przesunięty, a przy transpozycji zostaje praktycznie taki sam, więc tam analiza częstości jest o wiele prostsza.

**1.6–1.9.** Zmiana długości klucza AES z 128 na 192 albo 256 bitów nie dała widocznej zmiany entropii TT. Inna wartość klucza i wybór AES lub 3DES oczywiście zmieniają sam kryptogram, ale jego wygląd statystyczny zostaje podobny. Dla każdego z trzech tekstów jawnych entropia TT była wysoka. Nie da się więc ocenić siły szyfru tylko z jednej wartości entropii.

## 2. Tryby pracy algorytmów blokowych

### 2.1–2.4 3DES i tekst cykliczny

Tekst jawny miał 1024 bajty i postać `ABCDABCD…`. Dla 3DES użyto klucza 168-bitowego i tego samego IV w każdym porównaniu. W CFB sprzężenie zwrotne odbywało się całym blokiem 64-bitowym, a OFB tworzył strumień na podstawie 3DES-ECB.

| Tryb | H(TT) [bit/B] | Różne bloki 8-B | Początek TT | Ocena |
| --- | ---: | ---: | --- | --- |
| ECB | 3,0655 | 2 | `2fb9dc4cf8c31856` powtórzone | Ujawnia wzorzec; nie nadaje się do takich plików. |
| CBC | 7,7794 | 129 | `ef34f61e1d933ee947e99617a9020751…` | Powtarzalność znika. |
| CFB | 7,8044 | 128 | `e071cb117b5922e36813da149121a80e…` | Ukrywa wzorzec, działa strumieniowo. |
| OFB | 7,7818 | 128 | `e071cb117b5922e3ed1f45b0126e58d0…` | Ukrywa wzorzec, XOR ze strumieniem klucza. |

ECB szyfruje identyczne bloki dokładnie tak samo, przez co wzór w pliku nadal widać. W pozostałych trybach kolejne bloki zależą od wcześniejszego wyniku albo od bieżącego stanu i regularność znika. Dlatego ECB nie nadaje się do takich powtarzalnych danych.

### 2.5 i 2.8 Propagacja błędów

Dla AES-128-CBC, gdzie blok ma 16 B, użyto tekstu zróżnicowanego i numeracji bajtów od zera. Odwrócono bit 0 w `C[10]`. Po odszyfrowaniu pierwszy blok był nieczytelny, a w drugim bloku odwrócił się bit 0 w bajcie o tym samym przesunięciu; łącznie zmieniło się 17 bajtów. Następnie odwrócono bity w `C[10]` i `C[11]` (blisko siebie): pierwszy blok znów był nieczytelny, a w drugim zmieniły się dokładnie dwa wskazane bity. Dla bitów w `C[10]` i `C[74]` (daleko od siebie) nieczytelne były dwa odpowiadające im bloki, a po każdym z nich zmieniał się tylko wskazany bit następnego bloku.

| Modyfikacja TT | Wynik deszyfrowania CBC |
| --- | --- |
| Bit/jeden lub wiele bitów w bloku | bieżący blok nieczytelny; odpowiadające bity zmienione w następnym bloku |
| Dodanie/usunięcie 1 B w środku TT | długość nie jest wielokrotnością 16, więc deszyfrator odrzuca TT |
| Wstawienie 16 B po `C[3]` | wstawiony blok daje śmieci, następny blok TJ jest uszkodzony, a od kolejnego bloku następuje synchronizacja |
| Usunięcie `C[4]` | `P[4]` znika, `P[5]` jest uszkodzony, a od `P[6]` kolejne bloki są znów poprawne |

Dla porównania ECB uszkadza tylko blok odpowiadający błędowi, OFB tylko te bity, a CFB ma ograniczoną propagację do kolejnego segmentu/bloku.

### 2.6 Identyfikacja kryptogramów

W podanych przykładach bloki zapisano po 32 znaki hex, czyli po 16 B. Taki podział pasuje np. do AES.

| Próbka | Wniosek | Uzasadnienie |
| --- | --- | --- |
| a | ECB, blok 16 B | Wszystkie siedem bloków jest identyczne. |
| b | ECB, blok 16 B | Dwa bloki powtarzają się naprzemiennie. |
| c | CBC, CFB albo OFB; blok 16 B | Bloki się nie powtarzają i wyglądają losowo. Sam kryptogram nie wystarcza, aby wybrać jeden z tych trzech trybów. |

### 2.7–2.11 Odpowiedzi

- **2.7:** Dla jednorodnego TJ ECB zostawia powtarzające się bloki, dlatego entropia tej próbki jest wyraźnie niższa. CBC, CFB i OFB dały płaskie histogramy oraz około 7,8 bit/bajt.
- **2.8:** W CBC jeden błąd wpływa na dwa bloki. Przykładowo zmiana bitu 0 w `C[10]` zniszczyła cały pierwszy blok TJ, a w drugim zmieniła tylko bit 0 tego samego bajtu; zmiana dwóch bitów w `C[10]` i `C[11]` dała dwa takie kontrolowane przekłamania w drugim bloku. W ECB uszkodzony byłby tylko blok odpowiadający błędowi, w OFB zmieniają się jedynie te bity, które zostały zmienione w TT, a w CFB błąd przechodzi też na następny segment.
- **2.9:** Usunięcie fragmentu niebędącego pełnym blokiem rozstraja ECB i CBC: po usunięciu jednego bajtu z badanego AES-CBC deszyfracja została odrzucona, bo długość TT nie była wielokrotnością 16 B. Po usunięciu całego `C[4]` blok `P[4]` zniknął, `P[5]` był uszkodzony, a od `P[6]` tekst znów był poprawny. ECB nie ma zależności między blokami. W OFB i CFB utrata bajtu przesuwa cały dalszy strumień.
- **2.10:** ECB można wykorzystać dla niezależnych bloków, które już wcześniej nie mają widocznej struktury, ale przy plikach tekstowych nie jest dobrym wyborem. CBC nadaje się do szyfrowania kolejnych bloków wiadomości lub pliku.
- **2.11:** ECB pozwala bez problemu szyfrować i odszyfrowywać bloki równolegle. CBC szyfruje się po kolei, ale odszyfrowanie bloków można rozdzielić, jeśli dla każdego zadania dostępny jest poprzedni blok TT (dla pierwszego — IV). OFB działa kolejno w obu kierunkach. CFB szyfruje się kolejno; jego odszyfrowanie można wykonywać równolegle przy dostępie do poprzedniego segmentu TT.
