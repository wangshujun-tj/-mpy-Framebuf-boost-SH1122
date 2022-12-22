import time
from machine import Pin, SPI
spi = SPI(1, 20000000, sck=Pin(18), mosi=Pin(23), miso=Pin(19))
from SH1122 import SH1122_SPI
oled = SH1122_SPI(256, 64, spi,dc=Pin(21),cs=Pin(22),res=Pin(5),rot=0)
oled.font_load("GB2312-24.fon")

for i in range(4):
    oled.fill(0)
    oled.font_set(0x23,i,1,0)
    oled.text("中文显示GB2312",0,16,1)
    oled.show()
    time.sleep(0.5)
    oled.fill(0)
    oled.font_set(0x23,i,1,1)
    oled.text("中文显示GB2312",0,16,1)
    oled.show()
    time.sleep(2.5)

for i in range(15):
    oled.fill(i)
    oled.show()
    time.sleep(0.3)
oled.fill(0)    
for i in range(15):    
    oled.fill_rect(i*16, 0, 16, 64, i)
oled.show()
time.sleep(3)

oled.fill(0)
oled.show()
time.sleep(0.2)