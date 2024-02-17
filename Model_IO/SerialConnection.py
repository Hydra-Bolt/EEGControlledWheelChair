from serial import Serial
from time import sleep
from datetime import datetime
from joblib import load
import numpy as np
from processDataset import generate_model_input
from cleaningEEG import clean_csv
from random import randint
import numpy as np

def find_most_common_value(array):
    unique_values, counts = np.unique(array, return_counts=True)
    most_common_index = np.argmax(counts)
    most_common_value = unique_values[most_common_index]
    return most_common_value


FILES_STATES = {0: 'backward', 2: 'right', 1: 'left', 3: 'forward'}
FORMAT = "[%Y-%m-%d %H:%M:%S.%f]"
TEMP = "./temp.csv"
model = load("./EEGCLASSIFIER.joblib")
ser = Serial("COM3", 115200)
sleep(2)
while True:
    # Get data from Arduino
    count = 0
    signal_buffer = []
    timestamp_buffer = []
    while count<1000:
        signal_ = ser.readline().decode().strip()
        timestamp_ = datetime.now().strftime(FORMAT)
        timestamp_buffer.append(timestamp_)
        signal_buffer.append(signal_)
        count+=1
    # Write 500 lines to file
    with open(TEMP, "w+") as f:
        for timestamp, signal in zip(timestamp_buffer, signal_buffer):
            if len(signal)>0:
                f.write(f"{timestamp} {signal}\n")
    processed_frame = clean_csv(TEMP)
    prediction_frame = generate_model_input(processed_frame)
    predictions = model.predict(prediction_frame)
    prediction = find_most_common_value(predictions)
    prediction = randint(0, 3)
    ser.write(str(prediction).encode("utf-8"))
    print("Writing ... ", FILES_STATES[prediction])
    sleep(2)