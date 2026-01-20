package lab12;

import java.util.Arrays;
import java.util.Collection;

public class Zad3 {
    public static void main(String[] args) {
        Collection<Pojazd> pojazdy = Arrays.asList(
                new Samochod("ferrari", "laferrari"),
                new Samochod("lamborghini", "gallardo"),
                new ElektrycznySamochod("tesla", "model x"),
                new ElektrycznySamochod("hyundai", "kona"),
                new Pojazd("bmx", "skyway", "manual"),
                new Pojazd("rover", "umr 809", "manual")
        );
        Drukarka.drukuj(pojazdy);
    }
}
