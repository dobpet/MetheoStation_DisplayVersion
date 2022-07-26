from machine import Pin,I2C
from BMx280 import BME280
import sys

NBL=Pin(12,Pin.OUT,value=0)

IIC=I2C(Pin(5),Pin(4),freq=400000)
print(IIC.scan())



BME=BME280(i2c=IIC)
print(BME.values)
