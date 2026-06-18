import java.util.List;

public interface Graf<W, S> {

    /**
     * @return wszystkie wierzchołki grafu
     */
    List<W> wierzcholki();

    /**
     * @param w1 pierwszy wierzchołek
     * @param w2 drugi wierzchołek
     * @return etykietę krawędzi pomiędzy wierzchołkami albo NULL jesli nie istnieje
     */
    S krawedz(W w1, W w2);

    /**
     * @param w wierzchołek
     * @return wierzchołki, do których istnieje krawędź z w
     */
    List<W> krawedzie(W w);
}
