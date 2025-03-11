# **🛠 Kernel Assembly & C Code Documentation**  

This repository contains a **low-level operating system kernel**, written in **assembly and C**, with functions for **interrupt handling, memory allocation, task scheduling, input/output operations, system calls, and user-mode execution**.  

This kernel is designed as an **educational project** to explore **operating system fundamentals**, including **hardware interaction, preemptive multitasking, and memory management**.  

---

## **📌 Features**  

✅ **Interrupt Handling** – Manages hardware interrupts using an **Interrupt Descriptor Table (IDT)**.  
✅ **Memory Management** – Implements **basic heap allocation** and **paging support**.  
✅ **Preemptive Multitasking** – Uses **PIT (Programmable Interval Timer) to trigger task switching**.  
✅ **I/O Operations** – Read/write directly to **I/O ports** for hardware communication.  
✅ **System Calls** – Provides a **syscall interface (int 0x80)** for user programs to access kernel functions.  
✅ **User Mode Execution** – Runs user programs in **Ring 3**, enforcing **security and privilege separation**.  

---

## **📜 Table of Contents**  
1. [Introduction](#introduction)  
2. [File Structure](#file-structure)  
3. [Functions](#functions)  
   - [_Z4outbth](#z4outbth)  
   - [_Z3inbt](#z3inbt)  
   - [_Z6mallocm](#z6mallocm)  
   - [_Z11irq_handlerv](#z11irq_handlerv)  
   - [_Z12set_idt_gateim](#z12set_idt_gateim)  
   - [_Z8load_idtv](#z8load_idtv)  
   - [_Z11task_switchv](#z11task_switchv)  
   - [_Z11task_createPFvvE](#z11task_createPFvvE)  
   - [_Z11syscall_handler](#z11syscall_handler)  
   - [_Z11enter_usermode](#z11enter_usermode)  
   - [_Z5task1v](#z5task1v)  
   - [_Z5task2v](#z5task2v)  
   - [_Z11kernel_mainv](#z11kernel_mainv)  
4. [Compilation and Setup](#compilation-and-setup)  
5. [Usage](#usage)  
6. [License](#license)  

---

## **📌 Introduction**  

This project is an **assembly & C-based kernel** that provides a simple environment for:  
- **Handling interrupts** (including exceptions and hardware IRQs).  
- **Task switching** via preemptive multitasking using **PIT timer interrupts**.  
- **Memory management** with **paging** and **basic heap allocation**.  
- **System calls** to allow user programs to safely interact with the kernel.  
- **Running user-mode programs in Ring 3**, enforcing privilege separation.  

This kernel is an **educational tool** for understanding **low-level OS development**.  

---

## **📂 File Structure**  
```
/project-root
├── kernel.asm       # Core assembly functions (task switching, interrupts, syscalls)
├── idt.c            # Interrupt Descriptor Table (IDT) setup
├── pit.c            # Programmable Interval Timer (PIT) initialization
├── paging.c         # Basic paging and virtual memory management
├── syscall.c        # System call handling (int 0x80)
├── io.h             # Inline assembly for I/O port access
├── Makefile         # Build instructions
└── README.md        # This documentation
```

---

## **📜 Functions**  

### **🔹 `_Z4outbth` (I/O Write)**
- **Writes a byte to a specified I/O port** using `outb` instruction.  
- Used for **hardware communication** (e.g., sending data to a PIC or PIT).  

---

### **🔹 `_Z3inbt` (I/O Read)**
- **Reads a byte from an I/O port** using `inb`.  
- Used to **query hardware status**.  

---

### **🔹 `_Z6mallocm` (Heap Allocation)**
- Implements **basic memory allocation**.  
- Tracks **heap usage** and returns allocated addresses.  
- **Checks for memory overflows** (max **1MB heap**).  

---

### **🔹 `_Z11irq_handlerv` (IRQ Handler)**
- Handles **IRQ 32** (Programmable Interval Timer).  
- Calls `task_switch()` to **switch tasks preemptively**.  

---

### **🔹 `_Z12set_idt_gateim` (Interrupt Setup)**
- **Sets an entry** in the **Interrupt Descriptor Table (IDT)**.  
- Registers **exception handlers, IRQs, and system calls**.  

---

### **🔹 `_Z8load_idtv` (Load IDT into CPU)**
- Loads the **Interrupt Descriptor Table (IDT)** into the processor using `lidt`.  

---

### **🔹 `_Z11task_switchv` (Task Switching)**
- Implements **round-robin preemptive multitasking**.  
- Saves & restores **register states** when switching between tasks.  
- Uses **PIT timer (IRQ 0) to trigger automatic task switching**.  

---

### **🔹 `_Z11task_createPFvvE` (Task Creation)**
- Creates a **new task** by allocating memory and setting up its stack.  
- Adds the task to a **task queue** for scheduling.  

---

### **🔹 `_Z11syscall_handler` (System Calls)**
- Implements a **syscall handler (int 0x80)**.  
- Maps **syscall numbers to kernel functions** (e.g., printing to console).  

#### **📜 Example Syscall Code in C**
```c
void handle_syscall(uint32_t syscall_num, void *arg1) {
    switch (syscall_num) {
        case 1:
            sys_print((char*)arg1);
            break;
        default:
            break;
    }
}
```
- **Now, user programs can call syscalls using `int 0x80`!**  

---

### **🔹 `_Z11enter_usermode` (User Mode Execution)**
- Switches execution **from Ring 0 (Kernel) to Ring 3 (User Mode)**.  
- **Prepares a user-mode stack** before switching.  

#### **📜 User Mode Entry (Assembly)**
```assembly
global enter_usermode

enter_usermode:
    cli
    push 0x23  ; User mode data segment
    push 0x1000  ; User stack pointer
    pushf      ; EFLAGS
    push 0x1B  ; User mode code segment
    push user_main
    iretq
```
- **User programs now run safely in Ring 3!**  

---

### **🔹 `_Z5task1v` / `_Z5task2v` (Example Tasks)**
- **Demonstrates multitasking** by running infinite loops.  

---

### **🔹 `_Z11kernel_mainv` (Kernel Entry Point)**
- **Initializes interrupts, IDT, paging, and PIT**.  
- **Creates multiple tasks**.  
- **Switches to user mode**.  

---

## **⚙️ Compilation and Setup**  

### **1️⃣ Clone the Repository**  
```sh
git clone https://github.com/JSX1x1/projects/tree/main/Raw%20Code/test_kernel.git
cd test_kernel
```

### **2️⃣ Build the Kernel**  
```sh
make
```

### **3️⃣ Run the Kernel in QEMU**  
```sh
qemu-system-x86_64 -drive file=kernel.bin,format=raw
```
✔ **Now, the kernel will boot and run in QEMU!**  

---

## **📌 Usage**
- **Kernel boots and sets up interrupts & memory**.  
- **User programs run in Ring 3** with **syscall support**.  
- **Multitasking is handled via PIT timer interrupts**.  

---

## **📜 License**
This project is open-source and provided **for educational purposes only**.  
