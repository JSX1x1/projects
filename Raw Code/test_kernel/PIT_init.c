#include <stdint.h>
#include "io.h" // Contains outb() function

#define PIT_FREQUENCY 100 // 100Hz = 10ms per tick
#define PIT_COMMAND 0x43
#define PIT_CHANNEL0 0x40

void init_pit(uint32_t frequency) {
    uint32_t divisor = 1193180 / frequency;
    outb(0x43, 0x36);
    outb(0x40, (uint8_t)(divisor & 0xFF));
    outb(0x40, (uint8_t)((divisor >> 8) & 0xFF));
}


extern void pit_handler();

void init_irq() {
    set_idt_gate(32, (uint64_t)pit_handler); // IRQ 0 is mapped to IDT entry 32
    init_pit(PIT_FREQUENCY);
}

