import time
from machine import Pin, SPI
spi = SPI(2,20000000, sck=Pin(32), mosi=Pin(33), miso=Pin(35))
from SH1122 import SH1122
oled = SH1122(256, 64, spi,dc=Pin(26),cs=Pin(27),res=Pin(25))
oled.contrast(40)
oled.font_load("GB2312-24.fon")

for count in range(10):
    oled.fill(0)
    oled.font_set(0x11,0,1,0)
    oled.text("micro中文迤=%d"%count,0,0,1)
    oled.font_set(0x31,0,1,0)
    oled.text("micro中文迤=%d"%count,0,13,1)
    oled.text("micro中文迤=%d"%count,0,26,1)
    oled.font_set(0x41,0,1,0)
    oled.text("micro中文迤=%d"%count,0,39,1)
    oled.text("micro中文迤=%d"%count,0,51,1)
    oled.show()

for count in range(10):
    oled.fill(0)
    oled.font_set(0x12,0,1,0)
    oled.text("MicRo中文=%d"%count,0,0,1)
    oled.font_set(0x22,0,1,0)
    oled.text("MicRo中文=%d"%count,0,16,1)
    oled.font_set(0x32,0,1,0)
    oled.text("MicRo中文=%d"%count,0,32,1)
    oled.font_set(0x42,0,1,0)
    oled.text("micro中文=%d"%count,0,48,1)
    oled.show()

for count in range(10):
    oled.fill(0)
    oled.font_set(0x13,0,1,0)
    oled.text("MRo中文=%d"%count,0,0,1)
    oled.font_set(0x33,0,1,0)
    oled.text("MRo中文=%d"%count,0,32,1)
    oled.show()

for count in range(10):
    oled.fill(0)
    oled.font_set(0x14,0,1,0)
    oled.text("MR文=%d"%count,0,0,1)
    oled.font_set(0x34,0,1,0)
    oled.text("Mo中=%d"%count,0,32,1)
    oled.show()

f=open("img16new.bin","rb")
temp=bytearray(f.read(8192))
oled.buffer[:]=temp[:]
f.close()
oled.show()


