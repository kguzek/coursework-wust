# Cyberbezpieczeństwo

2026-10-13

## 1. Szyfrowanie historyczne

### Przykład 1

Szyfrowanie Vigenere `ABC` + Szyfrowanie Vigenere `DEF` się odszyfrowuje poprzez Vigenere `DFH`

### Przykład 2

Szyfrowanie Vigenere `ABC` + Szyfrowanie Vigenere `DEFG` się odszyfrowuje poprzez Vigenere `DFHGEGFHFEGI`

### Przykład 3

Szyfrowanie Hill 2x `QDZI` === Szyfrowanie Hill 1x `TUCJ`

## 2. Analiza własności dostępnych algorytmów.

### 2.1 Porównanie entropii tekstów jawnych

| Język     | Tekst                                                                            | Entropia |
| --------- | -------------------------------------------------------------------------------- | -------- |
| Polski    | Bardzo przepraszam, ale niestety nie mowie po polsku.                            | 3.94     |
| Angielski | I am terribly sorry, but unfortunately, I do not speak English.                  | 4.02     |
| Japoński  | Taihen moshiwake gozaimasen ga, zan ne nagara watashi wa nihongo no hanasemasen. | 3.44     |

### 2.2 Porównanie entropii tekstów zaszyfrowanych

1. Polski

| Algorytm szyfrowania | Entropia |
| -------------------- | -------- |
| Brak                 | 3.94     |
| Caesar               | 3.94     |

2. Angielski

| Algorytm szyfrowania | Entropia |
| -------------------- | -------- |
| Brak                 | 4.02     |
| Caesar               | 4.02     |

3. Japoński

| Algorytm szyfrowania | Entropia |
| -------------------- | -------- |
| Brak                 | 3.44     |
| Caesar               | 3.44     |

### 2.3 Histogramy tekstów jawnych

1. Polski
   ![Histogram tekstu w języku polskim](./screenshots/histograms/pl-plaintext.png)
2. Angielski
   ![Histogram tekstu w języku angielskim](./screenshots/histograms/en-plaintext.png)
3. Japoński
   ![Histogram tekstu w języku japońskim](./screenshots/histograms/jp-plaintext.png)

### 2.4 Histogramy tekstów zaszyfrowanych

### 2.5 N-gramy tekstów jawnych

1. Polski

   a. ![bigram tekstu w języku polskim](./screenshots/n-grams/pl-digram.png)
   b. ![trigram tekstu w języku polskim](./screenshots/n-grams/pl-trigram.png)
   c. ![4-gram tekstu w języku polskim](./screenshots/n-grams/pl-4gram.png)

2. Angielski

   a. ![bigram tekstu w języku angielskim](./screenshots/n-grams/en-digram.png)
   b. ![trigram tekstu w języku angielskim](./screenshots/n-grams/en-trigram.png)
   c. ![4-gram tekstu w języku angielskim](./screenshots/n-grams/en-4gram.png)

3. Japoński

   a. ![bigram tekstu w języku japońskim](./screenshots/n-grams/jp-digram.png)
   b. ![trigram tekstu w języku japońskim](./screenshots/n-grams/jp-trigram.png)
   c. ![4-gram tekstu w języku japońskim](./screenshots/n-grams/jp-4gram.png)
