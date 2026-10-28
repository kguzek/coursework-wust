#define LED_RED 6
#define LED_GREEN 5
#define LED_BLUE 3

const int leds[3] = {LED_RED, LED_GREEN, LED_BLUE};

int current = 0;

void setup()
{
  pinMode(LED_RED, OUTPUT);
  pinMode(LED_GREEN, OUTPUT);
  pinMode(LED_BLUE, OUTPUT);

  analogWrite(LED_RED, 255);
  analogWrite(LED_GREEN, 0);
  analogWrite(LED_BLUE, 0);
}

void loop()
{
  int next = (current + 1) % 3;

  for (int i = 0; i <= 255; i++)
  {
    analogWrite(leds[current], 255 - i);
    analogWrite(leds[next], i);
    delay(10);
  }

  current = next;
}
