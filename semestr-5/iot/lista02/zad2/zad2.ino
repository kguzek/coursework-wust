#define LED_RED 6
#define LED_GREEN 5
#define LED_BLUE 3

#define RED_BUTTON 2
#define GREEN_BUTTON 4

#define STEP 5

int brightness = 0;

void setup()
{
  pinMode(LED_RED, OUTPUT);
  pinMode(LED_GREEN, OUTPUT);
  pinMode(LED_BLUE, OUTPUT);

  digitalWrite(LED_RED, LOW);
  digitalWrite(LED_BLUE, LOW);
  analogWrite(LED_GREEN, brightness);

  pinMode(RED_BUTTON, INPUT_PULLUP);
  pinMode(GREEN_BUTTON, INPUT_PULLUP);
}

void loop()
{
  if (digitalRead(GREEN_BUTTON) == LOW)
    brightness = min(brightness + STEP, 255);

  if (digitalRead(RED_BUTTON) == LOW)
    brightness = max(brightness - STEP, 0);

  analogWrite(LED_GREEN, brightness);
  delay(20);
}
