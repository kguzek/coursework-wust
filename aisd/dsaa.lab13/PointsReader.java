package dsaa.lab13;

import java.util.LinkedList;
import java.util.Scanner;

public class PointsReader {
    static LinkedList<Point> load(Scanner scan, int numPoints) {
        LinkedList<Point> points = new LinkedList<>();
        for (int i = 0; i < numPoints; i++) {
            String line = scan.nextLine();
            String[] tokens = line.split(" ");
            int x = Integer.parseInt(tokens[0]);
            int y = Integer.parseInt(tokens[1]);
            points.add(new Point(x, y));
        }
        return points;
    }
}
