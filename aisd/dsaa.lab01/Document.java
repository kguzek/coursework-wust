package dsaa.lab01;

import java.util.Scanner;

public class Document {
    private static final String LINK_PREFIX = "link=";

    public static void loadDocument(String name, Scanner scan) {
        String line = "";
        while (!line.equals("eod")) {
            line = scan.nextLine();
            String[] words = line.split(" ");
            for (String word : words) {
                if (!word.toLowerCase().startsWith(LINK_PREFIX)) {
                    continue;
                }
                String link = word.substring(LINK_PREFIX.length());
                if (!correctLink(link)) {
                    continue;
                }
                System.out.println(link.toLowerCase());
            }
        }
    }

    // accepted only small letters, capital letters, digits and '_' (except the first character)
    public static boolean correctLink(String link) {
        if (link.isEmpty()) {
            return false;
        }
        if (!Character.isLetter(link.charAt(0))) {
            return false;
        }
        for (int i = 1; i < link.length(); i++) {
            char c = link.charAt(i);
            if (!Character.isLetter(c) && !Character.isDigit(c) && c != '_') {
                return false;
            }
        }
        return true;
    }

}
