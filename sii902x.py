import ctypes
import pylibi2c

address = 0x39
i2c = pylibi2c.I2CDevice("/dev/i2c-1", address)
i2c.delay = 10
i2c.page_bytes = 8
i2c.flags = pylibi2c.I2C_M_IGNORE_NAK

buf = bytes(256)

# reset and initialize
buf = bytes([0x00])
i2c.write(0xC7, buf)

rv = i2c.read(0x1B, 4)
print(rv)

# enable
buf = bytes([])
avi_pwr = i2c.read(0x1E, 1)
print(f"AVI POWER STATE: {avi_pwr}")
avi_pwr = 0
i2c.write(0x1E, bytes([avi_pwr]))

sys_ctrl = i2c.read(0x1A, 1)
print(f"SYS_CTRL_PWR: {sys_ctrl}")
avi_pwr &= ~0x1
i2c.write(0x1E, bytes([avi_pwr]))

output_mode = 1
i2c.write(0x1A, bytes([output_mode]))

buf = bytes([0x60, 0x09, 0x0F, 0x00, 0x30, 0x75, 0x20, 0x03, 0x60, 0x05])
i2c.write(0x00, buf)