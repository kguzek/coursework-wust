#define LED_RED 6
#define LED_GREEN 5
#define LED_BLUE 3

#define RED_BUTTON 2
#define GREEN_BUTTON 4

int leds[] = {LED_RED, LED_GREEN, LED_BLUE};
int color = 0;
bool ledOn = true;

bool lastRed = HIGH;
bool lastGreen = HIGH;

void setup()
{
  for (int i = 0; i < 3; i++)
    pinMode(leds[i], OUTPUT);

  pinMode(RED_BUTTON, INPUT_PULLUP);
  pinMode(GREEN_BUTTON, INPUT_PULLUP);
}

void loop()
{
  bool red = digitalRead(RED_BUTTON);
  bool green = digitalRead(GREEN_BUTTON);

  if (red == LOW && lastRed == HIGH)
    ledOn = !ledOn;

  if (green == LOW && lastGreen == HIGH && ledOn)
    color = (color + 1) % 3;

  lastRed = red;
  lastGreen = green;

  for (int i = 0; i < 3; i++)
    digitalWrite(leds[i], ledOn && i == color);

  delay(20);
}
