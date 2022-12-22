# MicroPython SSD1306 OLED driver, I2C and SPI interfaces

from micropython import const
import framebuf
import time
        
_SET_CONTRAST        = const(0x81)
_SET_NORM_INV        = const(0xa6)
_SET_DISP            = const(0xae)
_SET_SCAN_DIR        = const(0xc0)
_SET_SEG_REMAP       = const(0xa0)
_LOW_COLUMN_ADDRESS  = const(0x00)
_HIGH_COLUMN_ADDRESS = const(0x10)
_SET_PAGE_ADDRESS    = const(0xB0)

# http://docs.micropython.org/en/latest/pyboard/library/framebuf.html
class SH1108(framebuf.FrameBuffer):
    def __init__(self, width, height, rot = 0):
        self.rot = rot
        self.width = width
        self.height = height
        self.buffer = bytearray(self.height * self.width//8)
        if rot==0 or rot==2:
            super().__init__(self.buffer, self.width, self.height, framebuf.MONO_HMSB, self.width)
        else:
            super().__init__(self.buffer, self.width, self.height, framebuf.MONO_VLSB, self.width)

        self.init_display()

    def init_display(self):

        for cmd in (
            0xae,  #关显示
            0xB0,0x00,  #设置内存地址模式！！
            0x10,0x00,  #Set Higher Column Address of display RAM
            
            0x81,0xff,  #设置对比度
            0xa1,       #段重映射  ！！
            0xa4,       #正常显示，a5为全白显示
            0xa6,       #正常显示，a7为反白显示
            0xa8,0x3f,  #复用率设置
            #0xa9,0x00,  #设置分辨率64*160
            0xad,0x80,  #禁用DCDC
            0xc0,  #c8和c0交换com0--63
            0xd5,0x50,  #设置时钟分频
            0xd9,0x22,  #设置预充电周期
            0xdb,0x30,  #设置comh解除电平
            0xdc,0x30,  #设置segh解除电平
            0x30,0x33  #设置VSL解除电平
        ):
            self.write_cmd(cmd)
        if self.rot==1:
            self.write_cmd(0xc8)
        elif self.rot==2:
            self.write_cmd(0xa0)
            self.write_cmd(0xc8)
        elif self.rot==3:
            self.write_cmd(0xa0)
        else:
            pass
        self.fill(0)
        self.show()
        self.write_cmd(0xaf)


    def poweroff(self):
        self.write_cmd(SET_DISP | 0x00)

    def poweron(self):
        self.write_cmd(SET_DISP | 0x01)

    def contrast(self, contrast):
        self.write_cmd(SET_CONTRAST)
        self.write_cmd(contrast)

    def invert(self, invert):
        self.write_cmd(SET_NORM_INV | (invert & 1))

    def show(self):
        if self.rot==1 or self.rot==3:
            for page in range(self.height//8):
                self.write_cmd(_SET_PAGE_ADDRESS )
                self.write_cmd(page+2)
                self.write_cmd(_LOW_COLUMN_ADDRESS)
                self.write_cmd(_HIGH_COLUMN_ADDRESS+3)
                self.write_data(self.buffer[self.width * page:self.width *( page +1)])
        elif self.rot==0 or self.rot==2:
            for page in range(self.height):
                self.write_cmd(_SET_PAGE_ADDRESS)
                self.write_cmd(2)
                self.write_cmd(_LOW_COLUMN_ADDRESS+(page&0x0f))
                self.write_cmd(_HIGH_COLUMN_ADDRESS+3+(page>>4))
                self.write_data(self.buffer[self.width//8 * page:self.width//8 *( page +1)])


class SH1122_SPI(SH1108):
    def __init__(self, width, height, spi, dc, res, cs, rot=0):
        dc.init(dc.OUT, value=0)
        res.init(res.OUT, value=0)
        cs.init(cs.OUT, value=1)
        self.spi = spi
        self.dc = dc
        self.res = res
        self.cs = cs
        import time

        self.res(0)
        time.sleep_ms(1000)
        self.res(1)
        time.sleep_ms(100)
        super().__init__(width, height,rot)

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