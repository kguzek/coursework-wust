public class Lab11Zad3 {
    public static void main(String[] args) {
        JavaDebug debug = new JavaDebug();

        System.out.println("Samochód Toyota");
        JavaSamochod auto1 = new JavaSamochod("Toyota", "Corolla", 2020, 85000.0);
        debug.fields(auto1);

        System.out.println("Samochód BMW");
        JavaSamochod auto2 = new JavaSamochod("BMW", "X5", 2022, 250000.0);
        debug.fields(auto2);

        System.out.println("Samochód z zerową ceną");
        JavaSamochod auto3 = new JavaSamochod("Fiat", "126p", 1985, 0.0);
        debug.fields(auto3);

        System.out.println("Przekazanie null");
        debug.fields(null);
    }
}