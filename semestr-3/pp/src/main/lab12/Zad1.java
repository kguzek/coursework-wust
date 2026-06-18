package lab12;

public class Zad1 {
    public static void main(String[] args) {
        Pojazd[] pojazdy = new Pojazd[]{
                new Samochod("ferrari", "laferrari"),
                new Samochod("dodge", "challenger", "petrol"),
                new ElektrycznySamochod("tesla", "model x"),
                new Pojazd("bmx", "skyway", "manual")
        };
        for (Pojazd pojazd : pojazdy) {
            pojazd.drukuj();
        }
    }
}
