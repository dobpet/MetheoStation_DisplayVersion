from machine import RTC, Pin, I2C, ADC, SPI
from TM1637 import *
import PCD8544
import network
import ntptime
import utime
import time
import dht
from BMx280 import BME280

def dstTime():
    year = time.localtime()[0] #get current year
    # print(year)
    HHMarch = time.mktime((year,3 ,(14-(int(5*year/4+1))%7),1,0,0,0,0,0)) #Time of March change to CEST
    HHNovember = time.mktime((year,10,(7-(int(5*year/4+1))%7),1,0,0,0,0,0)) #Time of November change to CET
    #print(HHNovember)
    now=time.time()
    if now < HHMarch : # we are before last sunday of march
        dst=time.localtime(now+3600) # CET: UTC+1H
    elif now < HHNovember : # we are before last sunday of october
        dst=time.localtime(now+7200) # CEST: UTC+2H
    else: # we are after last sunday of october
        dst=time.localtime(now+3600) # CET: UTC+1H
    return(dst)

FR = ADC(0)

DC_CLK=Pin(15)
RST_DIO=Pin(0)

LED = TM1637(clk=DC_CLK,dio=RST_DIO)
LED.brightness(0)
LED.show('----', False)
CE = Pin(2, Pin.OUT, value = 0)

DSEN = dht.DHT11(Pin(16))
DSEN.measure()
print(DSEN.temperature())
print(DSEN.humidity())

CE.on()
spi = SPI(1)
spi.init(baudrate=100000, polarity=0, phase=0)
lcd = PCD8544.PCD8544_FRAMEBUF(spi, CE, DC_CLK, RST_DIO)

# fill(color)
lcd.fill(1)
lcd.show()
lcd.fill(0)
lcd.text('Nokia 5110', 0, 0, 1)
lcd.text('PCD8544', 0, 10, 1)
lcd.text('84x48', 0, 20, 1)
lcd.text('uPython1.9', 0, 30, 1)
lcd.text('ESP8266', 0, 40, 1)
lcd.show()
time.sleep(2)
lcd.data(bytearray(b'\x80\x00\x00\x80\x00\x00\x80\x00\x00\x80\x00\x00\x80\x00\x00\x80\x00\x00\x80\x80\x40\x40\x40\x80\x80\xC0\xC0\x40\xC0\xA0\xE0\xC0\xE0\xE0\xF0\xF0\xF8\xF8\xF8\xFC\xFC\xFE\xEE\xF4\xF0\xF0\x70\x30\x00\x80\x00\x00\x80\x00\x0C\x9C\x1C\x38\xB8\x38\x38\xB8\xF8\xF0\xF0\xF0\xF0\xF0\xF0\xF0\xF0\xF0\xF0\xF0\xF0\xF0\xF0\xF0\xF0\xF0\xF8\xF8\xF8\xF8\x88\x20\x8A\x20\x08\x22\x08\x00\x0A\x00\x00\x02\x80\x71\xBA\xDA\xFD\xDD\xED\xDE\xEE\xF7\xFF\xFB\xFD\xFD\xFE\xFF\x7F\x3F\x1F\x9F\x3F\x7F\x6F\x0F\xAF\x1F\xBF\x3E\x3C\x7A\x78\x70\x22\x88\xA0\x2A\x80\x08\x62\xE0\xE0\xF2\xF0\x58\xDA\xF8\xFC\x92\xFE\xFF\xFF\xD3\xFF\xFD\xF3\xE1\xF0\xF9\x7F\xBF\x3F\x8F\x2F\x4F\xAF\x0F\x4F\xA7\x0F\xAF\x87\x2F\x82\x80\x20\xC0\x80\x80\x50\x40\xC4\xD0\xA0\xE8\xE4\xEA\xFF\xFB\xFD\xFF\xFF\xFF\xFF\xFF\xEF\x4F\x27\x53\xA8\x54\x29\x4A\xB5\x82\xAC\xA1\x8A\xB6\x50\x4D\x32\xA4\x4A\xB4\xA9\x4A\x52\xB4\xAA\x45\xA8\xDA\x22\xAC\xD2\x2A\x52\xA8\x52\x4C\xB0\xAD\x43\x5B\xB3\x45\xA8\x5B\xA3\xAB\x55\xA8\x52\x54\xA9\x56\xA8\x45\xBA\xA4\x49\x5A\xA2\x54\xAA\x52\xFE\xFF\xFF\xFE\xFD\xFF\xFF\xFF\xFE\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\x7F\xFF\xFE\xBF\x7F\xBF\xBF\xFF\xDF\xBF\x5F\xDF\x7F\xDF\x7F\xDF\xAF\x7F\xEE\x8E\xF1\x6E\x99\xF7\x6A\xDD\xB2\x6E\xD5\x7A\xD7\xAC\x75\xDB\x6D\xD5\x7A\xD7\xAC\x7B\xE5\xDE\xA9\x77\xDA\xB5\xEE\x59\xB6\xEB\xDD\xB6\x69\xD6\xBF\xE8\x55\xEF\xB9\xD6\xED\xB5\x5B\xAB\xFF\xFD\xF7\xFF\x01\x01\x01\x01\xE1\xC1\x81\x03\x05\x0F\x1D\x2F\x7E\x01\x00\x01\x01\xFF\xFE\x03\x01\x01\x00\xF1\xF0\xF1\x71\xF1\xF1\xB1\xF1\x01\x01\x01\x03\xFE\xFF\x01\x01\x01\x01\xBE\x1B\x0D\x07\x03\x41\xE1\xF1\xF9\x6D\xFF\xFF\x00\x01\x01\x01\xFF\xFF\xEB\x3E\x0D\x03\x01\x41\x71\x70\x41\x01\x03\x0E\x3B\xEF\xFE\xFB\xEE\x7D\xF7\xFF\xFF\xFF\xFF\xFE\xFF\xF0\xF0\xF0\xF0\xFF\xFF\xFF\xFF\xFE\xFC\xF8\xF0\xF0\xF0\xF0\xF0\xF0\xFF\xFF\xF8\xF0\xF0\xF0\xF1\xF1\xF1\xF1\xF1\xF1\xF1\xF1\xF0\xF0\xF0\xF8\xFF\xFF\xF0\xF0\xF0\xF0\xFF\xFF\xFE\xFC\xF8\xF0\xF0\xF1\xF3\xF7\xFF\xFF\xF0\xF0\xF0\xF0\xFF\xF3\xF0\xF0\xF0\xFC\xFC\xFC\xFC\xFC\xFC\xFC\xFC\xF0\xF0\xF0\xF3\xFF\xFF\xFF\xFF\xFF'))



IIC=I2C(Pin(5),Pin(4),freq=400000)
BME=BME280(i2c=IIC)
print(BME.values)

sta_if = network.WLAN(network.STA_IF)
if not sta_if.isconnected():
    print('connecting to network...')
    sta_if.active(True)
    sta_if.connect('BTECH-openspace-public', 'btech1234')
    while not sta_if.isconnected():
        pass
    print('network config:', sta_if.ifconfig())
else:
    print('network config:', sta_if.ifconfig())
    

rtc = RTC()
print(rtc.datetime())
ntptime.settime()
print(rtc.datetime())
CET = dstTime()
print(CET)
rtc.datetime( (CET[0], CET[1], CET[2], CET[6], CET[3], CET[4], CET[5], CET[7]) )
print(rtc.datetime())
FSH = None
lcd.fill(0)
lcd.vline(42,0,48,1)
lcd.show()
while True:
    tmv = rtc.datetime()
    if FSH==None:
        tstr = '{0: >2}{1:0>2}'.format(tmv[4], tmv[5])
        CE.on()
        if tmv[7]>500:
            LED.show(tstr, True)
            FSH=False
            nFSH=False
        else:
            LED.show(tstr, True)
            FSH=False
            nFSH=True
        CE.off()
    else:
        if not FSH and tmv[7]>500:
            nFSH=True
        if FSH and tmv[7]<500:
            nFSH=False
        if FSH!=nFSH:
            tstr = '{0: >2}{1:0>2}'.format(tmv[4], tmv[5])
            CE.on()
            LED.show(tstr, nFSH)
            CE.off()
            #print(FR.read())
            FSH=nFSH
            DSEN.measure()
            lcd.text('{0: >5.1f} C'.format(DSEN.temperature()),0,0,1)
            lcd.show()

            
        
    utime.sleep_ms(100)