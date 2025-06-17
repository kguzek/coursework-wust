package dsaa.lab13;

import java.util.LinkedList;
import java.util.Scanner;

@SuppressWarnings("DuplicatedCode")
public class Main {

    static Scanner scan; // for input stream

    public static void main(String[] args) {
        System.out.println("START");
        scan = new Scanner(System.in);
        boolean halt = false;
        while (!halt) {
            String line = scan.nextLine();
            // empty line and comment line - read next line
            if (line.isEmpty() || line.charAt(0) == '#') continue;
            // copy line to output (it is easier to find a place of a mistake)
            System.out.println("!" + line);
            String[] word = line.split(" ");
            // ha
            if (word[0].equalsIgnoreCase("ha") && word.length == 1) {
                halt = true;
                continue;
            }
            // convexhull <nrOfPoints>
            if (word[0].equalsIgnoreCase("convexhull") && word.length == 2) {
                int nrOfPoints = Integer.parseInt(word[1]);
                LinkedList<Point> points = PointsReader.load(scan, nrOfPoints);
                LinkedList<Point> result = ConvexHull.solve(points);
                System.out.println(result);
                continue;
            }
            System.out.println("Wrong command");
        }
        System.out.println("END OF EXECUTION");
        scan.close();
    }

}
