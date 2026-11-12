#include <LiquidCrystal_I2C.h>

#define RED_BUTTON 2
#define GREEN_BUTTON 4

LiquidCrystal_I2C lcd(0x27, 16, 2);

void setup()
{
  lcd.init();
  lcd.clear();

  pinMode(RED_BUTTON, INPUT_PULLUP);
  pinMode(GREEN_BUTTON, INPUT_PULLUP);

  Serial.begin(2000000);
  while (!Serial)
    ;
}

void loop()
{
  Serial.print("red:");
  Serial.print(!digitalRead(RED_BUTTON));
  Serial.print(" green:");
  Serial.println(!digitalRead(GREEN_BUTTON));
  delay(10);
}
