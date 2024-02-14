// Fixed Sampling EEG Filter - BioAmp EXG Pill

#define SAMPLE_RATE 125
#define BAUD_RATE 115200
#define INPUT_PIN A0

void setup() {
  // Serial connection begin
  Serial.begin(BAUD_RATE);
}

void loop() {
  // Calculate elapsed time
  static unsigned long past = 0;
  unsigned long present = micros();
  unsigned long interval = present - past;
  past = present;

  // Run timer
  static long timer = 0;
  timer -= interval;

  // Sample
  if (timer < 0) {
    timer += 1000000 / SAMPLE_RATE;
    int sensor_value = analogRead(INPUT_PIN);
    float signal = EEGFilter(sensor_value);
    Serial.println(signal);
  }
}

// Band-Pass Butterworth IIR digital filter, generated using filter_gen.py.
// Sampling rate: 125.0 Hz, frequency: [0.5, 29.5] Hz.
// Filter is order 4, implemented as second-order sections (biquads).
// Reference:
// https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.butter.html
// https://courses.ideate.cmu.edu/16-223/f2020/Arduino/FilterDemos/filter_gen.py
float EEGFilter(float input) {
  float output = input;
  {
    static float z1, z2; // filter section state
    float x = output - -0.76828189 * z1 - 0.29112154 * z2;
    output = 0.00391759 * x + 0.00783519 * z1 + 0.00391759 * z2;
    z2 = z1;
    z1 = x;
  }
  {
    static float z1, z2; // filter section state
    float x = output - -0.99386185 * z1 - 0.67373813 * z2;
    output = 1.00000000 * x + 1.99744439 * z1 + 1.00000000 * z2;
    z2 = z1;
    z1 = x;
  }
  {
    static float z1, z2; // filter section state
    float x = output - -1.95557810 * z1 - 0.95654368 * z2;
    output = 1.00000000 * x + -1.99963446 * z1 + 1.00000000 * z2;
    z2 = z1;
    z1 = x;
  }
  {
    static float z1, z2; // filter section state
    float x = output - -1.97805789 * z1 - 0.97817022 * z2;
    output = 1.00000000 * x + -1.99999796 * z1 + 1.00000000 * z2;
    z2 = z1;
    z1 = x;
  }
  return output;
}
