#include <stdint.h>

void sys_print(const char *message);

void handle_syscall(uint32_t syscall_num, void *arg1) {
    switch (syscall_num) {
        case 1: // Syscall 1 = print string
            sys_print((char*)arg1);
            break;
        default:
            break;
    }
}
