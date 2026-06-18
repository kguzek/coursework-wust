import java.util.*;

public class GrafNieskierowany<W, S> implements Graf<W, S> {

    private final List<W> wierzcholki;
    private final Map<W, Integer> indeks;
    private final S[][] macierz;

    @SuppressWarnings("unchecked")
    public GrafNieskierowany(List<W> w, List<Krawedz<W, S>> k) {
        this.wierzcholki = List.copyOf(w);
        this.indeks = new HashMap<>();

        for (int i = 0; i < w.size(); i++) {
            indeks.put(w.get(i), i);
        }

        final int size = w.size();
        this.macierz = (S[][]) new Object[size][size];

        for (Krawedz<W, S> e : k) {
            int i = indeks.get(e.w1());
            int j = indeks.get(e.w2());

            macierz[i][j] = e.etykieta();
            macierz[j][i] = e.etykieta();
        }
    }

    @Override
    public List<W> wierzcholki() {
        return wierzcholki;
    }

    @Override
    public S krawedz(W w1, W w2) {
        Integer i = indeks.get(w1);
        Integer j = indeks.get(w2);

        if (i == null || j == null) {
            return null;
        }
        return macierz[i][j];
    }

    @Override
    public List<W> krawedzie(W w) {
        Integer i = indeks.get(w);
        if (i == null) {
            return List.of();
        }

        List<W> wynik = new ArrayList<>();
        for (int j = 0; j < macierz.length; j++) {
            if (macierz[i][j] != null) {
                wynik.add(wierzcholki.get(j));
            }
        }
        return wynik;
    }

    public boolean hasEdge(W w1, W w2) {
        return krawedz(w1, w2) != null;
    }

    public int stopien(W w) {
        Integer i = indeks.get(w);
        if (i == null) {
            return 0;
        }

        int count = 0;
        for (int j = 0; j < macierz.length; j++) {
            if (macierz[i][j] != null) {
                count++;
            }
        }
        return count;
    }
}
