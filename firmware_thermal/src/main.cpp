#include <Arduino.h>

#define NUM_H_BRUECKEN 2
uint8_t pin_clockwise[] = {7,4};
uint8_t pin_counterclockwise[] = {8,9};
uint8_t pin_pwm[] = {5, 6};

void setup() {
  Serial.begin(115200);

  for(int8_t i=0;i<NUM_H_BRUECKEN;i++) {
    Serial.print("initialize pins");
    pinMode(pin_clockwise[i], OUTPUT);
    digitalWrite(pin_clockwise[i], LOW);
    pinMode(pin_counterclockwise[i], OUTPUT);
    digitalWrite(pin_counterclockwise[i], LOW);
    pinMode(pin_pwm[i], OUTPUT);
    analogWrite(pin_pwm[i], 0);
  }
  delay(100);
  Serial.print("> ");
}

String inputString = "";
void interpretCommand(){

    int8_t h_brueke = inputString[0]-48;
    String sub = inputString.substring(1, inputString.length());
    sub.trim();
    uint8_t pwm = sub.toInt();
    if(h_brueke<0 || h_brueke>NUM_H_BRUECKEN-1){
      return;
    }

    if(pwm > 0){ // peltier elment anschluss: schwarz auf ausgang A und rot bei ausgang B
      // dann wird die seite mit dem Schriftzug kalt 
      digitalWrite(pin_clockwise[h_brueke], LOW);
      digitalWrite(pin_counterclockwise[h_brueke], HIGH);
      analogWrite(pin_pwm[h_brueke], pwm);
      
      Serial.print("Hbruecke ");
      Serial.print(h_brueke);
      Serial.print(" turned on with pwm ");
      Serial.println(pwm);
    }else{
      digitalWrite(pin_clockwise[h_brueke], LOW);
      digitalWrite(pin_counterclockwise[h_brueke], LOW);
      analogWrite(pin_pwm[h_brueke], 0);
      Serial.print("Hbruecke ");
      Serial.print(h_brueke);
      Serial.println(" turned off");
    }
}


void loop() { // 1 25\n

  int inInt = Serial.read();
  if(inInt!=-1){
    char inChar = (char)inInt;
    if (inChar == '\n' || inChar == '\r'){
      if(inputString.length()>2){
          interpretCommand();
          inputString.remove(0);
          
      }
      if(inChar=='\n'){
        Serial.print("\n> ");
      }
    }else{
      inputString += inChar;
      Serial.print(inChar);
    }
  }
  
}