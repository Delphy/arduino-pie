#include <Arduino.h>

void setup();
void loop();
void calculatePulse();
#line 1 "src/sketch.ino"
int analogPin = 0;
int val = 0;

//Number of pulses, used to measure energy.
  long pulseCount = 0;   
//Used to measure power.
  unsigned long pulseTime,lastTime;
//power and energy
  double power, elapsedkWh;
//Number of pulses per wh - found or set on the meter.
  int ppwh = 1; //1000 pulses/kwh = 1 pulse per wh
  int LDR_Pin = A0; //analog pin 0

int led = 13;

void setup()
{
    Serial.begin(9600);
    pinMode(led, OUTPUT);
}

void loop()
{

    val = analogRead(analogPin);
    if (val >= 280) {
        digitalWrite(led, HIGH);
        calculatePulse();
    }
    delay(20);
    digitalWrite(led, LOW);
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

  }

  //Serial.print(" ");
  //Serial.println(elapsedkWh,3);
}

