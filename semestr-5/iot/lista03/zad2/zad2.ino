#include <LiquidCrystal_I2C.h>

#define LED_RED 6
#define LED_GREEN 5
#define LED_BLUE 3

LiquidCrystal_I2C lcd(0x27, 16, 2);

int led[] = {LED_RED, LED_GREEN, LED_BLUE};
unsigned long period[] = {900UL, 1000UL, 1100UL};
int ledState[] = {LOW, LOW, LOW};
unsigned long lastChange[] = {0UL, 0UL, 0UL};

void blinkLed(int i)
{
  if (millis() - lastChange[i] >= period[i])
  {
    if (ledState[i] == HIGH)
      ledState[i] = LOW;
    else
      ledState[i] = HIGH;

    digitalWrite(led[i], ledState[i]);
    lastChange[i] += period[i];
  }
}

void setup()
{
  lcd.init();
  lcd.clear();

  pinMode(LED_RED, OUTPUT);
  pinMode(LED_GREEN, OUTPUT);
  pinMode(LED_BLUE, OUTPUT);

  digitalWrite(LED_RED, LOW);
  digitalWrite(LED_GREEN, LOW);
  digitalWrite(LED_BLUE, LOW);
}

void loop()
{
  blinkLed(0);
  blinkLed(1);
  blinkLed(2);
}
