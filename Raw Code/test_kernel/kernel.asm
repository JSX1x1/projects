; Function to output a byte to an I/O port (outb instruction)
_Z4outbth:
    push    rbp                ; Save the base pointer of the current function (setup stack frame)
    mov     rbp, rsp           ; Move the stack pointer into rbp for current function context
    mov     edx, edi           ; Move I/O port number from edi to dx
    mov     eax, esi           ; Move byte value from esi to eax
    mov     WORD PTR [rbp-4], dx    ; Store the 16-bit port number (dx) on the stack
    mov     BYTE PTR [rbp-8], al    ; Store the 8-bit data (al) on the stack
    movzx   eax, BYTE PTR [rbp-8]  ; Load the byte value back into eax (zero-extend)
    movzx   edx, WORD PTR [rbp-4]  ; Load the port number back into edx (zero-extend)
    outb    al, dx               ; Output the byte (al) to the I/O port (dx)
    nop                         ; No operation (used for debugging or alignment)
    pop     rbp                 ; Restore the previous base pointer
    ret                         ; Return from function

; Function to input a byte from an I/O port (inb instruction)
_Z3inbt:
    push    rbp                ; Save the base pointer
    mov     rbp, rsp           ; Set up the stack frame
    mov     eax, edi           ; Move the port number from edi to eax
    mov     WORD PTR [rbp-20], ax ; Store the port number on the stack
    movzx   eax, WORD PTR [rbp-20] ; Zero-extend the port number to eax
    mov     edx, eax           ; Move the port number from eax to edx (for inb)
    inb     dx, al             ; Input a byte from the I/O port into al
    mov     BYTE PTR [rbp-1], al ; Store the byte value in a local variable
    movzx   eax, BYTE PTR [rbp-1] ; Load the byte back into eax (zero-extend)
    pop     rbp                 ; Restore the previous base pointer
    ret                         ; Return from function

; Function to allocate memory (simple heap management)
_Z6mallocm:
    push    rbp                 ; Save the current base pointer
    mov     rbp, rsp            ; Set up stack frame
    mov     QWORD PTR [rbp-24], rdi  ; Store the requested size in the stack frame
    mov     rdx, QWORD PTR _ZL12heap_pointer[rip]  ; Load the heap pointer (global variable)
    mov     rax, QWORD PTR [rbp-24]   ; Load the requested size into rax
    add     rax, rdx                ; Add the heap pointer to the requested size
    cmp     rax, 1048576             ; Check if the allocated memory exceeds 1MB
    jbe     .L5                      ; If less than or equal, jump to memory allocation logic
    mov     eax, 0                   ; Return 0 if memory request is too large
    jmp     .L6                      ; Jump to end of function
.L5:
    mov     rax, QWORD PTR _ZL12heap_pointer[rip] ; Get current heap pointer
    add     rax, OFFSET FLAT:_ZL4heap ; Calculate next available memory address
    mov     QWORD PTR [rbp-8], rax    ; Store the allocated address on the stack
    mov     rdx, QWORD PTR _ZL12heap_pointer[rip] ; Update the heap pointer
    mov     rax, QWORD PTR [rbp-24]  ; Load the requested size again
    add     rax, rdx                ; Update the heap pointer with the allocated memory
    mov     QWORD PTR _ZL12heap_pointer[rip], rax ; Set the new heap pointer
    mov     rax, QWORD PTR [rbp-8]   ; Return the allocated address
.L6:
    pop     rbp                      ; Restore the base pointer
    ret                              ; Return from function

; Interrupt handler for IRQ 32 (example)
_Z11irq_handlerv:
    push    rbp                 ; Save the base pointer
    mov     rbp, rsp            ; Set up stack frame
    mov     esi, 32             ; IRQ number (32)
    mov     edi, 32             ; Pass IRQ number to outbth (for example purposes)
    call    _Z4outbth           ; Call outbth to output data to a port
    nop                         ; No operation (used for debugging or alignment)
    pop     rbp                 ; Restore the previous base pointer
    ret                         ; Return from function

; IDT (Interrupt Descriptor Table) - reserved for 2048 bytes
idt:
    .zero   2048

; Set a gate in the Interrupt Descriptor Table
_Z12set_idt_gateim:
    push    rbp                    ; Save the base pointer
    mov     rbp, rsp               ; Set up the stack frame
    mov     DWORD PTR [rbp-4], edi  ; Store the interrupt number in the stack
    mov     QWORD PTR [rbp-16], rsi ; Store the handler address in the stack
    mov     rax, QWORD PTR [rbp-16] ; Load handler address into rax
    mov     edx, eax                ; Store the handler address in edx
    mov     eax, DWORD PTR [rbp-4]  ; Load interrupt number into eax
    cdqe                            ; Convert to 64-bit value (sign-extend)
    mov     WORD PTR idt[0 + rax*8], dx ; Store the low 16 bits of the handler address
    mov     rax, QWORD PTR [rbp-16] ; Load handler address into rax
    shr     rax, 16                ; Shift to get the upper 16 bits
    mov     edx, eax                ; Store the high 16 bits of the handler address
    mov     eax, DWORD PTR [rbp-4]  ; Load interrupt number again
    cdqe                            ; Convert to 64-bit value (sign-extend)
    mov     WORD PTR idt[6 + rax*8], dx ; Store the high 16 bits of the handler address
    mov     eax, DWORD PTR [rbp-4]  ; Load interrupt number into eax
    cdqe                            ; Convert to 64-bit value (sign-extend)
    mov     WORD PTR idt[2 + rax*8], 8 ; Set flags (0x08) for interrupt
    mov     eax, DWORD PTR [rbp-4]  ; Load interrupt number into eax
    cdqe                            ; Convert to 64-bit value (sign-extend)
    mov     BYTE PTR idt[4 + rax*8], 0 ; Set interrupt type (0 for reserved)
    mov     eax, DWORD PTR [rbp-4]  ; Load interrupt number into eax
    cdqe                            ; Convert to 64-bit value (sign-extend)
    mov     BYTE PTR idt[5 + rax*8], -114 ; Set additional attributes (for example, negative number)
    nop                             ; No operation (used for debugging or alignment)
    pop     rbp                     ; Restore the previous base pointer
    ret                             ; Return from function

; Load the IDT into the processor
_Z8load_idtv:
    push    rbp                    ; Save the base pointer
    mov     rbp, rsp               ; Set up the stack frame
    mov     QWORD PTR [rbp-8], OFFSET FLAT:idt ; Store address of IDT
    mov     rax, QWORD PTR [rbp-8]  ; Load IDT address into rax
    lidt    (rax)                  ; Load IDT using the lidt instruction
    nop                             ; No operation (used for debugging or alignment)
    pop     rbp                     ; Restore the previous base pointer
    ret                             ; Return from function

; Global variables for tasks and the current task
tasks:
    .zero   163920                 ; Reserve space for task-related data
current_task:
    .zero   4                      ; Reserve space for storing the current task ID

; Task switching function (switch between tasks)
_Z11task_switchv:
    push    rbp                     ; Save the base pointer
    mov     rbp, rsp                ; Set up stack frame
    mov     eax, DWORD PTR current_task[rip] ; Load current task ID into eax
    lea     ecx, [rax+1]            ; Increment task ID (switch to next task)
    movsx   rax, ecx                ; Sign-extend ecx to rax
    imul    rax, rax, 1717986919    ; Multiply by some constant (could be task switching cost)
    shr     rax, 32                 ; Shift to get higher bits
    mov     edx, eax                ; Store result in edx
    sar     edx, 2                  ; Arithmetic shift right (task adjustment)
    mov     eax, ecx                ; Move task ID into eax
    sar     eax, 31                 ; Arithmetic shift right (task ID adjustment)
    sub     edx, eax                ; Subtract to get final task ID
    mov     eax, edx                ; Move final result into eax
    sal     eax, 2                  ; Shift left to adjust for task structure
    add     eax, edx                ; Add to eax
    add     eax, eax                ; Double the value
    sub     ecx, eax                ; Subtract for final adjustment
    mov     edx, ecx                ; Store final task ID into edx
    mov     DWORD PTR current_task[rip], edx ; Store the updated current task ID
    mov     eax, DWORD PTR current_task[rip] ; Load current task ID into eax
    cdqe                            ; Convert to 64-bit value
    imul    rax, rax, 16392        ; Multiply by task size (16392 bytes)
    add     rax, OFFSET FLAT:tasks ; Add base address of tasks
    mov     rax, QWORD PTR [rax]    ; Load task address into rax
    mov     rax, %esp               ; Switch to the task's stack
    nop                             ; No operation (used for debugging or alignment)
    pop     rbp                     ; Restore the previous base pointer
    ret                             ; Return from function

; Function to create a new task
_Z11task_createPFvvE:
    push    rbp                     ; Save the base pointer
    mov     rbp, rsp                ; Set up stack frame
    mov     QWORD PTR [rbp-24], rdi ; Store task function pointer in stack
    mov     eax, DWORD PTR current_task[rip] ; Load current task ID into eax
    cdqe                            ; Convert to 64-bit value
    imul    rax, rax, 16392        ; Multiply by task size
    add     rax, OFFSET FLAT:tasks ; Add base address of tasks
    mov     QWORD PTR [rbp-8], rax  ; Store allocated task address
    mov     rax, QWORD PTR [rbp-8]  ; Load task address into rax
    add     rax, 8                  ; Increment task address by 8
    lea     rdx, [rax+16380]        ; Load task data structure pointer into rdx
    mov     rax, QWORD PTR [rbp-8]  ; Load task address into rax
    mov     QWORD PTR [rax], rdx    ; Set up task data pointer
    mov     rax, QWORD PTR [rbp-24] ; Load task function pointer into rax
    mov     ecx, eax                ; Pass function pointer as argument
    mov     rax, QWORD PTR [rbp-8]  ; Load task address into rax
    mov     rax, QWORD PTR [rax]    ; Get the task data structure address
    lea     rdx, [rax-4]            ; Adjust task data pointer by 4 bytes
    mov     rax, QWORD PTR [rbp-8]  ; Load task address into rax
    mov     QWORD PTR [rax], rdx    ; Update task's pointer
    mov     rax, QWORD PTR [rbp-8]  ; Reload task address into rax
    mov     rax, QWORD PTR [rax]    ; Get task data
    mov     DWORD PTR [rax], ecx    ; Store function pointer into task data
    mov     rax, QWORD PTR [rbp-8]  ; Reload task address
    mov     rax, QWORD PTR [rax]    ; Get task pointer again
    lea     rdx, [rax-4]            ; Adjust again
    mov     rax, QWORD PTR [rbp-8]  ; Load task address again
    mov     QWORD PTR [rax], rdx    ; Update task data pointer again
    mov     rax, QWORD PTR [rbp-8]  ; Reload task address again
    mov     rax, QWORD PTR [rax]    ; Get task data again
    mov     DWORD PTR [rax], 514    ; Store additional value (could be priority or status)
    nop                             ; No operation (used for debugging or alignment)
    pop     rbp                     ; Restore the previous base pointer
    ret                             ; Return from function

; Kernel main function (entry point)
_Z11kernel_mainv:
    push    rbp                     ; Save the base pointer
    mov     rbp, rsp                ; Set up stack frame
    mov     eax, OFFSET FLAT:_Z11irq_handlerv ; Load IRQ handler address
    mov     rsi, rax                ; Pass IRQ handler address to set_idt_gateim
    mov     edi, 32                 ; IRQ number 32
    call    _Z12set_idt_gateim      ; Set interrupt gate in IDT
    call    _Z8load_idtv           ; Load the IDT into the processor
    mov     edi, OFFSET FLAT:_Z5task1v ; Load address of task1 function
    call    _Z11task_createPFvvE    ; Create the first task
    mov     edi, OFFSET FLAT:_Z5task2v ; Load address of task2 function
    call    _Z11task_createPFvvE    ; Create the second task
.L18:
    call    _Z11task_switchv        ; Switch between tasks
    jmp     .L18                    ; Repeat task switching
