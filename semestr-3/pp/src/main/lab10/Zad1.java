
import java.util.HashSet;
import java.util.List;

public class Zad1 {

    public static void main(String[] args) {
        testGrafPodstawowy();
        testGrafSkrajne();
        demonstracja();
    }

    private static void testGrafPodstawowy() {
        List<String> wierzcholki = List.of("A", "B", "C", "D");

        List<Krawedz<String, Integer>> krawedzie = List.of(
                new Krawedz<>("A", "B", 5),
                new Krawedz<>("A", "C", 3),
                new Krawedz<>("B", "D", 7)
        );

        GrafNieskierowany<String, Integer> graf
                = new GrafNieskierowany<>(wierzcholki, krawedzie);

        System.out.println(test("A-B istnieje", graf.krawedz("A", "B") == 5));
        System.out.println(test("B-A istnieje (nieskierowany)", graf.krawedz("B", "A") == 5));
        System.out.println(test("A-D nie istnieje", graf.krawedz("A", "D") == null));
        System.out.println(test("C-D nie istnieje", graf.krawedz("C", "D") == null));

        System.out.println(test("A-B true", graf.hasEdge("A", "B")));
        System.out.println(test("B-A true", graf.hasEdge("B", "A")));
        System.out.println(test("A-D false", !graf.hasEdge("A", "D")));
        System.out.println(test("C-C false (brak pętli)", !graf.hasEdge("C", "C")));

        System.out.println(test("stopien(A) == 2", graf.stopien("A") == 2));
        System.out.println(test("stopien(B) == 2", graf.stopien("B") == 2));
        System.out.println(test("stopien(C) == 1", graf.stopien("C") == 1));
        System.out.println(test("stopien(D) == 1", graf.stopien("D") == 1));

        System.out.println(test("sąsiedzi A = {B,C}",
                new HashSet<>(graf.krawedzie("A")).containsAll(List.of("B", "C"))
                && graf.krawedzie("A").size() == 2));

        System.out.println(test("sąsiedzi B = {A,D}",
                new HashSet<>(graf.krawedzie("B")).containsAll(List.of("A", "D"))
                && graf.krawedzie("B").size() == 2));

        System.out.println(test("sąsiedzi C = {A}",
                graf.krawedzie("C").equals(List.of("A"))));

        System.out.println(test("sąsiedzi D = {B}",
                graf.krawedzie("D").equals(List.of("B"))));

        System.out.println(test("nieistniejący wierzchołek",
                graf.stopien("X") == 0));
    }

    private static void testGrafSkrajne() {
        GrafNieskierowany<Integer, String> grafPusty
                = new GrafNieskierowany<>(List.of(), List.of());
        System.out.println(test("Graf pusty - brak wierzchołków",
                grafPusty.wierzcholki().isEmpty()));

        GrafNieskierowany<String, Integer> grafJeden
                = new GrafNieskierowany<>(List.of("X"), List.of());
        System.out.println(test("Graf jednoelementowy - stopień = 0",
                grafJeden.stopien("X") == 0));
        System.out.println(test("Graf jednoelementowy - brak sąsiadów",
                grafJeden.krawedzie("X").isEmpty()));

        List<Integer> wierzcholki = List.of(1, 2, 3, 4);
        List<Krawedz<Integer, String>> krawedzie = List.of(
                new Krawedz<>(1, 2, "a")
        );
        GrafNieskierowany<Integer, String> grafIzolowane
                = new GrafNieskierowany<>(wierzcholki, krawedzie);
        System.out.println(test("Izolowane wierzchołki - stopień(3) = 0",
                grafIzolowane.stopien(3) == 0));
        System.out.println(test("Izolowane wierzchołki - stopień(4) = 0",
                grafIzolowane.stopien(4) == 0));

        List<Character> wierzcholkiPelny = List.of('A', 'B', 'C');
        List<Krawedz<Character, Integer>> krawedzie2 = List.of(
                new Krawedz<>('A', 'B', 1),
                new Krawedz<>('A', 'C', 2),
                new Krawedz<>('B', 'C', 3)
        );
        GrafNieskierowany<Character, Integer> grafPelny
                = new GrafNieskierowany<>(wierzcholkiPelny, krawedzie2);
        System.out.println(test("Graf pełny - wszystkie stopnie = 2",
                grafPelny.stopien('A') == 2
                && grafPelny.stopien('B') == 2
                && grafPelny.stopien('C') == 2));

        List<String> w = List.of("start", "end");
        List<Krawedz<String, Double>> k = List.of(
                new Krawedz<>("start", "end", 3.14)
        );
        GrafNieskierowany<String, Double> grafDouble
                = new GrafNieskierowany<>(w, k);
        System.out.println(test("Etykiety typu Double",
                Math.abs(grafDouble.krawedz("start", "end") - 3.14) < 0.001));
    }

    private static void demonstracja() {
        List<String> miasta = List.of("Wrocław", "Warszawa", "Kraków", "Poznań", "Gdańsk");

        List<Krawedz<String, Integer>> drogi = List.of(
                new Krawedz<>("Wrocław", "Warszawa", 350),
                new Krawedz<>("Wrocław", "Kraków", 270),
                new Krawedz<>("Warszawa", "Kraków", 290),
                new Krawedz<>("Warszawa", "Gdańsk", 340),
                new Krawedz<>("Poznań", "Warszawa", 310)
        );

        GrafNieskierowany<String, Integer> mapa =
                new GrafNieskierowany<>(miasta, drogi);

        System.out.println("Wierzchołki grafu: " + mapa.wierzcholki());
        System.out.println("\nOperacje na grafie:");

        System.out.println("\n1. Metoda krawedz(w1, w2) - pobiera etykietę krawędzi:");
        System.out.println("   Odległość Wrocław-Warszawa: " + mapa.krawedz("Wrocław", "Warszawa") + " km");
        System.out.println("   Odległość Warszawa-Wrocław: " + mapa.krawedz("Warszawa", "Wrocław") + " km (nieskierowany!)");
        System.out.println("   Odległość Wrocław-Gdańsk: " + mapa.krawedz("Wrocław", "Gdańsk") + " (brak połączenia)");

        System.out.println("\n2. Metoda hasEdge(w1, w2) - sprawdza istnienie krawędzi:");
        System.out.println("   Czy istnieje droga Wrocław-Kraków? " + mapa.hasEdge("Wrocław", "Kraków"));
        System.out.println("   Czy istnieje droga Kraków-Poznań? " + mapa.hasEdge("Kraków", "Poznań"));

        System.out.println("\n3. Metoda stopien(w) - liczba sąsiadów:");
        for (String miasto : miasta) {
            System.out.println("   Stopień wierzchołka " + miasto + ": " + mapa.stopien(miasto));
        }

        System.out.println("\n4. Metoda krawedzie(w) - lista sąsiadów:");
        for (String miasto : List.of("Warszawa", "Wrocław", "Gdańsk")) {
            System.out.println("   Miasta połączone z " + miasto + ": " + mapa.krawedzie(miasto));
        }
    }

    private static String test(String opis, boolean warunek) {
        return (warunek ? "[OK]   " : "[BŁĄD] ") + opis;
    }
}
