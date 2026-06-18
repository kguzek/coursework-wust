package dsaa.lab12;

import java.util.Scanner;

public class LinesReader {
    String concatLines(int howMany, Scanner scanner) {
        //noinspection StringBufferMayBeStringBuilder
        StringBuffer buffer = new StringBuffer();
        for (int i = 0; i < howMany; i++) {
            buffer.append(scanner.nextLine());
        }
        return buffer.toString();
    }
}
