import serial
import joblib
from final import generate_model_input
from check import clean_csv
from time import sleep

ser = serial.Serial(port='COM3', baudrate=115200)
sleep(3)
model = joblib.load('model.pkl')
eeg_buffer = []
predict = False

try:
    while True:
        # Read EEG signal from Arduino
        eeg_signal = ser.readline().decode().strip()
        eeg_buffer.append(eeg_signal)

        # Accumulate EEG signals and predict in batches
        if len(eeg_buffer) >= 1000:  # Adjust batch size as needed
            with open("./temp.csv", "w+") as f:
                f.write('\n'.join(eeg_buffer))
            predict = True
            eeg_buffer = []  # Clear the buffer after writing to file

        # Make predictions
        if predict:
            result = generate_model_input(clean_csv("./temp.csv")).drop(columns=['Start Timestamp', "End Timestamp"])
            prediction  = model.predict([result.iloc[-1]])
            ser.write(prediction)
            predict = False

except KeyboardInterrupt:
    ser.close()  # Close the serial port on Ctrl+C
