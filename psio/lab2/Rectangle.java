package geometry;

public class Rectangle {

    private int x1, y1, x2, y2;

    private void init(int x1, int y1, int x2, int y2) {
        this.x1 = x1;
        this.y1 = y1;
        this.x2 = x2;
        this.y2 = y2;
    }

    public Rectangle() {
        init(0, 0, 1, 1);
    }

    public Rectangle(int x1, int y1, int x2, int y2) {
        this();
        init(x1, y1, x2, y2);
    }

    private int getSideLength(int a, int b) {
        return Math.abs(a - b);
    }

    public int getPerimeter() {
        return 2 * getSideLength(x1, x2) + 2 * getSideLength(y1, y2);
    }

    public int getArea() {
        return getSideLength(x1, x2) * getSideLength(y1, y2);
    }
}
