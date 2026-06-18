# MSID / Optymalizacja systemow - schematy rozwiazan

## 1. Jak rozpoznac typ zadania

| Objawy w tresci                                             | Typ zadania                       | Co robisz                                                                        |
| ----------------------------------------------------------- | --------------------------------- | -------------------------------------------------------------------------------- |
| Produkty, surowce, zysk, limity zasobow                     | programowanie liniowe, produkcja  | zmienne = ilosci produktow, maksymalizujesz zysk, ograniczenia zasobow           |
| Mieszanie skladnikow, minimalny koszt, wymagania procentowe | mieszanka/blending                | zmienne = ilosci skladnikow, minimalizujesz koszt, ograniczenia jakosci i ilosci |
| Magazyny, odbiorcy, koszty przewozu, podaz i popyt          | problem transportowy              | zmienne `x_ij`, minimalizujesz koszt transportu                                  |
| Firmy i zlecenia, kazdy dokladnie raz                       | problem przydzialu                | zmienne binarne `x_ij`, minimalizujesz koszt                                     |
| Kontener/plecak, waga, objetosc, wartosc                    | problem plecakowy                 | zmienne calkowite, maksymalizujesz wartosc                                       |
| Maszyny, produkty, czasy, wymagane ilosci                   | przydzial produkcji do maszyn     | zmienne `u_ij`, minimalizujesz koszt/czas                                        |
| Funkcja jednej zmiennej + rownania/nierownosci              | optymalizacja z ograniczeniami 1D | wyznaczasz zbior dopuszczalny i sprawdzasz kandydatow                            |
| Funkcja wielu zmiennych + rownosci                          | mnozniki Lagrange'a               | budujesz `L`, liczysz pochodne, rozwiazujesz uklad                               |
| Minimum funkcji bez ograniczen, punkt startowy i krok       | metoda najwiekszego spadku        | iterujesz `x(k+1)=x(k)-h(k) grad f(x(k))`                                        |
| Ograniczenia, metoda funkcji kary                           | kara zewnetrzna                   | minimalizujesz funkcje `F(x,r)=f(x)+r*kary` dla rosnacego `r`                    |
| Kilka funkcji celu `f1`, `f2`, wagi alfa                    | Pareto / metoda wag               | minimalizujesz `F=alfa1*f1+alfa2*f2`                                             |
| Minimum na przedziale jednej zmiennej                       | optymalizacja 1D                  | pochodna albo metoda numeryczna, sprawdzasz konce przedzialu                     |

## 2. Uniwersalny schemat modelowania

Zawsze zapisuj odpowiedz w tej kolejnosci:

1. Zmienne decyzyjne: co oznaczaja i w jakich jednostkach.
2. Funkcja celu: maksymalizacja albo minimalizacja.
3. Ograniczenia: zasoby, popyt, jakosc, czas, logika przydzialu.
4. Warunki znakowe/calkowitosci: `x_i >= 0`, czasem `x_i in Z_+`, `x_ij in {0,1}`.
5. Jezeli trzeba podac wynik liczbowy: rozwiazujesz metoda wierzcholkow, simpleksem, Solverem albo iteracyjnie.

Najczestszy blad: pomylenie kierunku nierownosci. Regula:

| Sformulowanie                                   | Nierownosc |
| ----------------------------------------------- | ---------- |
| nie wiecej niz, nie przekraczajac, limit, zasob | `<=`       |
| co najmniej, minimum, zapotrzebowanie           | `>=`       |
| dokladnie, ma byc rowne                         | `=`        |

## 3. Programowanie liniowe - produkcja

Typ z list 1 i 2: produkty, zyski, zuzycie zasobow, limity.

Dane:

- produkty `N_1,...,N_n`,
- zysk jednostkowy `z_j`,
- zasoby `R_i`, dostepne ilosci `b_i`,
- zuzycie zasobu `i` na produkt `j`: `a_ij`.

Model:

```text
x_j = liczba jednostek produktu j

max Z = sum_{j=1}^n z_j x_j

sum_{j=1}^n a_ij x_j <= b_i,  i=1,...,m
x_j >= 0
```

Jezeli produkty musza byc w sztukach, dopisz `x_j in Z_+`.

Manualnie dla 2 zmiennych:

1. Zamien ograniczenia na proste.
2. Narysuj obszar dopuszczalny.
3. Znajdz wierzcholki: przeciecia prostych i osi.
4. Policz funkcje celu w kazdym wierzcholku.
5. Dla maksimum wybierz najwieksza wartosc, dla minimum najmniejsza.

## 4. Mieszanka / blending

Typ: mieszanie wegla, paliwa, surowcow, jakosc procentowa.

Przyklad struktury: co najmniej `B` ton mieszanki, zanieczyszczenie fosforem nie wiecej niz `Pmax`, popiol nie wiecej niz `Amax`, koszty `c_A`, `c_B`.

Zmienne:

```text
x_A = ilosc skladnika A
x_B = ilosc skladnika B
```

Model kosztowy:

```text
min K = c_A x_A + c_B x_B
x_A + x_B >= B
p_A x_A + p_B x_B <= Pmax (x_A + x_B)
a_A x_A + a_B x_B <= Amax (x_A + x_B)
x_A, x_B >= 0
```

Uwaga na procenty: jezeli w tabeli jest `0,02%`, w obliczeniach mozesz konsekwentnie uzywac albo `0,02`, albo `0,0002`, ale po obu stronach nierownosci ta sama skala musi byc identyczna.

## 5. Problem transportowy

Typ: magazyny `M_i`, odbiorcy `O_j`, koszty `c_ij`, podaz `A_i`, popyt `B_j`.

Zmienne:

```text
x_ij = ilosc wyslana z magazynu i do odbiorcy j
```

Model:

```text
min K = sum_i sum_j c_ij x_ij

sum_j x_ij <= A_i       dla kazdego dostawcy i
sum_i x_ij >= B_j       dla kazdego odbiorcy j
x_ij >= 0
```

Gdy suma podazy rowna sie sumie popytu, najczesciej zapisuje sie rownosci:

```text
sum_j x_ij = A_i
sum_i x_ij = B_j
```

Gdy podaz i popyt nie sa rowne:

- `podaz > popyt`: dodaj fikcyjnego odbiorce z popytem `podaz-popyt` i kosztem `0`,
- `popyt > podaz`: dodaj fikcyjnego dostawce z podaza `popyt-podaz` i kosztem kary albo `0`, jezeli braki sa dopuszczalne.

## 6. Problem przydzialu

Typ: `N` firm i `N` zlecen, kazda firma ma wykonac dokladnie jedno zlecenie i kazde zlecenie ma byc wykonane dokladnie raz.

Zmienne binarne:

```text
x_ij = 1, jezeli firma i wykonuje zlecenie j
x_ij = 0, w przeciwnym razie
```

Model:

```text
min K = sum_i sum_j c_ij x_ij

sum_j x_ij = 1      dla kazdej firmy i
sum_i x_ij = 1      dla kazdego zlecenia j
x_ij in {0,1}
```

Do liczenia recznego: metoda wegierska albo sprawdzenie permutacji dla malych `N`.

## 7. Plecak / kontener

Typ: przedmioty, waga, objetosc, wartosc/zysk, pojemnosc i udzwig.

Zmienne:

```text
x_n = liczba sztuk towaru n
```

Model z waga i objetoscia:

```text
max W = sum_n c_n x_n
sum_n v_n x_n <= V
sum_n p_n x_n <= P
x_n in Z_+
```

Jezeli kazdy przedmiot mozna wziac najwyzej raz:

```text
x_n in {0,1}
```

Dla malego plecaka licz recznie przez enumeracje kombinacji. Dla wiekszego: programowanie dynamiczne albo Solver z calkowitoscia.

## 8. Przydzial produkcji do maszyn

Typ: produkty `i`, maszyny `j`, czas jednostkowy `t_ij`, koszt `c_ij`, dostepny czas `T_j`, wymagane ilosci `P_i`.

Zmienne:

```text
u_ij = ilosc produktu i wytworzona na maszynie j
```

Model:

```text
min K = sum_i sum_j c_ij u_ij

sum_j u_ij >= P_i              dla kazdego produktu i
sum_i t_ij u_ij <= T_j         dla kazdej maszyny j
u_ij >= 0
```

Jezeli celem jest minimalizacja lacznego czasu pracy, zamiast kosztu uzyj:

```text
min T = sum_i sum_j t_ij u_ij
```

Jezeli w tabeli podana jest wydajnosc `w_ij` w m/h, to czas potrzebny na produkcje `u_ij` wynosi:

```text
czas_ij = u_ij / w_ij
```

Wtedy ograniczenia czasu maszyn:

```text
sum_i u_ij / w_ij <= T_j
```

## 9. Optymalizacja jednej zmiennej z ograniczeniami

Typ z listy 3: funkcja `f(x)` i ograniczenia `h(x)=0` albo `g_i(x)<=0`.

Dla rownosci `h(x)=0`:

1. Rozwiaz `h(x)=0`.
2. Dostajesz skonczony zbior kandydatow `x`.
3. Oblicz `f(x)` dla kazdego.
4. Minimum to najmniejsza wartosc, maksimum najwieksza.

Dla nierownosci `g_i(x)<=0`:

1. Rozwiaz kazda nierownosc osobno.
2. Wez czesc wspolna, czyli zbior dopuszczalny.
3. Znajdz punkty krytyczne `f'(x)=0` lezace w zbiorze dopuszczalnym.
4. Dodaj granice przedzialow dopuszczalnych.
5. Policz `f` w kandydatach i wybierz optimum.

Uwaga: jezeli zbior dopuszczalny nie jest domkniety albo funkcja dazy do `-infinity`, minimum moze nie istniec.

## 10. Mnozniki Lagrange'a

Typ: minimum/maksimum `f(x_1,...,x_n)` przy ograniczeniach rownosciowych.

Standardowy zapis ograniczen:

```text
h_j(x) = b_j,  j=1,...,m
```

Funkcja Lagrange'a:

```text
L(x, lambda) = f(x) + sum_{j=1}^m lambda_j (b_j - h_j(x))
```

Rownowaznie mozna uzyc `L=f+sum lambda_j(h_j(x)-b_j)`. Znak lambdy sie zmieni, ale punkt `x` bedzie ten sam.

Warunki konieczne:

```text
partial L / partial x_i = 0,  i=1,...,n
partial L / partial lambda_j = 0,  j=1,...,m
```

Schemat rozwiazania:

1. Zapisz `L`.
2. Policz wszystkie pochodne po `x_i` i `lambda_j`.
3. Rozwiaz uklad rownan.
4. Dla kazdego punktu policz `f`.
5. Porownaj wartosci i wybierz minimum/maksimum.

Przyklad postaci dla jednego ograniczenia `x1^2+x2^2=1`:

```text
L = f(x1,x2) + lambda(1 - x1^2 - x2^2)
dL/dx1 = 0
dL/dx2 = 0
dL/dlambda = 1 - x1^2 - x2^2 = 0
```

Typowy trik: gdy z pochodnych wychodzi np. `2x1 - 2lambda x1 = 0`, zapisujesz `2x1(1-lambda)=0`, wiec masz przypadki `x1=0` albo `lambda=1`.

## 11. Metoda najwiekszego spadku - krok staly

Typ z list 4 i 7: dana funkcja, punkt startowy, staly krok `h`, tolerancja `epsilon`.

Algorytm minimalizacji:

```text
x(0) = punkt startowy
for k = 0,1,2,...:
    oblicz grad f(x(k))
    x(k+1) = x(k) - h grad f(x(k))
    stop, gdy ||x(k+1)-x(k)|| < epsilon albo ||grad f(x(k))|| < epsilon
```

Norma najczesciej:

```text
||v|| = sqrt(v1^2 + v2^2 + ... + vn^2)
```

Jak pokazac iteracje w tabeli:

| k   | x1(k) | x2(k) | grad f(x(k)) | x(k+1) | norma kroku | f(x(k+1)) |
| --- | ----: | ----: | ------------ | ------ | ----------: | --------: |

Wazne:

- dla zbyt duzego kroku metoda moze oscylowac albo uciekac,
- dla zbyt malego kroku bedzie bardzo wolna,
- jezeli potrzeba wiecej niz 10 iteracji, lista 4 pozwala uzyc komputera i pokazac pierwsze oraz ostatnie 3 iteracje.

## 12. Metoda najwiekszego spadku - krok zmienny

Typ: `h(k)` zalezy od numeru iteracji, np. `0.0007k`, `0.03 sqrt(k)`.

Algorytm:

```text
x(0) = punkt startowy
for k = 1,2,3,...:
    h_k = wzor z zadania
    x(k) = x(k-1) - h_k grad f(x(k-1))
    stop, gdy ||x(k)-x(k-1)|| < epsilon albo ||grad f(x(k))|| < epsilon
```

Uwaga na indeksowanie: jezeli startujesz od `x(0)`, wygodnie brac pierwszy krok jako `h_1`.

Przy porownywaniu wariantow kroku zapisuj:

```text
h(k), liczba iteracji, punkt koncowy, f(x), czy metoda byla stabilna
```

## 13. Pochodne gradientow z list

Dla szybkiego liczenia.

Funkcja kwadratowa:

```text
f(x1,x2) = x1^2 + x2^2
grad f = (2x1, 2x2)
```

Funkcja Rosenbrocka-podobna:

```text
f(x1,x2) = a(x1^2 - x2)^2 + b(1 - x1)^2

df/dx1 = 4a x1 (x1^2 - x2) - 2b(1 - x1)
df/dx2 = -2a (x1^2 - x2)
```

Dla przykladow:

```text
2.5(x1^2-x2)^2 + (1-x1)^2:
grad = (10x1(x1^2-x2) - 2(1-x1), -5(x1^2-x2))

3(x1^2-x2)^2 + 2(1-x1)^2:
grad = (12x1(x1^2-x2) - 4(1-x1), -6(x1^2-x2))

2(x1^2-x2)^2 + (1-x1)^2:
grad = (8x1(x1^2-x2) - 2(1-x1), -4(x1^2-x2))
```

## 14. Metoda funkcji kary zewnetrznej

Typ z list 5 i 7: minimalizacja `f(x)` przy ograniczeniach rownosciowych lub nierownosciowych.

Idea: zamieniasz problem z ograniczeniami na serie problemow bez ograniczen.

Dla rownosci `h_j(x)=0` kara:

```text
P_eq(x) = sum_j h_j(x)^2
```

Dla nierownosci `g_i(x)<=0` kara:

```text
P_ineq(x) = sum_i max(0, g_i(x))^2
```

Funkcja karna:

```text
F(x,r) = f(x) + r [P_eq(x) + P_ineq(x)]
```

Algorytm:

```text
wybierz x(0), r0 > 0, beta > 1
for s = 0,1,2,...:
    zminimalizuj F(x, r_s) metoda bez ograniczen
    otrzymaj x_s
    jezeli naruszenie ograniczen jest male: stop
    r_{s+1} = beta r_s
    startuj kolejna minimalizacje z x_s
```

Co zapisac w rozwiazaniu:

```text
r, punkt x, f(x), wartosc kary, naruszenie ograniczen
```

Interpretacja ograniczen z listy 5:

- `g(x)<=0` jest spelnione, gdy `g(x)` jest ujemne albo zero,
- kara dziala tylko, gdy `g(x)>0`,
- dla przedzialu `[-1,1]` z ograniczen `-x-1<=0`, `x-1<=0` kara to `max(0,-x-1)^2 + max(0,x-1)^2`.

## 15. Pareto i metoda wag

Typ z list 6 i 7: dwie funkcje celu, np. `f1(x1,x2)`, `f2(x1,x2)`, minimum w sensie Pareto, podane pary wag.

Metoda wag:

```text
F_alpha(x) = alpha1 f1(x) + alpha2 f2(x)
alpha1 >= 0, alpha2 >= 0, alpha1 + alpha2 = 1
```

Nastepnie rozwiazujesz zwykle zadanie liniowe:

```text
min F_alpha(x)
przy danych ograniczeniach
```

Dla funkcji liniowych:

```text
f1 = a1 x1 + b1 x2
f2 = a2 x1 + b2 x2

F_alpha = (alpha1 a1 + alpha2 a2)x1 + (alpha1 b1 + alpha2 b2)x2
```

Schemat reczny dla 2 zmiennych:

1. Dla danej pary wag policz wspolczynniki funkcji `F_alpha`.
2. Wyznacz obszar dopuszczalny z nierownosci.
3. Znajdz jego wierzcholki.
4. Policz `F_alpha` w kazdym wierzcholku.
5. Wybierz najmniejsza wartosc.
6. Powtorz dla pozostalych par wag.

Wazne przy nierownosciach typu `>=`: obszar dopuszczalny jest po stronie powyzej/prowadzonej przez nierownosc. Minimum funkcji liniowej najczesciej bedzie w dolnych/lewych wierzcholkach obszaru, ale zawsze sprawdz wierzcholki.

Punkt Pareto-optymalny: nie istnieje inny punkt dopuszczalny, ktory poprawia jedna funkcje celu bez pogorszenia drugiej. Metoda wag znajduje typowe punkty Pareto dla problemow wypuklych.

## 16. Optymalizacja 1D na przedziale

Typ z listy 7: `f(x)=x+1/x`, `x+1/x^2`, `x+1/x^3`, `x^2+1/x^3` na przedziale.

Najszybszy schemat analityczny:

1. Sprawdz dziedzine funkcji, szczegolnie `x=0` przy `1/x^p`.
2. Oblicz pochodna `f'(x)`.
3. Rozwiaz `f'(x)=0`.
4. Wez tylko punkty lezace w przedziale i dziedzinie.
5. Dodaj konce przedzialu, jesli naleza do dziedziny.
6. Policz `f` i wybierz minimum.

Przydatne wzory:

```text
f(x) = x + 1/x        => f'(x) = 1 - 1/x^2, minimum przy x=1
f(x) = x + 1/x^2      => f'(x) = 1 - 2/x^3, minimum przy x = cubert(2)
f(x) = x + 1/x^3      => f'(x) = 1 - 3/x^4, minimum przy x = fourthroot(3)
f(x) = x^2 + 1/x^3    => f'(x) = 2x - 3/x^4, minimum przy x = fifthroot(3/2)
```

Uwaga: jezeli przedzial zawiera `0`, ale funkcja ma `1/x`, to `x=0` nie nalezy do dziedziny. Na przedziale typu `[0,2]` faktycznie analizujesz `(0,2]`.

## 17. Jak liczyc wierzcholki obszaru liniowego

Dla zadan z 2 zmiennymi.

1. Kazde ograniczenie liniowe zapisz jako prosta, np. `a x1 + b x2 = c`.
2. Rozwiazuj parami uklady dwoch prostych.
3. Dodaj przeciecia z osiami, jezeli masz `x1>=0`, `x2>=0`.
4. Kazdy kandydat sprawdz we wszystkich nierownosciach.
5. Zostaw tylko punkty dopuszczalne.
6. Policz funkcje celu.

Uklad dwoch prostych:

```text
a1 x + b1 y = c1
a2 x + b2 y = c2
```

Wyznacznik:

```text
D = a1 b2 - a2 b1
x = (c1 b2 - c2 b1) / D
y = (a1 c2 - a2 c1) / D
```

Jesli `D=0`, proste sa rownolegle albo pokrywaja sie.

## 18. Solver / arkusz - szybka procedura

Dla zadan liniowych, transportowych, przydzialu, plecaka:

1. Wpisz zmienne w komorkach.
2. Obok policz lewa strone kazdego ograniczenia przez `SUMA.ILOCZYNOW`.
3. Policz funkcje celu przez `SUMA.ILOCZYNOW(koszty_lub_zyski; zmienne)`.
4. Solver: ustaw komorke celu, min/max.
5. Zmieniane komorki: zakres zmiennych.
6. Dodaj ograniczenia: limity, popyty, nieujemnosc, calkowitosc/binarnosc.
7. Dla liniowych wybierz metode Simplex LP.

## 19. Minimalny szablon odpowiedzi egzaminacyjnej

```text
Zmienne decyzyjne:
x1 - ...
x2 - ...

Funkcja celu:
max/min Z = ...

Ograniczenia:
... <=/>=/= ...
... <=/>=/= ...
x1, x2 >= 0

Metoda:
Poniewaz jest to zadanie liniowe z dwiema zmiennymi, sprawdzam wierzcholki obszaru dopuszczalnego.

Wierzcholki i wartosci celu:
...

Wniosek:
Optimum jest w punkcie ..., wartosc funkcji celu wynosi ...
```

Dla metod iteracyjnych:

```text
Gradient:
grad f = (...)

Wzor iteracji:
x(k+1) = x(k) - h(k) grad f(x(k))

Kryterium stopu:
||x(k+1)-x(k)|| < epsilon

Tabela iteracji:
k, x(k), grad, h(k), x(k+1), norma, f(x(k+1))

Wniosek:
Po ... iteracjach otrzymano x ~= ..., f(x) ~= ...
```

## 20. Checklist przed oddaniem

- Czy zmienne maja opis i jednostki?
- Czy funkcja celu ma dobry kierunek: `max` zysk/wartosc, `min` koszt/czas?
- Czy kazdy zasob ma ograniczenie `<=`?
- Czy kazde zapotrzebowanie/minimum ma ograniczenie `>=`?
- Czy dodano `x >= 0`?
- Czy przy przydziale dodano `x_ij in {0,1}`?
- Czy przy plecaku dodano calkowitosc?
- Czy przy Lagrange'u sprawdzono wszystkie punkty z ukladu?
- Czy przy nierownosciach sprawdzono granice obszaru?
- Czy przy metodzie gradientowej zapisano kryterium stopu i liczbe iteracji?
- Czy przy Pareto policzono osobno wynik dla kazdej pary wag?
