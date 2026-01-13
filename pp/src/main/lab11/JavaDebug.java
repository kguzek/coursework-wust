import java.lang.reflect.Field;

class JavaDebug {
    public void fields(Object obj) {
        if (obj == null) {
            System.out.println("Przekazano null");
            return;
        }

        Class<?> klasa = obj.getClass();
        Field[] pola = klasa.getDeclaredFields();

        System.out.println("Klasa: " + klasa.getName());
        System.out.println("Lista pól:");

        for (Field pole : pola) {
            String nazwa = pole.getName();
            String typ = pole.getType().getName();

            Object value;
            pole.setAccessible(true);
            try {
                value = pole.get(obj);
            } catch (IllegalAccessException e) {
                value = "[brak dostępu]";
            } catch (Exception e) {
                value = "[niedostępne - " + e.getClass().getSimpleName() + "]";
            }
            System.out.println("  - Nazwa: " + nazwa + ", Typ: " + typ + ", Wartość: " + value);
        }
    }
}

