#include <LiquidCrystal_I2C.h>

#define POTENTIOMETER A0

LiquidCrystal_I2C lcd(0x27, 16, 2);

void setup()
{
  lcd.init();
  lcd.clear();

  Serial.begin(9600);
  while (!Serial)
    ;
}

void loop()
{
  Serial.print("min:0 max:1023 adc:");
  Serial.println(analogRead(POTENTIOMETER));
  delay(10);
}
