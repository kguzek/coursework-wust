trait Debug {
  def debugName(): Unit = {
    println(s"Klasa: ${this.getClass.getName}")
  }
}

class Samochod(val marka: String, val model: String, val rokProdukcji: Int, val cena: Double) extends Debug

val auto1 = new Samochod("Toyota", "Corolla", 2020, 85000.0)
auto1.debugName()

val auto2 = new Samochod("BMW", "X5", 2022, 250000.0)
auto2.debugName()

class Motocykl(val marka: String) extends Debug
val motor = new Motocykl("Harley")
motor.debugName()

val obiekt = new Debug {}
obiekt.debugName()

val auto3 = new Samochod("Fiat", "126p", 1985, 5000.0)
auto3.debugName()
