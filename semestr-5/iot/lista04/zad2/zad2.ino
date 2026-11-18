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

    bool valid = true;
    int digits = 0;
    for (unsigned int i = 0; i < command.length(); i++)
    {
      char c = command[i];
      if (isDigit(c))
        digits++;
      else if (c == ' ')
        digits = 0;
      else
        valid = false;

      if (digits > 3)
        valid = false;
    }

    int values[3];
    int end = 0;
    if (!valid || sscanf(command.c_str(), "%d %d %d%n", &values[0], &values[1], &values[2], &end) != 3 || end != (int)command.length())
      valid = false;

    for (int i = 0; valid && i < 3; i++)
    {
      if (values[i] > 255)
        valid = false;
    }

    if (!valid)
    {
      Serial.println("Usage: <red> <green> <blue> (0-255)");
      return;
    }

    for (int i = 0; i < 3; i++)
      analogWrite(leds[i], values[i]);

    Serial.println(String("RGB ") + values[0] + " " + values[1] + " " + values[2]);
  }
}
