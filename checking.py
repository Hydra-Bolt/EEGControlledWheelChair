import serial

ser = serial.Serial("COM4", 9600, timeout=1) # Change your port name COM... and your baudrate

def retrieveData(inp: str):
    ser.write(inp.encode('ascii'))
    data = ser.readline().decode('ascii').strip()
    return data

while True:
    uInput = input("Retrieve data? ")
    print(retrieveData(uInput))
