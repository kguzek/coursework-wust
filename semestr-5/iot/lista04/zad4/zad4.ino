#define POTENTIOMETER A0

void setup()
{
  Serial.begin(9600);
  while (!Serial)
    ;
}

void loop()
{
  Serial.print("min:0 max:1023 adc:");
  Serial.println(analogRead(POTENTIOMETER));
  delay(10);
}
