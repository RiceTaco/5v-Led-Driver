#include <stdio.h>
#include "pico/stdlib.h"
#include "hardware/spi.h"
#include "hardware/i2c.h"
#include "hardware/pio.h"
#include "hardware/interp.h"
#include "hardware/timer.h"
#include "hardware/watchdog.h"
#include "hardware/clocks.h"
#include "pwmRead.pio.h"

void pwmSetup() {
     PIO pio = pio0;
    uint sm_id = pio_claim_unused_sm(pio, true);

    uint offset = pio_add_program(pio, &pwm_reader_program);
    pio_sm_config c = pwm_reader_program_get_default_config(offset);1

    // Configure the GPIO pin for input
    pio_gpio_init(pio, 2); // Change 2 to the desired GPIO pin
    pio_sm_set_consecutive_pindirs(pio, sm_id, 2, 1, false);

    pio_sm_init(pio, sm_id, offset, &c);
    pio_sm_set_enabled(pio, sm_id, true);

}

void readPWM() {        
    uint32_t high_time = pio_sm_get_blocking(pio, sm_id);
    uint32_t low_time = pio_sm_get_blocking(pio, sm_id);

    // Calculate duty cycle and frequency
    printf("Duty Cycle: %f%%\n", (float)high_time / (high_time + low_time) * 100);
    printf("Frequency: %f Hz\n", 125000000.0 / (high_time + low_time));
}
int main()
{
    stdio_init_all();

   
}
