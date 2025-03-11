#include <stdint.h>

#define IDT_SIZE 256  // 256 Interrupts (x86 standard)

// Structure of an IDT entry (Interrupt Descriptor)
struct idt_entry {
    uint16_t offset_low;  // Lower 16 bits of ISR address
    uint16_t selector;    // Kernel segment selector
    uint8_t zero;         // Always zero
    uint8_t type_attr;    // Flags (Type and Privilege)
    uint16_t offset_high; // Upper 16 bits of ISR address
} __attribute__((packed));

// IDT descriptor structure
struct idt_ptr {
    uint16_t limit;  // Size of the IDT (in bytes) - 1
    uint32_t base;   // Base address of the IDT
} __attribute__((packed));

// Define IDT table
struct idt_entry idt[IDT_SIZE];
struct idt_ptr idt_descriptor;

// External assembly function to load IDT
extern void load_idt();

// Function to set an entry in the IDT
void set_idt_gate(int num, uint32_t base, uint16_t sel, uint8_t flags) {
    idt[num].offset_low  = base & 0xFFFF;   // Lower 16 bits of ISR
    idt[num].selector    = sel;             // Kernel code segment
    idt[num].zero        = 0;               // Reserved
    idt[num].type_attr   = flags;           // Type and attributes
    idt[num].offset_high = (base >> 16) & 0xFFFF; // Upper 16 bits of ISR
}

// Function to initialize and load the IDT
void init_idt() {
    idt_descriptor.limit = sizeof(idt) - 1;
    idt_descriptor.base  = (uint32_t)&idt;

    // Load IDT using lidt
    load_idt();
}