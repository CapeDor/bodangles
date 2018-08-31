#include <Wire.h>
#include <Indio.h>
#include <SimpleModbusSlave.h>
#include <UC1701.h>
#include <Adafruit_SleepyDog.h>

#define TxEnablePin 9
#define   baud 9600
#define   SlaveID 14

//[oxy_send, press_send, online, sol_state, o2_alarm, float_alarm]
#define   HOLDING_REGS_SIZE 6

static UC1701 lcd;

unsigned int holdingRegs[HOLDING_REGS_SIZE];

const int buttonEnterPin = 24;

const int LED_1 = 3; //alarm LED
const int LED_2 = 2; //online LED


bool sol_state = 0;
bool float_state = 0;
bool o2_alarm = 0;
bool float_alarm = 0;

void setup() {
  lcd.begin();
  lcd.clear();
  lcd.setCursor(1, 1);
  lcd.print("Tank:4 SID:");
  lcd.print(SlaveID);

  analogWrite(26, 100);

  Indio.digitalMode(1, OUTPUT);
  Indio.digitalMode(2, OUTPUT);
  Indio.digitalMode(3, OUTPUT);
  Indio.digitalMode(4, INPUT);
  Indio.digitalMode(5, INPUT);
  Indio.digitalMode(6, OUTPUT);
  Indio.digitalMode(7, OUTPUT);
  Indio.digitalMode(8, OUTPUT);

  Indio.digitalWrite(1, LOW);
  Indio.digitalWrite(2, LOW);
  Indio.digitalWrite(3, LOW);
  Indio.digitalWrite(4, LOW);
  Indio.digitalWrite(5, LOW);
  Indio.digitalWrite(6, LOW);
  Indio.digitalWrite(7, LOW);
  Indio.digitalWrite(8, LOW);

  Indio.setADCResolution(16);
  Indio.analogReadMode(1, mA);

  int timer = Watchdog.enable(3000);

  modbus_configure(&Serial, baud, SERIAL_8N2, SlaveID, TxEnablePin, HOLDING_REGS_SIZE, holdingRegs);
  modbus_update_comms(baud, SERIAL_8N2, SlaveID);
}

void loop() {

  bool pin = digitalRead(buttonEnterPin);
  if(pin == LOW){
    delay(20000);
  }

//[oxy_send, press_send, online, sol_state, o2_alarm, float_alarm]
  modbus_update();

  float sat_mA = Indio.analogRead(1);
  float sat = 12.5*(sat_mA) - 50;
  int oxy_send = (sat*100);

  //250psi unit
  float pres_mA = Indio.analogRead(2);
  float pressure = (2.5676*pres_mA) - 5.1082;
  int pres_send = 0;
  
  if (pressure<=0){
    pres_send = 0;
    }
    else{
      pres_send = (pressure*1000);
    }
    
  bool online = !Indio.digitalRead(4);
  float_state = Indio.digitalRead(5);

  if((sat<=80)&&(online == 1)){
    o2_alarm = 1;
  }

  if((sat>=100)&&(online == 1)){
    o2_alarm = 0;
  }
  
  if((float_state == 1)&&(online == 1)){
    float_alarm = 1;
  }
  else{
    float_alarm = 0;
  }
  
  if((float_alarm == 1)||(o2_alarm == 1)){
    sol_state = 1;
    Indio.digitalWrite(LED_2,HIGH);
  }
  else{
    sol_state = 0;
    Indio.digitalWrite(LED_2,LOW);
  }

  if(online == 1){
    Indio.digitalWrite(LED_1, HIGH);
  }
  else{
    Indio.digitalWrite(LED_1,LOW);
    }

  if(sol_state == 1){
    Indio.digitalWrite(1, HIGH);
  }
  else{
    Indio.digitalWrite(1,LOW);
    }

//[oxy_send, press_send, online, sol_state, o2_alarm, float_alarm]
  holdingRegs[0] = oxy_send;
  holdingRegs[1] = pres_send;
  holdingRegs[2] = online;
  holdingRegs[3] = sol_state;
  holdingRegs[4] = o2_alarm;
  holdingRegs[5] = float_alarm;


  SerialUSB.println(holdingRegs[0]);
  SerialUSB.println(holdingRegs[1]);
  SerialUSB.println(holdingRegs[2]);
  SerialUSB.println(holdingRegs[3]);
  SerialUSB.println(holdingRegs[4]);
  SerialUSB.println(holdingRegs[5]);
  SerialUSB.println("---------------");

  lcd.setCursor(1, 2);
  lcd.print("%sat: ");
  lcd.print(sat);
  
  lcd.setCursor(1, 3);
  lcd.print("pressure: ");
  lcd.print(pressure);

  lcd.setCursor(1, 4);
  lcd.print("sol_state: ");
  lcd.print(sol_state);

  lcd.setCursor(1, 5);
  lcd.print("online: ");
  lcd.print(online);

  lcd.setCursor(1, 6);
  lcd.print("ALARM[o2,float]:[");
  lcd.print(o2_alarm);
  lcd.print(",");
  lcd.print(float_state);
  lcd.print("]");
  
  Watchdog.reset();
}
