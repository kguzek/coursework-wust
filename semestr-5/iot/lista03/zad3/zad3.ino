#include <LiquidCrystal_I2C.h>

#define RED_BUTTON 2
#define GREEN_BUTTON 4

#define DEBOUNCE_PERIOD 10UL

LiquidCrystal_I2C lcd(0x27, 16, 2);

int buttons[] = {RED_BUTTON, GREEN_BUTTON};
int debounced_button_state[] = {HIGH, HIGH};
int previous_reading[] = {HIGH, HIGH};
unsigned long last_change_time[] = {0UL, 0UL};

bool running = false;
unsigned long startTime = 0UL;
unsigned long accumulated = 0UL;
unsigned long shownSeconds = 0UL;

bool isButtonPressed(int i)
{
  bool isPressed = false;
  int current_reading = digitalRead(buttons[i]);

  if (previous_reading[i] != current_reading)
    last_change_time[i] = millis();

  if (millis() - last_change_time[i] > DEBOUNCE_PERIOD)
  {
    if (current_reading != debounced_button_state[i])
    {
      if (debounced_button_state[i] == HIGH && current_reading == LOW)
        isPressed = true;

      debounced_button_state[i] = current_reading;
    }
  }

  previous_reading[i] = current_reading;

  return isPressed;
}

void printTwoDigits(unsigned long value)
{
  if (value < 10)
    lcd.print('0');
  lcd.print(value);
}

void showTime(unsigned long seconds)
{
  lcd.setCursor(4, 1);
  printTwoDigits(seconds / 3600);
  lcd.print(':');
  printTwoDigits(seconds / 60 % 60);
  lcd.print(':');
  printTwoDigits(seconds % 60);
}

void setup()
{
  pinMode(RED_BUTTON, INPUT_PULLUP);
  pinMode(GREEN_BUTTON, INPUT_PULLUP);

  lcd.init();
  lcd.backlight();

  lcd.setCursor(5, 0);
  lcd.print("Stoper");
  showTime(0);
}

void loop()
{
  if (isButtonPressed(1))
  {
    if (running)
      accumulated += millis() - startTime;
    else
      startTime = millis();

    running = !running;
  }

  if (isButtonPressed(0))
  {
    running = false;
    accumulated = 0UL;
  }

  unsigned long elapsed = accumulated;
  if (running)
    elapsed += millis() - startTime;

  unsigned long seconds = elapsed / 1000UL;
  if (seconds != shownSeconds)
  {
    shownSeconds = seconds;
    showTime(seconds);
  }
}
