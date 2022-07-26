from TM1637 import *
from machine import Pin
import time

LED = TM1637(clk=Pin(15),dio=Pin(0))


LED.brightness(0)
LED.show("1352", True)
time.sleep(2)
LED.brightness(7)
LED.show("1353", True)
