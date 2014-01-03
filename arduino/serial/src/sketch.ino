int analogPinLDR = 0;
int valLDR = 0;
int analogPinLM35 = 1;

//Number of pulses, used to measure energy.
  long pulseCount = 0;   
//Used to measure power.
  unsigned long pulseTime,lastTime;
//power and energy
  double power, elapsedkWh;
//Number of pulses per wh - found or set on the meter.
  int ppwh = 1; //1000 pulses/kwh = 1 pulse per wh


int led = 13;

// include the library code:
#include <LiquidCrystal.h>

// initialize the library with the numbers of the interface pins
LiquidCrystal lcd(27, 28, 29, 30, 31, 32);

void setup()
{
    Serial.begin(9600);
    pinMode(led, OUTPUT);
  // set up the LCD's number of columns and rows: 
  lcd.begin(16, 2);
  // Print a message to the LCD.
  lcd.print("Initializing...!");

}

void loop()
{

    valLDR = analogRead(analogPinLDR);
    if (valLDR >= 280) {
        digitalWrite(led, HIGH);
        calculatePulse();
    }
    delay(20);
    digitalWrite(led, LOW);

}

void getTemperature()
{
    int reading = analogRead(analogPinLM35);
    float temperature = (reading * 0.0049) * 100;
    /*
    lcd.setCursor(0, 1);
    lcd.print("Temp: ");
    lcd.print(temperature);
    lcd.print((char)223);
    lcd.print("C");
    */
    Serial.print("Temperature: ");
    Serial.println(temperature);
}

void calculatePulse()
{
  //used to measure time between pulses.
  lastTime = pulseTime;
  pulseTime = micros();
  
  //Calculate power
  power = (3600000000.0 / (pulseTime - lastTime))/ppwh;
  
  //Find kwh elapsed
  //elapsedkWh = (1.0*pulseCount/(ppwh*1000)); //multiply by 1000 to pulses per wh to kwh convert wh to kwh
 
  if (power < 20000) {
    //pulseCounter
    pulseCount++;
 
    //Print the values.
    Serial.print("PulsePower: ");
    Serial.println(power);

    if (pulseCount == 1000) {
      Serial.println("kWh: 1");
    }
    // set the cursor to column 0, line 1
    // (note: line 1 is the second row, since counting begins with 0):
    lcd.setCursor(0, 0);
    lcd.print("Power: ");
    lcd.print(power);
    lcd.print("W");
  
  }

  //getTemperature();
}

