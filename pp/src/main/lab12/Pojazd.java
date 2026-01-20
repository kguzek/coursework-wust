package lab12;

public class Pojazd {
    private final String make;
    private final String model;
    private final String fuelType;

    public Pojazd(String make, String model, String fuelType) {
        this.make = make;
        this.model = model;
        this.fuelType = fuelType;
    }

    public String getMake() {
        return make;
    }
    
    public String getModel() {
        return model;
    }

    public String getFuelType() {
        return fuelType;
    }

    public void drukuj() {
        System.out.println(this.getClass().getName() + " " + this.getMake() + " " + this.getModel() + ", " + this.getFuelType());
    }
}
