package dsaa.lab01;

public class Drawer {
    private static void drawLine(int n, char ch) {
        for (int i = 0; i < n; i++) {
            System.out.print(ch);
        }
    }

    public static void drawPyramid(int rows) {
        drawPyramid(rows, rows);
    }

    private static void drawPyramid(int rows, int cols) {
        for (int i = 0; i < rows; i++) {
            int dots = cols - i - 1;
            drawLine(dots, '.');
            drawLine(1 + i * 2, 'X');
            drawLine(dots, '.');
            System.out.println();
        }
    }

    public static void drawChristmasTree(int n) {
        for (int i = 0; i <= n; i++) {
            drawPyramid(i, n);
        }
    }
}
