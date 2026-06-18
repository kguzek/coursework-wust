package dsaa.lab13;

import java.util.Iterator;
import java.util.LinkedList;
import java.util.Stack;

public class ConvexHull {

    public static Point getBottomPoint(LinkedList<Point> points) {
        Iterator<Point> it = points.iterator();
        Point bottomPoint = it.next();
        while (it.hasNext()) {
            Point p = it.next();
            if (p.y < bottomPoint.y || (p.y == bottomPoint.y && p.x < bottomPoint.x)) {
                bottomPoint = p;
            }
        }
        return bottomPoint;
    }

    public static LinkedList<Point> solve(LinkedList<Point> points) {
        Point bottomPoint = getBottomPoint(points);
        points.remove(bottomPoint);
        Stack<Point> stack = new Stack<>();

        points.sort((a, b) -> {
            float crossProduct = bottomPoint.crossProduct(a, b);
            return (int) (crossProduct == 0 ? (a.x == b.x ? a.y - b.y : a.x - b.x) : crossProduct * -1);
        });
        stack.push(bottomPoint);
        stack.push(points.removeFirst());

        for (Point next : points) {
            Point previous = stack.pop();
            while (!stack.isEmpty() && stack.peek().crossProduct(previous, next) <= 0) {
                previous = stack.pop();
            }
            stack.push(previous);
            stack.push(next);
        }
        return new LinkedList<>(stack);
    }
}
