#include <Wire.h>

#define mpu_add 0x68 //mpu6050 address

 

long ac_x, ac_y, ac_z, gy_x, gy_y, gy_z ; //acc, gyro data 

 

int ledPin =13;

int vib =2; 
 

double angle = 0, deg ; // angle, deg data

double dgy_x ; //double type acc data

char device[]="/dev/ttyACM0";

int fd;
unsigned long baud = 9600;
double average = 0;
double sum = 0;

void setup(void) {
    

  // put your setup code here, to run once:

  Serial.begin(9600) ;  //set serial baud

  Wire.begin() ;  //set I2C

  Wire.beginTransmission(mpu_add) ;

  Wire.write(0x6B) ;

  Wire.write(0) ;

  Wire.endTransmission(true) ;

   pinMode(3, OUTPUT);
   int x;
  
  for(x=1; x<1001; x++){

      Wire.beginTransmission(mpu_add) ; //get acc data

  Wire.write(0x3B) ;  // accelerator

  Wire.endTransmission(false) ;

  Wire.requestFrom(mpu_add, 6, true) ;

  ac_x = Wire.read() << 8 | Wire.read() ;

  ac_y = Wire.read() << 8 | Wire.read() ;

  ac_z = Wire.read() << 8 | Wire.read() ;

 

  Wire.beginTransmission(mpu_add) ; //get gyro data

  Wire.write(0x43) ; // gyro 

  Wire.endTransmission(false) ;

  Wire.requestFrom(mpu_add, 6, true) ;

  gy_x = Wire.read() << 8 | Wire.read() ;

  gy_y = Wire.read() << 8 | Wire.read() ;

  gy_z = Wire.read() << 8 | Wire.read() ;

 

  deg = atan2(ac_x, ac_z) * 180 / PI ;  //rad to deg

 

  dgy_x = gy_y / 131. ;  //16-bit data to 250 deg/sec

  angle = (0.95 * (angle + (dgy_x * 0.001))) + (0.05 * deg) ; //complementary filter


    sum = sum + angle;
    average = sum/1000;
    delay(1);
    Serial.println("Sensorvalue : " +String(angle));
  }
  Serial.println("Average: " +String(average));


}
  

void loop(void) {

Wire.beginTransmission(mpu_add) ; //get acc data

  Wire.write(0x3B) ;  // accelerator

  Wire.endTransmission(false) ;

  Wire.requestFrom(mpu_add, 6, true) ;

  ac_x = Wire.read() << 8 | Wire.read() ;

  ac_y = Wire.read() << 8 | Wire.read() ;

  ac_z = Wire.read() << 8 | Wire.read() ;

 

  Wire.beginTransmission(mpu_add) ; //get gyro data

  Wire.write(0x43) ; // gyro 

  Wire.endTransmission(false) ;

  Wire.requestFrom(mpu_add, 6, true) ;

  gy_x = Wire.read() << 8 | Wire.read() ;

  gy_y = Wire.read() << 8 | Wire.read() ;

  gy_z = Wire.read() << 8 | Wire.read() ;

 

  deg = atan2(ac_x, ac_z) * 180 / PI ;  //rad to deg

 

  dgy_x = gy_y / 131. ;  //16-bit data to 250 deg/sec

  angle = (0.95 * (angle + (dgy_x * 0.001))) + (0.05 * deg) ; //complementary filter

 
if(average - angle > 30){
  Serial.println(angle);
  Serial.println("time check start");
  delay(5000);
  if(average - angle > 30){
    while(true){
      Wire.beginTransmission(mpu_add) ; //get acc data

  Wire.write(0x3B) ;  // accelerator

  Wire.endTransmission(false) ;

  Wire.requestFrom(mpu_add, 6, true) ;

  ac_x = Wire.read() << 8 | Wire.read() ;

  ac_y = Wire.read() << 8 | Wire.read() ;

  ac_z = Wire.read() << 8 | Wire.read() ;

 

  Wire.beginTransmission(mpu_add) ; //get gyro data

  Wire.write(0x43) ; // gyro 

  Wire.endTransmission(false) ;

  Wire.requestFrom(mpu_add, 6, true) ;

  gy_x = Wire.read() << 8 | Wire.read() ;

  gy_y = Wire.read() << 8 | Wire.read() ;

  gy_z = Wire.read() << 8 | Wire.read() ;

 

  deg = atan2(ac_x, ac_z) * 180 / PI ;  //rad to deg

 

  dgy_x = gy_y / 131. ;  //16-bit data to 250 deg/sec

  angle = (0.95 * (angle + (dgy_x * 0.001))) + (0.05 * deg) ; //complementary filter


      analogWrite(3, 250); //진동세기 임의의 값
      delay(50);
      analogWrite(3, 0);
      Serial.println(angle);
     Serial.println("Left_Warning");
     if(average - angle < 30) {
      break;  
     }
   }
  }
}
else if(average - angle < -30){
  Serial.println(angle);
  Serial.println("time check start");
  delay(5000);
  if(average - angle < -30){
    while(true){
      Wire.beginTransmission(mpu_add) ; //get acc data

  Wire.write(0x3B) ;  // accelerator

  Wire.endTransmission(false) ;

  Wire.requestFrom(mpu_add, 6, true) ;

  ac_x = Wire.read() << 8 | Wire.read() ;

  ac_y = Wire.read() << 8 | Wire.read() ;

  ac_z = Wire.read() << 8 | Wire.read() ;

 

  Wire.beginTransmission(mpu_add) ; //get gyro data

  Wire.write(0x43) ; // gyro 

  Wire.endTransmission(false) ;

  Wire.requestFrom(mpu_add, 6, true) ;

  gy_x = Wire.read() << 8 | Wire.read() ;

  gy_y = Wire.read() << 8 | Wire.read() ;

  gy_z = Wire.read() << 8 | Wire.read() ;

 

  deg = atan2(ac_x, ac_z) * 180 / PI ;  //rad to deg

 

  dgy_x = gy_y / 131. ;  //16-bit data to 250 deg/sec

  angle = (0.95 * (angle + (dgy_x * 0.001))) + (0.05 * deg) ; //complementary filter


      analogWrite(3, 250); //진동세기 임의의 값
      delay(50);
      analogWrite(3, 0);
      Serial.println(angle);
     Serial.println("Right_Warning");
     if(average - angle > -30) {
      break;  
     }
   }
  }
}
else {
  Serial.println(angle);
  Serial.println("OK");
}
