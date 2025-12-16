import java.util.HashSet;
import java.util.List;

public class Main {

    public static void main(String[] args) {

        List<String> wierzcholki = List.of("A", "B", "C", "D");

        List<Krawedz<String, Integer>> krawedzie = List.of(
                new Krawedz<>("A", "B", 5),
                new Krawedz<>("A", "C", 3),
                new Krawedz<>("B", "D", 7)
        );

        GrafNieskierowany<String, Integer> graf =
                new GrafNieskierowany<>(wierzcholki, krawedzie);

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

    private static String test(String opis, boolean warunek) {
        return (warunek ? "[OK]   " : "[BŁĄD] ") + opis;
    }
}
