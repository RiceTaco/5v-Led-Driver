from machine import Pin, Timer # type: ignore
import time
import neopixel # type: ignore

class pwm_read:
    def __init__(self, pin):
        self.pin = pin
        self.pin.init(Pin.IN)
        self.last_time = 0
        self.pulse_width = 0
        self.frequency = 0
    
    def pwm_callback(self):
        #Interrupt handler to measure PWM pulse width and frequency
        current_time = time.ticks_us()  # Get current time in microseconds
        
        # Measure pulse width
        self.pulse_width = time.ticks_diff(current_time, self.last_time)
        self.last_time = current_time  # Update last timestamp

        # Compute frequency
        if self.pulse_width > 0:
            self.frequency = 1000000 // self.pulse_width  # Convert period to Hz

    def get_pwm(self):
        return self.frequency

class led_strip:
    def __init__(self, pin):
        self.pin = Pin(pin, Pin.OUT)
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
        self.last_color = (
            int(r * self.brightness), 
            int(g * self.brightness), 
            int(b * self.brightness)
        )
        self.led.fill(self.last_color) #storing the color for the on function
        self.led.write()

    "useful for fading during patterns"
    def set_brightness(self, brightness): 
        self.brightness = max(0.0, min(1.0, brightness))  # Keep within range

    "patterns"   
    def blink(self, sleep_time=0.1):
        self.on()
        time.sleep(sleep_time)
        self.off()

    def snake(self, sleep_time=0.1):
        for i in range(self.led.n):
            self.led[i] = self.last_color
            self.led.write()
            time.sleep(sleep_time)
            self.led[i] = (0, 0, 0)
            self.led.write()
    
    def pulse(self, max_brightness=1.0, sleep_time=0.1, steps=100):
        for i in range(steps):
            brightness = max_brightness * (i / float(steps))
            self.set_brightness(brightness)
            self.set_color(last_color)
            time.sleep(sleep_time)
        for i in range(steps):
            brightness = max_brightness * (1 - i / float(steps))
            self.set_brightness(brightness)
            self.set_color(last_color)
            time.sleep(sleep_time)

    "reads pwm signal and sets color based on the frequency"
    def set_led_state(self, frequency):
        if frequency >= 1205:
            set.color(124, 46, 201)
            self.blink()
        elif frequency >= 1195:
            set.color(124, 46, 201)
            self.pulse()
        elif frequency >= 1185:
            set.color(35, 38, 194)
            self.blink()
        elif frequency >= 1175:
            set.color(35, 38, 194)
            self.pulse()
        elif frequency >= 1165:
            set.color(70, 166, 240)
            self.blink()
        elif frequency >= 1155:
            set.color(70, 166, 240)
            self.pulse()
        elif frequency >= 1145:
            set.color(21, 191, 78)
            self.blink()
        elif frequency >= 1135:
            set.color(21, 191, 78)
            self.pulse()
        elif frequency >= 1125:
            set.color(255, 244, 28)
            self.blink()
        elif frequency >= 1115:
            set.color(255, 244, 28)
            self.pulse()
        elif frequency >= 1105:
            set.color(255, 129, 33)
            self.blink()            
        elif frequency >= 1095:
            set.color(255, 129, 33)
            self.pulse()
        elif frequency >= 1085:
            set.color(255, 33, 33)
            self.blink()
        elif frequency >= 1075:
            set.color(255, 33, 33)
            self.pulse()
        elif frequency >= 1065:
            set.color(124, 46, 201)
        elif frequency >= 1055:
            set.color(35, 38, 194)
        elif frequency >= 1045:
            set.color(70, 166, 240)
        elif frequency >= 1035:
            set.color(21, 191, 78)
        elif frequency >= 1025:
            set.color(255, 244, 28)
        elif frequency >= 1015:
            set.color(255, 129, 33)
        elif frequency >= 1005:
            set.color(255, 33, 33)
        else:
            set.color(0, 0, 0)
            

def main():
    # Setup PWM reader on pin 26
    pwm_reader = pwm_read(Pin(26))
    # interrupt on both rising and falling edges
    pwm_reader.pin.irq(trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING, handler=pwm_reader.pwm_callback)

    # Setup LED_strip on pin 1
    led = led_strip(1)

    "loop to read pwm"
    while True:

        # Read PWM frequency
        frequency = pwm_reader.get_pwm()
        print("Frequency: {} Hz".format(frequency))

        led.set_led_state(frequency)

        time.sleep(0.1) # delay to avoid excessive updates
        
if __name__ == "__main__":
    main()
      
