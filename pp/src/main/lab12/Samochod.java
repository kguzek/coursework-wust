package lab12;

public class Samochod extends Pojazd {

    public Samochod(String make, String model) {
        super(make, model, "petrol");
    }

    public Samochod(String make, String model, String fuelType) {
        super(make, model, fuelType);
    }
}
