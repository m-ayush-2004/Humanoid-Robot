//#include <ArduinoHardware.h>
//#include <ArduinoTcpHardware.h>
//  Make sure you have the Adafruit servo driver library installed >>>>> https://github.com/adafruit/Adafruit-PWM-Servo-Driver-Library
//  X-axis joystick pin: A1
//  Y-axis joystick pin: A0
//  Trim potentiometer pin: A2
//  Button pin: 2

#include <ros.h>
#include <Wire.h>
#include <std_msgs/String.h>
#include <Adafruit_PWMServoDriver.h>

ros::NodeHandle nh;
Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();

#define SERVOMIN  140 // this is the 'minimum' pulse length count (out of 4096)
#define SERVOMAX  520 // this is the 'maximum' pulse length count (out of 4096)

// our servo # counter
uint8_t servonum = 0;

void callbackFunction(const std_msgs:: String &msg);

ros::Subscriber<std_msgs:: String> sub("sender", &callbackFunction);



int trimval;

const int analogInPin = A0;
int sensorValue = 0;
int outputValue = 0;
int switchval = 0;

void setup() {
  Serial.begin(9600);
  Serial.println("8 channel Servo test!");
  pinMode(analogInPin, INPUT);
 
  pwm.begin();
  
  pwm.setPWMFreq(60);  // Analog servos run at ~60 Hz updates

  delay(10);
  nh.initNode();
  nh.subscribe(sub);
}

// you can use this function if you'd like to set the pulse length in seconds
// e.g. setServoPulse(0, 0.001) is a ~1 millisecond pulse width. its not precise!
void setServoPulse(uint8_t n, double pulse) {
  double pulselength;
  
  pulselength = 1000000;   // 1,000,000 us per second
  pulselength /= 60;   // 60 Hz
  Serial.print(pulselength); Serial.println(" us per period"); 
  pulselength /= 4096;  // 12 bits of resolution
  Serial.print(pulselength); Serial.println(" us per bit"); 
  pulse *= 1000000;  // convert to us
  pulse /= pulselength;
  Serial.println(pulse);

}

void loop() {
  nh.spinOnce();
  delay(5);

}

static uint32_t curr = millis();
void set_location(int x ,int y){
  int lexpulse;
int rexpulse;

int leypulse;
int reypulse;

int uplidpulse;
int lolidpulse;
int altuplidpulse;
int altlolidpulse;
    lexpulse = map(x,780, 30, 220, 440);
    rexpulse = lexpulse;

    switchval = digitalRead(2);
    
    
    leypulse = map(y, 450,0, 250, 500);
    reypulse = map(y, 450,0, 400, 280);

  trimval = analogRead(A2);
    trimval=map(trimval, 320, 580, -40, 40);
     uplidpulse = map(y, 450,0, 400, 280);
        uplidpulse -= (trimval-40);
          uplidpulse = constrain(uplidpulse, 280, 400);
     altuplidpulse = 680-uplidpulse;

     lolidpulse = map(y, 450,0, 410, 280);
       lolidpulse += (trimval/2);
         lolidpulse = constrain(lolidpulse, 280, 400);      
     altlolidpulse = 680-lolidpulse;
 
    
      pwm.setPWM(0, 0, lexpulse);
      pwm.setPWM(1, 0, leypulse);
      
      if(millis()-curr >=2000){
      pwm.setPWM(2, 0, 400);
      pwm.setPWM(3, 0, 240);
      pwm.setPWM(4, 0, 240);
      pwm.setPWM(5, 0, 400);
      delay(100);
      pwm.setPWM(2, 0, uplidpulse);
      pwm.setPWM(3, 0, lolidpulse);
      pwm.setPWM(4, 0, altuplidpulse);
      pwm.setPWM(5, 0, altlolidpulse);
      curr = millis();
      }


          Serial.println(trimval);
}

void callbackFunction(const std_msgs:: String &msg){
  String str = String(msg.data);
  int idx = str.indexOf(',');
  int dat[2];
  dat[0]= (str.substring(0,idx)).toInt();
  dat[1]= (str.substring(idx+1)).toInt();
  set_location(dat[0] ,dat[1]);
}