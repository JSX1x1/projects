# Makefile for the Kernel Assembly Code

# Compiler and assembler options
ASM = nasm
ASM_FLAGS = -f elf64 -g

# Linker and linker options
LD = ld
LD_FLAGS = -m elf_x86_64

# Output files
KERNEL_BIN = kernel.bin
KERNEL_OBJ = kernel.o
KERNEL_SRC = kernel.asm

# Clean up build files
RM = rm -f

# Default target: build the kernel
all: $(KERNEL_BIN)

# Assemble the kernel source into an object file
$(KERNEL_OBJ): $(KERNEL_SRC)
	$(ASM) $(ASM_FLAGS) $(KERNEL_SRC) -o $(KERNEL_OBJ)

# Link the object file to create the kernel binary
$(KERNEL_BIN): $(KERNEL_OBJ)
	$(LD) $(LD_FLAGS) -o $(KERNEL_BIN) $(KERNEL_OBJ)

# Clean up build files
clean:
	$(RM) $(KERNEL_OBJ) $(KERNEL_BIN)

# Run the kernel using QEMU (or another virtual machine emulator)
run: $(KERNEL_BIN)
	qemu-system-x86_64 -drive file=$(KERNEL_BIN),format=raw

# Rebuild everything (clean and then build)
rebuild: clean all

# Print help message
help:
	@echo "Makefile for Kernel Assembly"
	@echo ""
	@echo "Usage:"
	@echo "  make        - Build the kernel"
	@echo "  make clean  - Clean up build files"
	@echo "  make run    - Build and run the kernel using QEMU"
	@echo "  make rebuild - Clean and rebuild the kernel"
	@echo "  make help   - Show this help message"
