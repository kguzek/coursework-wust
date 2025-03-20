package dsaa.lab03;

public class Link {
    public String ref;

    public Link(String ref) {
        this.ref = ref;
    }
    // in the future there will be more fields

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
}
