#include <LiquidCrystal_I2C.h>

#define POTENTIOMETER A0
#define V_REF 5.0
#define SAMPLES 16
#define HYSTERESIS 2

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

  Serial.begin(9600);
  while (!Serial)
    ;
}

int readAveraged()
{
  long sum = 0;
  for (int i = 0; i < SAMPLES; i++)
    sum += analogRead(POTENTIOMETER);
  return (sum + SAMPLES / 2) / SAMPLES;
}

void loop()
{
  int value = readAveraged();

  Serial.print("min:0 max:1023 adc:");
  Serial.println(value);

  if (shownValue < 0 || abs(value - shownValue) > HYSTERESIS ||
      (value != shownValue && (value == 0 || value == 1023)))
  {
    shownValue = value;

    lcd.setCursor(5, 0);
    lcd.print(value);
    lcd.print("    ");

    lcd.setCursor(5, 1);
    lcd.print(value * V_REF / 1024, 3);
    lcd.print(" V");
  }

  delay(10);
}
