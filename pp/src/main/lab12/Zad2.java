package lab12;

public class Zad2 {
    public static void main(String[] args) {
        Pojazd[] samochody = new Samochod[]{
                new Samochod("lamborghini", "gallardo"),
                new ElektrycznySamochod("hyundai", "kona"),
                new Samochod("iveco", "daily", "diesel")
        };

        samochody[0] = new Pojazd("rover", "umr 809", "manual");
        for (Pojazd samochod : samochody) {
            samochod.drukuj();
        }
    }
}
