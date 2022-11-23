import serial
import time

arduino=serial.Serial('COM11',9600)
time.sleep(2)
dato_leido=arduino.readline()
print(dato_leido)
arduino.close()
