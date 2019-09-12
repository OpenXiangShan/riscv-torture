OPTIONS :=

gen:
	mill generator.run $(OPTIONS)

asm_tests = test.S

RISCV_GCC = riscv64-unknown-elf-gcc
RISCV_GCC_OPTS = -nostdlib -nostartfiles -Wa,-march=rv64im
RISCV_OBJDUMP = riscv64-unknown-elf-objdump --disassemble-all --section=.text --section=.data --section=.bss
RISCV_OBJCOPY = riscv64-unknown-elf-objcopy -S --set-section-flags .bss=alloc,contents
ADJUST_VMA = --adjust-vma +0x100000

#------------------------------------------------------------
# Build assembly tests

asm_tests_elf = $(asm_tests:.S=.elf)
asm_tests_bin = $(asm_tests:.S=.bin)

$(asm_tests_elf): %: $(asm_tests)
	$(RISCV_GCC) $(RISCV_GCC_OPTS) -I../../env/p -T../../env/p/link.ld $< -o $@

$(asm_tests_bin): $(asm_tests_elf)
	$(RISCV_OBJCOPY) -O binary $(ADJUST_VMA) $< $@
	$(RISCV_OBJDUMP) $(ADJUST_VMA) $< > test.txt

PORT ?= 10000

run: $(asm_tests_bin)
	make -C $(NEMU_HOME) ISA=riscv64 run ARGS="-b $(abspath $(asm_tests_bin)) -p $(PORT)"

all: $(asm_tests_bin)
