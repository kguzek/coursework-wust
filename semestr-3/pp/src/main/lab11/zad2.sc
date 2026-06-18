trait Debug {
  def debugVars(): Unit = {
    val klasa = this.getClass
    val pola = klasa.getDeclaredFields

    println(s"Klasa: ${klasa.getName}")
    println("Lista pól:")

    for (pole <- pola) {
      pole.setAccessible(true)
      val nazwa = pole.getName
      val typ = pole.getType.getName
      val wartosc = pole.get(this)

      println(s"  - Nazwa: $nazwa, Typ: $typ, Wartość: $wartosc")
    }
  }
}

class Samochod(val marka: String, val model: String, val rokProdukcji: Int, val cena: Double) extends Debug

val auto1 = new Samochod("Toyota", "Corolla", 2020, 85000.0)
auto1.debugVars()

val auto2 = new Samochod("BMW", "X5", 2022, 250000.0)
auto2.debugVars()

val auto3 = new Samochod("Fiat", "126p", 1985, 0.0)
auto3.debugVars()

class SamochodRozszerzony(marka: String, model: String, rok: Int, cena: Double, val kolor: String)
  extends Samochod(marka, model, rok, cena)
val auto4 = new SamochodRozszerzony("Audi", "A4", 2021, 150000.0, "Czerwony")
auto4.debugVars()

val auto5 = new Samochod("Tesla", "Model 3", -1, 200000.0)
auto5.debugVars()
