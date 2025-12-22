
import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Set;

public class Zad3 {

    public static <W, S> List<List<W>> znajdzSkladowe(Graf<W, S> graf) {
        List<List<W>> skladowe = new ArrayList<>();
        Set<W> odwiedzone = new HashSet<>();

        for (W wierzcholek : graf.wierzcholki()) {
            if (!odwiedzone.contains(wierzcholek)) {
                List<W> skladowa = new ArrayList<>();
                dfs(graf, wierzcholek, odwiedzone, skladowa);
                skladowe.add(skladowa);
            }
        }

        return skladowe;
    }

    private static <W, S> void dfs(Graf<W, S> graf, W wierzcholek,
                                   Set<W> odwiedzone, List<W> skladowa) {
        odwiedzone.add(wierzcholek);
        skladowa.add(wierzcholek);

        for (W sasiad : graf.krawedzie(wierzcholek)) {
            if (!odwiedzone.contains(sasiad)) {
                dfs(graf, sasiad, odwiedzone, skladowa);
            }
        }
    }

    public static <W, S> void wypiszSkladowe(Graf<W, S> graf) {
        List<List<W>> skladowe = znajdzSkladowe(graf);

        System.out.println("Liczba spójnych składowych: " + skladowe.size());

        for (int i = 0; i < skladowe.size(); i++) {
            List<W> skladowa = skladowe.get(i);
            System.out.println("Składowa " + (i + 1) + ": " + skladowa);
        }
    }

    public static <W, S> boolean czySpojny(Graf<W, S> graf) {
        return znajdzSkladowe(graf).size() == 1;
    }

    public static void main(String[] args) {
        testy();
        demonstracja();
    }

    private static void testy() {
        List<String> w1 = List.of("A", "B", "C");
        List<Krawedz<String, Integer>> k1 = List.of(
                new Krawedz<>("A", "B", 1),
                new Krawedz<>("B", "C", 2)
        );
        GrafNieskierowany<String, Integer> graf1
                = new GrafNieskierowany<>(w1, k1);
        List<List<String>> skladowe1 = znajdzSkladowe(graf1);
        System.out.println(test("Graf spójny - 1 składowa",
                skladowe1.size() == 1 && skladowe1.getFirst().size() == 3));

        List<Integer> w2 = List.of(1, 2, 3, 4, 5);
        List<Krawedz<Integer, String>> k2 = List.of(
                new Krawedz<>(1, 2, "a"),
                new Krawedz<>(2, 3, "b"),
                new Krawedz<>(4, 5, "c")
        );
        GrafNieskierowany<Integer, String> graf2
                = new GrafNieskierowany<>(w2, k2);
        List<List<Integer>> skladowe2 = znajdzSkladowe(graf2);
        System.out.println(test("Graf niespójny - 2 składowe", skladowe2.size() == 2));
        System.out.println(test("Pierwsza składowa - 3 wierzchołki",
                skladowe2.stream().anyMatch(s -> s.size() == 3)));
        System.out.println(test("Druga składowa - 2 wierzchołki",
                skladowe2.stream().anyMatch(s -> s.size() == 2)));

        List<Character> w3 = List.of('A', 'B', 'C', 'D');
        GrafNieskierowany<Character, Integer> graf3
                = new GrafNieskierowany<>(w3, List.of());
        List<List<Character>> skladowe3 = znajdzSkladowe(graf3);
        System.out.println(test("Graf z izolowanymi wierzchołkami - 4 składowe",
                skladowe3.size() == 4));
        System.out.println(test("Każda składowa ma 1 wierzchołek",
                skladowe3.stream().allMatch(s -> s.size() == 1)));

        GrafNieskierowany<String, String> graf4
                = new GrafNieskierowany<>(List.of(), List.of());
        List<List<String>> skladowe4 = znajdzSkladowe(graf4);
        System.out.println(test("Graf pusty - 0 składowych", skladowe4.isEmpty()));

        GrafNieskierowany<Integer, Integer> graf5
                = new GrafNieskierowany<>(List.of(42), List.of());
        List<List<Integer>> skladowe5 = znajdzSkladowe(graf5);
        System.out.println(test("Graf jednoelementowy - 1 składowa", skladowe5.size() == 1));
        System.out.println(test("Składowa zawiera element 42",
                skladowe5.getFirst().contains(42) && skladowe5.getFirst().size() == 1));

        System.out.println(test("Graf spójny - czySpojny() = true",
                czySpojny(graf1)));
        System.out.println(test("Graf niespójny - czySpojny() = false",
                !czySpojny(graf2)));
    }

    private static void demonstracja() {
        System.out.println("1. Graf spójny (sieć społecznościowa - wszyscy połączeni):");
        List<String> osoby1 = List.of("Anna", "Bartek", "Celina", "Damian");
        List<Krawedz<String, String>> znajomosci1 = List.of(
                new Krawedz<>("Anna", "Bartek", "przyjaciele"),
                new Krawedz<>("Bartek", "Celina", "koledzy"),
                new Krawedz<>("Celina", "Damian", "rodzina"),
                new Krawedz<>("Damian", "Anna", "sąsiedzi")
        );
        GrafNieskierowany<String, String> siec1 =
                new GrafNieskierowany<>(osoby1, znajomosci1);
        wypiszSkladowe(siec1);
        System.out.println("Graf jest spójny: " + czySpojny(siec1));

        System.out.println("\n2. Graf z dwiema grupami (dwie oddzielne grupy znajomych):");
        List<String> osoby2 = List.of("Anna", "Bartek", "Celina", "Damian", "Ewa", "Filip");
        List<Krawedz<String, String>> znajomosci2 = List.of(
                new Krawedz<>("Anna", "Bartek", "grupa1"),
                new Krawedz<>("Bartek", "Celina", "grupa1"),
                new Krawedz<>("Damian", "Ewa", "grupa2"),
                new Krawedz<>("Ewa", "Filip", "grupa2")
        );
        GrafNieskierowany<String, String> siec2 =
                new GrafNieskierowany<>(osoby2, znajomosci2);
        wypiszSkladowe(siec2);
        System.out.println("Graf jest spójny: " + czySpojny(siec2));

        System.out.println("\n3. Graf z izolowanymi osobami:");
        List<Integer> id = List.of(1, 2, 3, 4, 5);
        List<Krawedz<Integer, String>> polaczenia = List.of(
                new Krawedz<>(1, 2, "link")
        );
        GrafNieskierowany<Integer, String> siec3 =
                new GrafNieskierowany<>(id, polaczenia);
        wypiszSkladowe(siec3);

        System.out.println("\n4. Graf bez krawędzi (wszyscy izolowani):");
        List<Character> litery = List.of('A', 'B', 'C');
        GrafNieskierowany<Character, Integer> siec4 =
                new GrafNieskierowany<>(litery, List.of());
        wypiszSkladowe(siec4);

        System.out.println("\n5. Graf z wieloma składowymi o różnych rozmiarach:");
        List<Integer> wierzcholki = List.of(1, 2, 3, 4, 5, 6, 7, 8, 9);
        List<Krawedz<Integer, Integer>> krawedzie = List.of(
                new Krawedz<>(1, 2, 10),
                new Krawedz<>(2, 3, 20),
                new Krawedz<>(3, 4, 30),
                new Krawedz<>(5, 6, 40),
                new Krawedz<>(8, 9, 50)
        );
        GrafNieskierowany<Integer, Integer> siec5 =
                new GrafNieskierowany<>(wierzcholki, krawedzie);
        wypiszSkladowe(siec5);
    }

    private static String test(String opis, boolean warunek) {
        return (warunek ? "[OK]   " : "[BŁĄD] ") + opis;
    }
}
