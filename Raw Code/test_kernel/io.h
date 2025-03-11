#ifndef IO_H
#define IO_H

#include <stdint.h>

/**
 * @brief Output a byte to the specified I/O port.
 * @param port The I/O port number.
 * @param value The byte value to send.
 */
static inline void outb(uint16_t port, uint8_t value) {
    asm volatile ("outb %0, %1" : : "a"(value), "Nd"(port));
}

/**
 * @brief Output a word (2 bytes) to the specified I/O port.
 * @param port The I/O port number.
 * @param value The 16-bit word to send.
 */
static inline void outw(uint16_t port, uint16_t value) {
    asm volatile ("outw %0, %1" : : "a"(value), "Nd"(port));
}

/**
 * @brief Output a double word (4 bytes) to the specified I/O port.
 * @param port The I/O port number.
 * @param value The 32-bit value to send.
 */
static inline void outl(uint16_t port, uint32_t value) {
    asm volatile ("outl %0, %1" : : "a"(value), "Nd"(port));
}

/**
 * @brief Read a byte from the specified I/O port.
 * @param port The I/O port number.
 * @return The byte value read from the port.
 */
static inline uint8_t inb(uint16_t port) {
    uint8_t value;
    asm volatile ("inb %1, %0" : "=a"(value) : "Nd"(port));
    return value;
}

/**
 * @brief Read a word (2 bytes) from the specified I/O port.
 * @param port The I/O port number.
 * @return The 16-bit word read from the port.
 */
static inline uint16_t inw(uint16_t port) {
    uint16_t value;
    asm volatile ("inw %1, %0" : "=a"(value) : "Nd"(port));
    return value;
}

/**
 * @brief Read a double word (4 bytes) from the specified I/O port.
 * @param port The I/O port number.
 * @return The 32-bit value read from the port.
 */
static inline uint32_t inl(uint16_t port) {
    uint32_t value;
    asm volatile ("inl %1, %0" : "=a"(value) : "Nd"(port));
    return value;
}

/**
 * @brief Introduce a short delay after an I/O operation.
 */
static inline void io_wait(void) {
    asm volatile ("outb %%al, $0x80" : : "a"(0));
}

#endif // IO_H
