package lab12;

import java.util.Collection;

public class Drukarka {
    static void drukuj(Collection<Pojazd> pojazdy) {
        for (Pojazd pojazd : pojazdy) {
            pojazd.drukuj();
        }
    }
}
