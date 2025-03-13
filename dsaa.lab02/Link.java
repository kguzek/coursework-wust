package dsaa.lab02;

public class Link {
    public String ref;

    public Link(String ref) {
        this.ref = ref;
    }
    // in the future there will be more fields

    @Override
    public boolean equals(Object other) {
        if (other == null) {
            return false;
        }
        if (other.getClass() != this.getClass()) {
            return false;
        }
        Link link = (Link) other;
        return ref.equals(link.ref);
    }

}
