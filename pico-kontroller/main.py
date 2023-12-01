from machine import ADC, Pin
from time import sleep

led = Pin(25, Pin.OUT)
x_joystick = ADC(Pin(28, Pin.IN))
y_joystick = ADC(Pin(27, Pin.IN))
knappJ = Pin(26, Pin.IN, Pin.PULL_UP)
knappA = Pin(18, Pin.IN, Pin.PULL_UP)
knappB = Pin(13, Pin.IN, Pin.PULL_UP)

FPS = 60
DIVISOR = 2**15

dt = 1 / FPS

while True:
    sleep(dt)
        
    x = x_joystick.read_u16() / DIVISOR - 1
    y = y_joystick.read_u16() / DIVISOR - 1
    
    kJ = int(knappJ.value() == 0)
    kA = int(knappA.value() == 0)
    kB = int(knappB.value() == 0)
    if kJ:
        led.on()
    else:
        led.off()
        
    print(x, y, kJ, kA, kB)
