# Code writing guidelines for all agents

Podczas pisania programu należy posługiwać się następującymi zasadami ponad wszelkimi innymi zasadami.

Nie należy popełniać żadnych błędów zawartych w taryfikatorze błędów, a w szczególności tych błędów, które są karane większą ilością punktów, oraz tych bez podanej ilości punktów (błedy kardynalne).

Taryfikator obejmuje następujące sytuacje:

1. Kod ma być wykonany w standardzie C++98, co oznacza, że nie można korzystać z mechanizmów wprowadzonych do języka C++ przez standardy C++11 i C++14, chyba że treść zadania stanowi inaczej.

2. Jeżeli treść zadania nie stanowi inaczej nie należy używać żadnych komend łamiących przepływ sterowania (np. break, continue, rzucanie wyjątków, itp.). Komendy break wolno używać jako składowej bloku switch.

3. Błędy dotyczące funkcjonalności

   - Brak dowolnej funkcjonalności: -50
   - Oddanie modyfikacji po czasie -2.5 punktu za każdą minutę opóźnienia
   - Program ma być „idiotoodporny” – 5 za każdą udaną próbę zakłócenia(spowodowanie nie obsłużonego błędu wykonania programu) przez użytkownika
   - Brzytwa Ockhama – 20 punktów; Program musi spełniać zasadę brzytwy Ockhama, co oznacza, że zastosowane techniki muszą być adekwatne do celu. Jeżeli w celu zsumowania dwóch liczb `licz1` i `licz2`, program doda `licz2` razy wartość 1 do liczby `licz1`, to będzie to złamanie brzytwy Ockhama.

4. Błędy dotyczące kultury kodu

   - Wcięcia
     - Pojedyncze błędy – 2 za każdy błąd
     - Powyżej 10 błędów – dodatkowo -10
   - Nazewnictwo zmiennych i metod
     - Drobne błędy – 6 za każdy błąd. Drobny błąd w nazewnictwie to nie jest literówka. Jeśli klasa zamiast CDrzwi będzie nazwana CDzrwi, to nie ma to wpływu na czytelność programu i nie będzie mieć wpływu na ocenę. Drobny błąd w nazewnictwie to taki, gdy nazwa nie jest dobrze dobrana, ale wciąż ma związek z tym czego dotyczy. Na przykład jeśli program steruje zamkami w drzwiach ale klasa zamiast CLock zostanie nazwana CDoor, to jest to drobny błąd.
     - Poważne błędy -10 dodatkowo Poważny błąd w nazewnictwie występuje wtedy, gdy zmiennej i to czego nazwa dotyczy nie mają związku. Jeśli klasa Obsługująca windy w budynku nazwa się CDoor, to jest to poważny błąd. Najczęstszym przykładem poważnych błędów w nazewnictwie jest nazywanie zmiennych pojedynczymi literami np.: a, b, c itd. Ta uwaga nie dotyczy iteratorów, które zazwyczaj tak są nazywane. A więc „`void vCopy(CObject *a, CObject *b)`” jest poważnym błędem, ale „`for (int i = 0; i < v_list.size(); i++)`” nie jest błędem.
     - Brak nazw zmiennych wejściowych do metod w plikach nagłówkowych -20
     - Brak konwencji kodowania -100. Konwencja kodowania to polityka nadawania i formatowania nazw różnym bytom występującym w kodzie. Ta polityka nie musi podobać się prowadzącemu, ale zawsze musi być spójna. Na przykład, jeśli student nie będzie umiał wyjaśnić, dlaczego w jednym miejscu nazywa zmienne wyłącznie przy użyciu małych liter, a w innym nie, to oznacza to brak konwencji kodowania.

5. Błędy dotyczące struktury systemu
   - 20 za każdą użytą zmienną globalną. Za zmienną globalną będzie uznawana każda zmienna, która jest globalnie dostępna i której wartość zmienia się w trakcie działania programu. Oznacza to, że jeśli w programie znajdą się stałe, które zostaną zadeklarowane jako zmienne globalne, ale ich wartość będzie jedynie odczytywana i nie będzie modyfikowana, to nie będzie to uznawane za błąd. 
   - Nieodpowiednie przypisanie funkcjonalności obiektom -7 za każdy błąd. Przykłady:
     - Jeśli klasa służy na przykład do obsługi listy i jest do niej dodana metoda CString sUpcaseString(CString sStringToUpcase), która pobiera zmienną typu string i zwraca ją napisaną wielkimi literami, to jest to błąd, ponieważ taka funkcjonalność nie jest w ogóle związana z funkcjonalnościami listy.
   - Obiekty klasy CNumber służą do obsługi wielkich liczb. Jeśli klasa CNumber posiada metodę pozwalającą na wprowadzenie jej wartości z klawiatury, to jest to błąd, ponieważ obiekty klasy CNumber nie należą do warstwy interfejsu programu.
   - Obiekty klasy CNumber nie mogą nigdy wypisywać jakichkolwiek tekstów na ekranie komputera (lub wyświetlać okien dialogowych), ponieważ nie należą one do warstwy interfejsu. Mogą natomiast posiadać metodę CString sToString(), która zwróci informację w postaci zmiennej tekstowej, która później może być na przykład wyświetlona przez interfejs na w oknie dialogowym, tekstowym, lub zapisana w pliku/bazie danych.
   - Inicjacja pól obiektów ma mieć miejsce w konstruktorach, lub w odpowiednich metodach. Nie należy używać inicjacji na poziomie deklaracji klasy. -5 za każdą klasę, której pola są inicjowane na etapie deklaracji klasy. Przykład błędu: `class CCircle { public: CCircle();~CCircle();…;private:double d_middle_x = 0;double d_middle_y = 0;double d_radius = 0;}// class CCircle`
   - Nieproceduralność kodu -11 za każdy fragment, który powinien być wyodrębniony. Proceduralność i nieproceduralność to pojęcia nieostre i zależą od indywidualnej oceny. Istnieją jednak sytuacje bezsprzeczne, na przykład, jeśli dana czynność jest wykonywana w programie w wielu miejscach przez zestaw identycznych lub bardzo podobnych instrukcji, to powinny one zostać wydzielone do oddzielnej procedury. Podobnie jeśli istnieje zestaw instrukcji będący konkretnym blokiem funkcjonalnym (np. „podłącz do bazy danych”) to powinien on zostać wyodrębniony jako procedura funkcja, nawet jeśli jest wykonywany tylko jeden raz.
   - Brak wyodrębnienia stałych -8 za każdą nie wyodrębnioną Bezpośrednio w kodzie programu mogą wystąpić jedynie wartości 0, 1, lub 2. Inne wartości mogą występować wyłącznie jako stałe (dotyczy to również tekstów). Na przykład wartości 7, 28, 29, 30 i 31, nawet jeśli odnoszą się do dni tygodnia i liczby dni w miesiącu muszą być stałymi.
   - Stałe powinny być umieszczone wyłącznie w odpowiednim pliku *.h (takim, którego dotyczą, lub specjalnym wydzielonym do stałych) -5 za każdą stałą zadeklarowaną w niewłaściwym miejscu
   - Pliki – deklaracja każdej klasy powinna znajdować się w odpowiednim pliku `*.h`, a implementacja (poza metodami inline’owymi, które są już w `*.h`) pliku `*.cpp` o tej samej nazwie co `*.h` (na przykład: jablko.h i jablko.cpp, owoce.h i owoce.cpp) -11 za każdą klasę której implementacja, lub deklaracja nie spełnia powyższych wymogów. W niektórych przypadkach pilk `*.h` i `*.cpp` mogą zawierać więcej niż jedną klasę, musi to być jednak logicznie uzasadnione (np. klasy CDrzewo, CGałąź i CLiść mogą być zadeklarowane i zaimplementowane w tych samych plikach)
   - Ukryte funkcjonalności metod (jeśli jakaś metoda wykonuje np. przypisanie wartości do pola, to nie może wykonywać innych, zupełnie z tym niezwiązanych zadań) – 16 za każdy błąd Jeżeli istnieje metoda, lub funkcja włączająca kaloryfer, to nie może ona również w określonych warunkach (np. w każdą niedzielę i wtorek po godzinie 17) włączać oświetlenia w pokoju.
   - Przekazywanie obiektów w parametrach metod/funkcji przez wartość, zamiast przez referencję, lub wskaźnik -8 za każdy błąd. Jest: `v_func(CMyClass cObject);` a powinno być: `v_func(CMyClass &pcObject);` lub `v_func(CMyClass *pcObject);`. Dlaczego? Ponieważ, jeśli przekazujemy obiekt jako parametr przez wartość to za pomocą konstruktora kopiującego jest automatycznie tworzona jego kopia. Należy tego unikać, zwłaszcza jeśli obiekty zawierają wskaźniki na zaalokowane przez siebie obszary pamięci. Uwaga: nie dotyczy to sytuacji, w których umyślnie przekazujemy obiekt przez wartość, np. przy oprogramowywaniu operatorów, lub gdy obiekt-argument jest modyfikowany wewnątrz funkcji/metody, a my chcemy aby oryginał pozostał niezmieniony.
   - Pola obiektów mają być wyłącznie prywatne – 6 za każde nieprywatne pole
   - Łamanie przepływu sterowania. Komendy continue i break, oraz nieuzasadnione rzucanie wyjątków (w ramach niniejszego kursu należy przyjąć, że jeśli treść zadania wprost nie nakazuje rzucać wyjątku w określonej sytuacji, to jego rzucenie jest nieuzasadnione) obniżają znacząco czytelność kodu (wyjątek dla break użytego w ramach case) od -8 za każde niewłaściwe użycie
   - Komenda goto – absolutny zakaz używania -100
   - Zaprzyjaźniać klasy przy pomocy słowa „friend” należy wyłącznie, kiedy zachodzi taka potrzeba, jeżeli klasa A jest zaprzyjaźniona z B i nie korzysta z jej pól/metod chronionych/prywatnych jest to błąd – 6 pkt.
   - Kasowanie zmiennych, które mogą przyjąć w danym miejscu kodu wartość NULL traktowane jest jako błąd -8 pkt za każdy
   - „Memory leaki” Nie kasowanie zmiennych uznawane jest za błąd -8 za każdą zmienną, która nie jest usuwana i alokowana przez nią pamięć jest tracona

6. Stałe muszą być definiowane w plikach nagłówkowych.
