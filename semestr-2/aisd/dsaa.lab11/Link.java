package dsaa.lab11;

public class Link implements Comparable<Link> {
    public String ref;
    public int weight;

    public Link(String ref) {
        this(ref, 1);
    }

    public Link(String ref, int weight) {
        this.ref = ref;
        this.weight = weight;
    }

    public boolean equals(Link other) {
        return ref.equalsIgnoreCase(other.ref);
    }

    @Override
    public boolean equals(Object obj) {
        if (this == obj) {
            return true;
        }
        if (!(obj instanceof Link)) {
            return false;
        }
        return equals((Link) obj);
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
