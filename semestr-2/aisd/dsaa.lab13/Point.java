package dsaa.lab13;

public class Point {
    public long x;
    public long y;

    public Point(int x, int y) {
        this.x = x;
        this.y = y;
    }

    /**
     * Constructs two vectors from the current point to each of the provided points and calculates the cross-product of those two vectors.
     */
    public float crossProduct(Point a, Point b) {
        return (a.x - this.x) * (b.y - this.y) - (a.y - this.y) * (b.x - this.x);
    }

    @Override
    public String toString() {
        return String.format("(%s, %s)", x, y);
    }
}
