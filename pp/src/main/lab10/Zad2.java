
import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Set;

public class Zad2 {

    public static <W, S> List<S> znajdzSciezke(Graf<W, S> graf, W start, W cel) {
        if (start == null || cel == null) {
            return null;
        }

        if (!graf.wierzcholki().contains(start) || !graf.wierzcholki().contains(cel)) {
            return null;
        }

        if (start.equals(cel)) {
            return List.of();
        }

        Set<W> odwiedzone = new HashSet<>();
        List<S> sciezka = new ArrayList<>();

        if (dfs(graf, start, cel, odwiedzone, sciezka)) {
            return sciezka;
        }

        return null;
    }

    private static <W, S> boolean dfs(Graf<W, S> graf, W aktualny, W cel,
            Set<W> odwiedzone, List<S> sciezka) {
        odwiedzone.add(aktualny);

        if (aktualny.equals(cel)) {
            return true;
        }

        for (W sasiad : graf.krawedzie(aktualny)) {
            if (!odwiedzone.contains(sasiad)) {
                S etykieta = graf.krawedz(aktualny, sasiad);
                sciezka.add(etykieta);

                if (dfs(graf, sasiad, cel, odwiedzone, sciezka)) {
                    return true;
                }

                sciezka.removeLast();
            }
        }

        return false;
    }

    public static <W, S> boolean istniejeSciezka(Graf<W, S> graf, W start, W cel) {
        List<S> sciezka = znajdzSciezke(graf, start, cel);

        if (sciezka == null) {
            System.out.println("Nie istnieje ścieżka z " + start + " do " + cel);
            return false;
        }

        if (sciezka.isEmpty()) {
            System.out.println("Wierzchołki " + start + " i " + cel + " są identyczne");
        } else {
            System.out.println("Ścieżka z " + start + " do " + cel + ": " + sciezka);
        }

        return true;
    }

    public static void main(String[] args) {
        testy();
        demonstracja();
    }

    private static void testy() {
        List<String> w1 = List.of("A", "B", "C", "D", "E");
        List<Krawedz<String, Integer>> k1 = List.of(
                new Krawedz<>("A", "B", 1),
                new Krawedz<>("B", "C", 2),
                new Krawedz<>("C", "D", 3),
                new Krawedz<>("D", "E", 4)
        );
        GrafNieskierowany<String, Integer> graf1
                = new GrafNieskierowany<>(w1, k1);

        List<Integer> sciezka1 = znajdzSciezke(graf1, "A", "E");
        System.out.println(test("Ścieżka A->E istnieje", sciezka1 != null && !sciezka1.isEmpty()));
        System.out.println(test("Długość ścieżki A->E = 4", sciezka1 != null && sciezka1.size() == 4));

        List<Integer> sciezka2 = znajdzSciezke(graf1, "B", "B");
        System.out.println(test("Ścieżka B->B (pusty)", sciezka2 != null && sciezka2.isEmpty()));

        List<String> w2 = List.of("A", "B", "C", "D");
        List<Krawedz<String, String>> k2 = List.of(
                new Krawedz<>("A", "B", "ab"),
                new Krawedz<>("C", "D", "cd")
        );
        GrafNieskierowany<String, String> graf2
                = new GrafNieskierowany<>(w2, k2);

        List<String> sciezka3 = znajdzSciezke(graf2, "A", "D");
        System.out.println(test("Brak ścieżki A->D", sciezka3 == null));

        GrafNieskierowany<Integer, Integer> graf3
                = new GrafNieskierowany<>(List.of(1), List.of());
        List<Integer> sciezka4 = znajdzSciezke(graf3, 1, 1);
        System.out.println(test("Graf jednoelementowy - ścieżka 1->1", sciezka4 != null && sciezka4.isEmpty()));

        List<Integer> sciezka5 = znajdzSciezke(graf1, "X", "Y");
        System.out.println(test("Nieistniejące wierzchołki - null", sciezka5 == null));

        List<String> w3 = List.of("A", "B", "C", "D");
        List<Krawedz<String, Integer>> k3 = List.of(
                new Krawedz<>("A", "B", 1),
                new Krawedz<>("B", "C", 2),
                new Krawedz<>("C", "D", 3),
                new Krawedz<>("D", "A", 4)
        );
        GrafNieskierowany<String, Integer> grafCykl
                = new GrafNieskierowany<>(w3, k3);
        List<Integer> sciezka6 = znajdzSciezke(grafCykl, "A", "C");
        System.out.println(test("Ścieżka w grafie cyklicznym A->C",
                sciezka6 != null && !sciezka6.isEmpty()));

        if (sciezka1 != null) {
            System.out.println(test("Etykiety ścieżki A->E: " + sciezka1, true));
        }
    }

    private static void demonstracja() {
        List<String> komputery = List.of("Server", "PC1", "PC2", "PC3", "PC4", "Printer");

        List<Krawedz<String, String>> polaczenia = List.of(
                new Krawedz<>("Server", "PC1", "eth0"),
                new Krawedz<>("Server", "PC2", "eth1"),
                new Krawedz<>("PC1", "PC3", "wifi"),
                new Krawedz<>("PC2", "PC4", "eth2"),
                new Krawedz<>("PC3", "Printer", "usb")
        );

        GrafNieskierowany<String, String> siec =
                new GrafNieskierowany<>(komputery, polaczenia);

        System.out.println("Topologia sieci: " + komputery);
        System.out.println("\nWyszukiwanie ścieżek w sieci:\n");

        System.out.println("1. Sprawdzanie połączenia Server -> Printer:");
        istniejeSciezka(siec, "Server", "Printer");

        System.out.println("\n2. Sprawdzanie połączenia Server -> PC2:");
        istniejeSciezka(siec, "Server", "PC2");

        System.out.println("\n3. Sprawdzanie połączenia PC1 -> PC1:");
        istniejeSciezka(siec, "PC1", "PC1");

        System.out.println("\n4. Sprawdzanie połączenia Printer -> PC4:");
        List<String> sciezka = znajdzSciezke(siec, "Printer", "PC4");
        if (sciezka != null) {
            System.out.println("   Etykiety na ścieżce: " + sciezka);
        }

        List<String> urzadzenia = List.of("A", "B", "C", "D", "E");
        List<Krawedz<String, Integer>> lacza = List.of(
                new Krawedz<>("A", "B", 1),
                new Krawedz<>("D", "E", 2)
        );
        GrafNieskierowany<String, Integer> sieci2 =
                new GrafNieskierowany<>(urzadzenia, lacza);

        System.out.println("\n5. Graf z rozłącznymi składowymi:");
        System.out.println("   Topologia: A-B, C (izolowany), D-E");
        istniejeSciezka(sieci2, "A", "E");
        istniejeSciezka(sieci2, "C", "D");
    }

    private static String test(String opis, boolean warunek) {
        return (warunek ? "[OK]   " : "[BŁĄD] ") + opis;
    }
}
