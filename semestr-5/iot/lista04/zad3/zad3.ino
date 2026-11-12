#include <LiquidCrystal_I2C.h>

#define POTENTIOMETER A0
#define V_REF 5.0

LiquidCrystal_I2C lcd(0x27, 16, 2);

int shownValue = -1;

void setup()
{
  lcd.init();
  lcd.clear();
  lcd.backlight();

  lcd.print("ADC:");
  lcd.setCursor(0, 1);
  lcd.print("U:");
}

void loop()
{
  int value = analogRead(POTENTIOMETER);
  if (value == shownValue)
    return;

  shownValue = value;

  lcd.setCursor(5, 0);
  lcd.print(value);
  lcd.print("    ");

  lcd.setCursor(5, 1);
  lcd.print(value * V_REF / 1024, 3);
  lcd.print(" V");
}
