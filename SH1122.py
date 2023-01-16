# MicroPython ST7567 LCD driver, SPI interfaces

from micropython import const
import framebuf
import time

INIT_CMD_LIST=[
0xAE,#DISPOFF
0xB0,0x00,#SET_PAGE_ADDR
0x10,#Set Higher Column Address
0x00,#Set Lower Column Address
0xD5,0x50,#Set Display Clock Divide Ratio/Oscillator Frequency
0xD9,0x22,#Set Discharge/Precharge Period
0x40,#Set Display Start Line
0x81,0xFF,#Set Contrast Control Register
0xA1,#Set Segment Re-map A0
0xC8,#Set Common Output Scan Direction C0
0xD3,0x20,#Set Display Offset
0xA4,#Set Entire Display A5
0xA6,#Set Normal/Reverse Display A7
0xA8,0x3F,#Set Multiplex Ration
0xAD,0x80,#DC-DC Setting bit0:on/off bit1-3:freq 
0xDB,0x30,#Set VCOM Deselect Level
0xDC,0x33,#Set VSEGM Level
0xAF #DISPON
]
# Subclassing FrameBuffer provides support for graphics primitives
# http://docs.micropython.org/en/latest/pyboard/library/framebuf.html
class SH1122(framebuf.FrameBuffer):
    
    def __init__(self, width, height, spi, dc, res, cs):
        
        self.width = width
        self.height = height
        self.buffer = bytearray(self.height//2 * self.width)
        super().__init__(self.buffer, self.width, self.height, framebuf.GS4_HMSB, self.width)

        dc.init(dc.OUT, value=0)
        res.init(res.OUT, value=0)
        cs.init(cs.OUT, value=1)
        self.spi = spi
        self.dc = dc
        self.res = res
        self.cs = cs

        self.init_display()

    def init_display(self):

        self.res(1)
        time.sleep_ms(10)
        self.res(0)
        time.sleep_ms(100)
        self.res(1)
        time.sleep_ms(10)
        for cmd in INIT_CMD_LIST:
            self.write_cmd(cmd)
        self.fill(0)
        self.show()
        self.poweron()
        
    def write_cmd(self, cmd):
        self.cs(1)
        self.dc(0)
        self.cs(0)
        self.spi.write(bytearray([cmd]))
        self.cs(1)

    def write_data(self, buf):
        self.cs(1)
        self.dc(1)
        self.cs(0)
        self.spi.write(buf)
        self.cs(1)

    def poweroff(self):
        self.write_cmd(0XAE)

    def poweron(self):
        self.write_cmd(0XAF)

    def contrast(self, contrast):
        self.write_cmd(0X81)
        self.write_cmd((contrast&0xff))

    def invert(self, invert):
        self.write_cmd(0XA6 | (invert >0))


    def show(self):
        self.write_cmd(0xB0)
        self.write_cmd(0)
        self.write_cmd(0x10)
        self.write_cmd(0x00)
        self.write_data(self.buffer)

