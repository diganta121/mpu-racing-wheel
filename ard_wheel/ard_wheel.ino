#include <MPU9250_WE.h>
#include <Wire.h>
#define MPU9250_ADDR 0x68
MPU9250_WE myMPU9250 = MPU9250_WE(MPU9250_ADDR);

void setup() {
  Serial.begin(115200);
  Wire.begin();
  pinMode(19,INPUT);
  pinMode(26,INPUT);

  if(!myMPU9250.init()){
    Serial.println("MPU9250 does not respond");
  }
  else{
    Serial.println("MPU9250 is connected");
  }
 
  /* The slope of the curve of acceleration vs measured values fits quite well to the theoretical 
   * values, e.g. 16384 units/g in the +/- 2g range. But the starting point, if you position the 
   * MPU9250 flat, is not necessarily 0g/0g/1g for x/y/z. The autoOffset function measures offset 
   * values. It assumes your MPU9250 is positioned flat with its x,y-plane. The more you deviate 
   * from this, the less accurate will be your results.
   * The function also measures the offset of the gyroscope data. The gyroscope offset does not   
   * depend on the positioning.
   * This function needs to be called at the beginning since it can overwrite your settings!
   */
  Serial.println("Position you MPU9250 flat and don't move it - calibrating...");
  delay(1000);
  myMPU9250.autoOffsets();
  Serial.println("Done!");
  /*  This is a more accurate method for calibration. You have to determine the minimum and maximum 
   *  raw acceleration values of the axes determined in the range +/- 2 g. 
   *  You call the function as follows: setAccOffsets(xMin,xMax,yMin,yMax,zMin,zMax);
   *  Use either autoOffset or setAccOffsets, not both.
   */
  //myMPU9250.setAccOffsets(-14240.0, 18220.0, -17280.0, 15590.0, -20930.0, 12080.0);
  
  /*  Sample rate divider divides the output rate of the gyroscope and accelerometer.
   *  Sample rate = Internal sample rate / (1 + divider) 
   *  It can only be applied if the corresponding DLPF is enabled and 0<DLPF<7!
   *  Divider is a number 0...255
   */
  myMPU9250.enableFifo(false);

  myMPU9250.setSampleRateDivider(5);

  /*  MPU9250_ACC_RANGE_2G      2 g    (default)
   *  MPU9250_ACC_RANGE_4G      4 g
   *  MPU9250_ACC_RANGE_8G      8 g   
   *  MPU9250_ACC_RANGE_16G    16 g
   */
  myMPU9250.setAccRange(MPU9250_ACC_RANGE_2G);

  /*  Enable/disable the digital low pass filter for the accelerometer 
   *  If disabled the bandwidth is 1.13 kHz, delay is 0.75 ms, output rate is 4 kHz
   */
  myMPU9250.enableAccDLPF(true);

  /*  Digital low pass filter (DLPF) for the accelerometer, if enabled 
   *  MPU9250_DPLF_0, MPU9250_DPLF_2, ...... MPU9250_DPLF_7 
   *   DLPF     Bandwidth [Hz]      Delay [ms]    Output rate [kHz]
   *     0           460               1.94           1
   *     1           184               5.80           1
   *     2            92               7.80           1
   *     3            41              11.80           1
   *     4            20              19.80           1
   *     5            10              35.70           1
   *     6             5              66.96           1
   *     7           460               1.94           1
   */
  myMPU9250.setAccDLPF(MPU9250_DLPF_6);  
}

float curr;
float prev = 0;
unsigned long tim = millis();
int accelB = false;
int brakeB = false;
int ti = 3;
const int max_ti = 3;
int buttons = 0;

void loop() {
  // TODO accelerate , break button 

  xyzFloat angles = myMPU9250.getAngles();
  /* This method provides quite precise values for x/y 
   angles up 60°. */
  curr = angles.y;
  float diff = curr-prev;
  /* Pitch and roll consider all axes for calculation. According to my experience
  it provides more reliable results at higher angles (>60°) */
  float roll = myMPU9250.getRoll();

  if (ti == max_ti){
    accelB = digitalRead(19);
    brakeB = digitalRead(26);
    if (accelB && brakeB){
      buttons = 3;
    }
    else if (accelB){
      buttons = 1;
    }
    else if (brakeB){
      buttons = 2;
    }
    else{
      buttons = 0;
    }
    ti--;
  }
  else if(ti == 0){
    ti = max_ti;
  }
  else{
    ti--;
  }
  Serial.print(curr);
  Serial.print(" ");
  Serial.print(roll);
  Serial.print(" ");
  Serial.print(diff);
  Serial.print(" ");
  Serial.println(buttons);
  // tim = millis();
  // Serial.println(tim);
  prev = curr;
  delay(80);
}
