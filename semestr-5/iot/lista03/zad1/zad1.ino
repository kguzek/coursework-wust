#include <LiquidCrystal_I2C.h>

#define LED_RED 6
#define LED_GREEN 5
#define LED_BLUE 3

#define RED_BUTTON 2
#define GREEN_BUTTON 4

#define DEBOUNCE_PERIOD 10UL

LiquidCrystal_I2C lcd(0x27, 16, 2);

int led[] = {LED_RED, LED_GREEN, LED_BLUE};
int led_index = 0;

int buttons[] = {RED_BUTTON, GREEN_BUTTON};
int debounced_button_state[] = {HIGH, HIGH};
int previous_reading[] = {HIGH, HIGH};
unsigned long last_change_time[] = {0UL, 0UL};

bool isButtonReleased(int i)
{
  bool isReleased = false;
  int current_reading = digitalRead(buttons[i]);

  if (previous_reading[i] != current_reading)
    last_change_time[i] = millis();

  if (millis() - last_change_time[i] > DEBOUNCE_PERIOD)
  {
    if (current_reading != debounced_button_state[i])
    {
      if (debounced_button_state[i] == LOW && current_reading == HIGH)
        isReleased = true;

      debounced_button_state[i] = current_reading;
    }
  }

  previous_reading[i] = current_reading;

  return isReleased;
}

void setup()
{
  lcd.init();
  lcd.clear();

  pinMode(LED_RED, OUTPUT);
  pinMode(LED_GREEN, OUTPUT);
  pinMode(LED_BLUE, OUTPUT);

  digitalWrite(LED_RED, HIGH);
  digitalWrite(LED_GREEN, LOW);
  digitalWrite(LED_BLUE, LOW);

  pinMode(RED_BUTTON, INPUT_PULLUP);
  pinMode(GREEN_BUTTON, INPUT_PULLUP);
}

void loop()
{
  bool redReleased = isButtonReleased(0);
  bool greenReleased = isButtonReleased(1);

  if (redReleased || greenReleased)
  {
    digitalWrite(led[led_index], LOW);
    led_index = (led_index + 1) % 3;
    digitalWrite(led[led_index], HIGH);
  }
}
