#include <LiquidCrystal_I2C.h>

#define LED_RED 6
#define LED_GREEN 5
#define LED_BLUE 3

LiquidCrystal_I2C lcd(0x27, 16, 2);

const int leds[] = {LED_RED, LED_GREEN, LED_BLUE};

void setup()
{
  lcd.init();
  lcd.clear();

  for (int led : leds)
  {
    pinMode(led, OUTPUT);
    analogWrite(led, 0);
  }

  Serial.begin(9600);
  while (!Serial)
    ;
}

void loop()
{
  if (Serial.available() > 0)
  {
    String command = Serial.readStringUntil('\n');
    command.trim();

    int values[3];
    if (sscanf(command.c_str(), "%d %d %d", &values[0], &values[1], &values[2]) != 3)
    {
      Serial.println("Usage: <red> <green> <blue> (0-255)");
      return;
    }

    for (int i = 0; i < 3; i++)
    {
      values[i] = constrain(values[i], 0, 255);
      analogWrite(leds[i], values[i]);
    }

    Serial.println(String("RGB ") + values[0] + " " + values[1] + " " + values[2]);
  }
}
