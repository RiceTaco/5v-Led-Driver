from machine import Pin, Timer
import time
import neopixel

class pwm_read:
    def __init__(self, pin):
        self.pin = pin
        self.pin.init(Pin.IN)
        self.last_time = 0
        self.pulse_width = 0
        self.frequency = 0
    
    "need to understand got from chatgpt"
    def pwm_callback(self, pin):
        """Interrupt handler to measure PWM pulse width and frequency."""
        current_time = time.ticks_us()  # Get current time in microseconds
        
        # Measure pulse width
        self.pulse_width = time.ticks_diff(current_time, self.last_time)
        self.last_time = current_time  # Update last timestamp

        # Compute frequency
        if self.pulse_width > 0:
            self.frequency = 1000000 // self.pulse_width  # Convert period to Hz

    def get_pwm(self):
        return self.frequency

"need to write a function to get the pwm frequency and then use it to control the led"
class led_strip:
    def __init__(self, pin):
        self.pin = (pin, Pin.OUT)
        self.led = neopixel.NeoPixel(self.pin, 1)
        self.brightness = 1.0
        self.last_color = (0, 0, 0)
        self.led.fill(self.last_color)
        self.led.write()

    # useful for blinking
    def on(self):
        self.led.fill(self.last_color)
        self.led.write()
    def off(self):
        self.led.fill((0, 0, 0))
        self.led.write()


    def set_color(self, r, g, b):
        """Set LED color with brightness scaling and store it."""
        self.last_color = (
            int(r * self.brightness), 
            int(g * self.brightness), 
            int(b * self.brightness)
        )
        self.led.fill(self.last_color) #storing the color for the on function
        self.led.write()

    "might not be needed" 
    def set_brightness(self, brightness): 
        self.brightness = max(0.0, min(1.0, brightness))  # Keep within range

    "only pattern for now"    
    def blink(self):
        self.on()
        time.sleep(0.5)
        self.off()

def main():
    # Setup PWM reader on pin 26
    pwm_reader = pwm_read(Pin(26))
    pwm_reader.pin.irq(trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING, handler=pwm_reader.pwm_callback)

    # Setup LED_strip on pin 2
    led = led_strip(1)

    "loop to read pwm"
    while True:
        # Read PWM frequency
        frequency = pwm_reader.get_pwm()
        print("Frequency: {} Hz".format(frequency))
       