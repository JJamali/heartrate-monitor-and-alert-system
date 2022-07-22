//This is initializing an analog pin
const int sensorPin = A0;
//This will read a value coming in from the AC gain stage
int sensorVal = 0; 
//counter temporary variable
unsigned long pulseCounter = 0;
//the first detectable pulse
unsigned long pulseStarting = 0;
//the second one for reference
unsigned long pulseStartingSecond = 0;
//The time between the two pulses
unsigned long time_between_pulses = 0;
//How much the refactory period represents
const unsigned long refractoryPeriod = 300;
//Needed for calculating heart rate
const double minutes_in_milliseconds = 60000;
int static_variable = 500;


//This threshold is theoretical and can be changed depending on the purse
const double threshold = 0.44;


void setup()
{

  Serial.begin(115200); //  Baud rate determined
  delay(2000); //a slight delay for system stabilization
}


void loop()
{
  //creates a timer variable to keep track of time
  unsigned long timer = millis();
  
  sensorVal = analogRead(sensorPin); //Reading the sensor pin
  
  double voltage = voltageConversion(sensorVal); //calling the voltage converting
  
  double absorbance = calculateAbsorbance(voltage); // signal processing for absorption
  
  long time_between_pulses = thresholdDetector(absorbance); //signal processing to detect when the refractory period should be
  
  int pulseRate = calculatePulseRate(time_between_pulses); // signal processing to take the refactory period and get a heart rate
    
  displayPulseInLabVIEW(absorbance, pulseRate);
  
  //small delay to change our sampling rate
  //and stabilize our signal
  delay(25);  
}


//displayPulseInLabVIEW()
//Outputs the data via serial communication. LabVIEW reads the
//data coming in and plots the pulse waveform as well as the
//pulse rate
void displayPulseInLabVIEW(double absorbance, int pulseRate)
{
  //Serial.print allows us to output the data
  //via serial communication
  Serial.print(absorbance,5);
  Serial.print("\t");
  Serial.print(pulseRate);
  Serial.println();
  delay(1000);
}


//voltageConversion()
double voltageConversion(double ADC_Val)
{
  double volt = 0;
  
//  Converts the sensor reading to voltage here
  volt = 5*(ADC_Val/1023);
  
  return volt;
}


//calculateAbsorbance()
double calculateAbsorbance(double volt)
{
  double absorbance = 0;
  
//  calculating absorbance of the finger based off the voltage conversion 
    
  absorbance = log10(5/volt);
  
  return absorbance;  
}


//calculatePulseRate()
//This method calculates pulse rate by dividing 60 seconds by the time between subsequent pulses
double calculatePulseRate(long time_between_pulses)
{
  return minutes_in_milliseconds/time_between_pulses;
}


//thresholdDetector()
//This method detects whether the signal has passed our threshold and determines the time between subsequent peaks
long thresholdDetector(double absorbance)
{
  if (millis() - pulseStarting >= refractoryPeriod
    && absorbance >= threshold)
  {
    if (pulseCounter == 0)
    {
      pulseCounter++;
      pulseStarting = millis();
    }
    else if (pulseCounter == 1)
    {
      pulseStartingSecond = millis();
      time_between_pulses = pulseStartingSecond - pulseStarting;
      pulseStarting = pulseStartingSecond;
    }
  }

  return time_between_pulses;
}
