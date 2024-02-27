
import pylibi2c

def set_bits(address, mask, bits):
    """Set bits in a register."""
    buf = i2c.read(address, 1)
    buf = (buf & ~mask) | (bits & mask)
    i2c.write(address, bytes([buf]))


address = 0x39
i2c = pylibi2c.I2CDevice("/dev/i2c-1", address)
i2c.delay = 10
i2c.page_bytes = 8
i2c.flags = pylibi2c.I2C_M_IGNORE_NAK

buf = bytes(256)

# Step 1: reset and initialize
buf = bytes([0x00])
i2c.write(0xC7, buf)

# Step 2: detect revision
rv = i2c.read(0x1B, 4)
print(f"Version: {rv[0]}")

# Step 3: power up
buf = bytes([])
avi_pwr = i2c.read(0x1E, 1)
print(f"AVI POWER STATE: {avi_pwr}")
avi_pwr = 0
i2c.write(0x1E, bytes([avi_pwr]))

# Step 4: enable output
output_mode = 1  # 1:HDMI 0:DVI
set_bits(0x1A, 0x01, output_mode)

# Step 5: TPI configuration
pixelClock = 2400  # 24MHz / 10000

vFreq = 43  # in Hz

pixelsPerLine = 1056  # 800 pixels width + 256 blanking

Lines = 635  # 480 lines + 155 blanking

pixelRepetitionFactor = 0  # Bit 0 .. 3
edgeSelect = 1 << 4  # Bit 4
inputBusSelect = 1 << 5  # Bit 5
TClkSel = 1 << 7  # Bit 6 and 7 (value 0..3)
buf = bytes(
    [
        pixelClock & 0xFF,
        (pixelClock >> 8) & 0xFF,
        vFreq & 0xFF,
        (vFreq >> 8) & 0xFF,
        pixelsPerLine & 0xFF,
        (pixelsPerLine >> 8) & 0xFF,
        Lines & 0xFF,
        (Lines >> 8) & 0xFF,
        (pixelRepetitionFactor | edgeSelect | inputBusSelect | TClkSel),
        0x00,  # Range Auto, Colorspace RGB
    ]
)
i2c.write(0x00, buf)

PIXEL_LEN = 42ns 

VSYNC_LEN = 442us
VSYNC_P = 43,33Hz 23,03ms
VSYNC = 1 #low active

HSYNC_LEN = 412ns
HSYNC_P = 22,73kHz 44000ns % 42ns
HSYNC = 1 #low active
DE_DLY = 1023 # ~43800ns % 42ns
DE_TOP = 1 # measured 2000000ns % 42ns 
DE_CNT = 800
DE_LIN = 480
DE_LOW = 10,8us



buf = bytes(
    [
        DE_DLY & 0xff,
        (DE_DLY >> 8) & 0x3 + 0x70,
        DE_TOP & 0x7f,
        0x00,
        DE_CNT & 0xff,
        (DE_CNT >> 8) & 0x0f,
        DE_LIN & 0xff,
        (DE_LIN >> 8) & 0x0f,
    ]
)
i2c.write(0x62, buf)

