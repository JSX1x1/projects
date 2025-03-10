Certainly! Below is a detailed README in Markdown format, explaining your assembly code and its components. You can use this for your GitHub project.

---

# Kernel Assembly Code Documentation

This repository contains a basic kernel written in assembly, with functions for interrupt handling, memory allocation, task scheduling, and input/output operations. It is a low-level operating system kernel that manages tasks and interacts with hardware via direct I/O operations.

## Features

- **Interrupt Handling**: The kernel handles interrupts by setting up an Interrupt Descriptor Table (IDT).
- **Memory Management**: A simple memory allocation function that tracks heap usage.
- **Task Scheduling**: A basic task switching mechanism that allows two tasks to run concurrently in a round-robin fashion.
- **I/O Operations**: Functions for reading from and writing to I/O ports.

---

## Table of Contents

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
   - [_Z5task1v](#z5task1v)
   - [_Z5task2v](#z5task2v)
   - [_Z11kernel_mainv](#z11kernel_mainv)
4. [Compilation and Setup](#compilation-and-setup)
5. [Usage](#usage)
6. [License](#license)

---

## Introduction

This project is an assembly-based kernel that provides a simple environment for managing tasks and handling interrupts. It interacts directly with hardware via I/O port operations, manages a basic heap for memory allocation, and switches between two tasks using round-robin scheduling.

This kernel is intended as an educational tool to understand how low-level kernel development works, especially focusing on assembly language and system programming concepts.

---

## File Structure

```
/project-root
├── kernel.asm       # The main assembly code file containing the kernel functions
├── Makefile         # Build instructions for compiling the kernel
└── README.md        # This documentation
```

---

## Functions

### `_Z4outbth`

This function writes a byte to a specified I/O port.

**Parameters:**
- `edi`: The I/O port number (16-bit).
- `esi`: The byte value to be written.

**Operations:**
- Stores the I/O port and data to the stack.
- Writes the byte to the specified I/O port using the `outb` instruction.

---

### `_Z3inbt`

This function reads a byte from an I/O port.

**Parameters:**
- `edi`: The I/O port number (16-bit).

**Operations:**
- Reads a byte from the specified I/O port using the `inb` instruction.
- Stores the byte read into a local variable.

---

### `_Z6mallocm`

A simple memory allocation function that provides memory from a heap.

**Parameters:**
- `rdi`: The requested size of memory.

**Operations:**
- Adds the requested memory size to the current heap pointer.
- Checks if the total heap usage exceeds the 1MB limit.
- Updates the global heap pointer and returns the allocated memory address.

---

### `_Z11irq_handlerv`

This is an example interrupt handler function for IRQ 32.

**Operations:**
- Outputs the IRQ number to an I/O port via the `outbth` function.

---

### `_Z12set_idt_gateim`

Sets a gate in the Interrupt Descriptor Table (IDT) for handling interrupts.

**Parameters:**
- `edi`: The interrupt number (32-bit).
- `rsi`: The address of the interrupt handler function (64-bit).

**Operations:**
- Stores the handler address in the appropriate entry in the IDT.
- Sets flags and attributes for the interrupt gate.

---

### `_Z8load_idtv`

Loads the Interrupt Descriptor Table (IDT) into the processor.

**Operations:**
- Uses the `lidt` instruction to load the IDT from memory into the processor.

---

### `_Z11task_switchv`

This function switches between tasks using a round-robin scheduler.

**Operations:**
- Loads the current task ID.
- Adjusts the task ID to determine the next task.
- Switches the stack pointer to the new task's stack.

---

### `_Z11task_createPFvvE`

This function creates a new task by setting up a task structure.

**Parameters:**
- `rdi`: A pointer to the function that the task will execute.

**Operations:**
- Allocates space for the new task.
- Sets the function pointer and task-related data.

---

### `_Z5task1v`

This is the first task that will run in an infinite loop.

**Operations:**
- Continuously outputs data to an I/O port.

---

### `_Z5task2v`

This is the second task that will run in an infinite loop.

**Operations:**
- Continuously outputs data to an I/O port.

---

### `_Z11kernel_mainv`

The main entry point of the kernel.

**Operations:**
- Sets up interrupt handling.
- Creates two tasks (`task1` and `task2`).
- Enters an infinite loop where tasks are switched using the `task_switchv` function.

---

## Compilation and Setup

To compile and run the kernel, follow these steps:

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/kernel-assembly.git
   cd kernel-assembly
   ```

2. **Build the Kernel**:

   The kernel can be built using a Makefile. To compile the code, run:

   ```bash
   make
   ```

   This will assemble the `kernel.asm` file into a binary that can be loaded onto a virtual machine or real hardware.

3. **Running the Kernel**:

   To test the kernel, you can use a virtual machine (e.g., QEMU) or an emulator. For example, to run the kernel using QEMU, use the following command:

   ```bash
   qemu-system-x86_64 -drive file=kernel.bin,format=raw
   ```

---

## Usage

Once the kernel is running, it will perform the following tasks:

- **Interrupt Handling**: IRQ 32 will trigger the interrupt handler.
- **Task Scheduling**: The kernel will continuously switch between two tasks (`task1` and `task2`), which will output data to an I/O port.

---

Feel free to fork, modify, or contribute to this project. If you have any questions or suggestions, feel free to open an issue or create a pull request!