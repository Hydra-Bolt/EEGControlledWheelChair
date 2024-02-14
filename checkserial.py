import serial
import time
# Establish serial connection with Arduino
ser = serial.Serial(port='COM3', baudrate=9600)  # Adjust port and baudrate as needed
time.sleep(2)
try:
    while True:
        # Read data from Arduino
        arduino_data = ser.readline().decode().strip()
        
        # Process the data or perform actions based on Arduino input
        print("Arduino says:", arduino_data)
        sent = str(int(arduino_data)//9)
        print("sending data: ",sent)
        ser.write(sent.encode('utf-8'))  # Send ACK to indicate we received the message
        print("Arduino replied:", ser.readline().decode().strip())
except KeyboardInterrupt:
    ser.close()  # Close the serial port on Ctrl+C
