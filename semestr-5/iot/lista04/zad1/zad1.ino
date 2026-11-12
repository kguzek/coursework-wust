#define RED_BUTTON 2
#define GREEN_BUTTON 4

void setup()
{
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
