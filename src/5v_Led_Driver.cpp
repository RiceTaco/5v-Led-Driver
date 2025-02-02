#include <stdio.h>
#include "pico/stdlib.h"
#include "hardware/pio.h"
#include "hardware/gpio.h"
#include "pwmRead.pio.h"

PIO pio = pio0;
uint sm = 0;
class ledStrip {
    public:
        
        ledStrip(uint8_t pin) : pin(pin) {
            gpio_init(pin);
            gpio_set_dir(pin, GPIO_OUT);
        }
        void setBrightness(uint8_t brightness) {
            gpio_put(pin, brightness);
        }
        void turnOff() {
            gpio_put(pin, 0);
        }
        void setPin(uint8_t pin) {
            this->pin = pin;
        }
        void setPattern(uint8_t pattern) {
            this->pattern = pattern;
        }


      
    private:
        uint8_t pin;
        uint8_t pattern;
};


// Define the pwm_reader_program
extern const pio_program_t pwm_reader_program;

void setupPWMReader(uint pin) {
    uint offset = pio_add_program(pio, &pwm_reader_program);
    pio_sm_config c = pio_get_default_sm_config();
    sm_config_set_wrap(&c, offset, offset + pwm_reader_program.length - 1);

    // Map the state machine's 'in' pin to the specified GPIO
    sm_config_set_in_pins(&c, pin);
    pio_gpio_init(pio, pin);
    pio_sm_set_consecutive_pindirs(pio, sm, pin, 1, false);

    // Initialize the state machine
    pio_sm_init(pio, sm, offset, &c);
    pio_sm_set_enabled(pio, sm, true);
}

void readPWM(uint &high_time, uint &low_time) {
    high_time = pio_sm_get_blocking(pio, sm);
    low_time = pio_sm_get_blocking(pio, sm);
}

int main()
{
    stdio_init_all();

   
}
