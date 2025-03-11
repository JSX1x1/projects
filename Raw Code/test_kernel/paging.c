#include <stdint.h>

#define PAGE_SIZE 4096
#define PAGE_PRESENT 1
#define PAGE_WRITABLE 2
#define PAGE_USER 4

uint32_t page_directory[1024] __attribute__((aligned(4096)));
uint32_t page_tables[1024][1024] __attribute__((aligned(4096)));

void init_paging() {
    for (int i = 0; i < 1024; i++) {
        page_directory[i] = (uint32_t) &page_tables[i] | PAGE_PRESENT | PAGE_WRITABLE;
        for (int j = 0; j < 1024; j++) {
            page_tables[i][j] = (i * 1024 + j) * PAGE_SIZE | PAGE_PRESENT | PAGE_WRITABLE;
        }
    }

    // Load page directory into CR3
    asm volatile("mov %0, %%cr3":: "r"(page_directory));

    // Enable paging (set PG bit in CR0)
    uint32_t cr0;
    asm volatile("mov %%cr0, %0" : "=r"(cr0));
    cr0 |= 0x80000000;
    asm volatile("mov %0, %%cr0":: "r"(cr0));
}
