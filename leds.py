import os
import spidev
import anvil.server
from time import sleep

NUM_LEDS = 30
MAX_BRIGHTNESS = 31 # 1 - 31 inclusive

if "UPLINK_KEY" in os.environ:
    anvil.server.connect(os.environ["UPLINK_KEY"])

spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz = 32000000

# Buffer is 4 bytes per LED, data must start with 111,
# then five bits of brightness (0-32), then 24 bits of blue, green, red.
# Default: Brightness 0 (off), and a nice flame colour.
buffer = [0xe0, 2, 100, 255] * NUM_LEDS

# Unused for now
def set_led(idx, brightness, red, green, blue):
    buffer[idx*4] = 0xe0 + brightness
    buffer[idx*4+1] = blue
    buffer[idx*4+2] = green
    buffer[idx*4+3] = red

def update_leds():
    spi.writebytes2([0,0,0,0] + buffer)

@anvil.server.callable
def led_on(idx):
    buffer[idx*4] = 0xe0 + MAX_BRIGHTNESS
    update_leds()

@anvil.server.callable
def led_off(idx):
    buffer[idx*4] = 0xe0
    update_leds()

if "UPLINK_KEY" in os.environ:
  anvil.server.wait_forever()

# We only get here if there's no uplink connection
j = 0
while True:
    led_off((j%NUM_LEDS)-3)
    led_on(j% NUM_LEDS)
    update_leds()
    j+=1
    sleep(0.05)

