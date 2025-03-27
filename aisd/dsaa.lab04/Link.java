package dsaa.lab04;

public class Link implements Comparable<Link> {
    public String ref;
    public int weight;

    public Link(String ref) {
        this(ref, 1);
    }

    public Link(String ref, int weight) {
        this.ref = ref.toLowerCase();
        this.weight = weight;
    }

    @Override
    public boolean equals(Object other) {
        if (this == other) {
            return true;
        }
        if (!(other instanceof Link)) {
            return false;
        }
//        Cannot use pattern variable because of compatibility with Java 8
        @SuppressWarnings("PatternVariableCanBeUsed") Link link = (Link) other;
        return ref.equals(link.ref);
    }

    @Override
    public String toString() {
        return ref + "(" + weight + ")";
    }

    @Override
    public int compareTo(Link another) {
        return ref.compareTo(another.ref);
    }
}

