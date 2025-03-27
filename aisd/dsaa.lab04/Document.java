package dsaa.lab04;

import java.util.ListIterator;
import java.util.Scanner;

public class Document {
    public String name;
    public TwoWayCycledOrderedListWithSentinel<Link> link;
    private static final String LINK_PREFIX = "link=";

    public Document(String name, Scanner scan) {
        this.name = name.toLowerCase();
        link = new TwoWayCycledOrderedListWithSentinel<>();
        load(scan);
    }

    @SuppressWarnings("DuplicatedCode")
    public void load(Scanner scan) {
        String line = "";
//        while (!line.equals("eod")) {
//            line = scan.nextLine();
//            String[] words = line.split(" ");
//            for (String word : words) {
//                if (!word.toLowerCase().startsWith(LINK_PREFIX)) {
//                    continue;
//                }
//                String link = word.substring(LINK_PREFIX.length());
//                if (!correctLink(link)) {
//                    continue;
//                }
//                this.link.add(new .Link(link));
////                System.out.println(link.toLowerCase());
//            }
//        }
    }

    public static boolean isCorrectId(String id) {
        //TODO
        return false;
    }

    // accepts only small letters, capital letters, digits and '_' (except the first character)
    static Link createLink(String link) {
        //TODO
        return null;
    }

    @Override
    public String toString() {
        String retStr = "Document: " + name;
        //TODO
        return retStr;
    }

    public String toStringReverse() {
        String retStr = "Document: " + name;
        ListIterator<Link> iter = link.listIterator();
        while (iter.hasNext()) iter.next();
        //TODO
        while (iter.hasPrevious()) {
        }
        return retStr;
    }
}

