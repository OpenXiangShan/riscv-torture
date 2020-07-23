######### Program Generation #########

OPTIONS :=

gen:
	mill generator.run $(OPTIONS)


######### Program Compilation #########

asm_tests = test.S

RISCV_GCC = riscv64-linux-gnu-gcc
RISCV_GCC_OPTS = -nostdlib -nostartfiles -Wa,-march=rv64im -Wl,--build-id=none
RISCV_OBJDUMP = riscv64-linux-gnu-objdump
RISCV_OBJCOPY = riscv64-linux-gnu-objcopy -S --set-section-flags .bss=alloc,contents
# ADJUST_VMA = --adjust-vma +0x100000

asm_tests_elf = $(asm_tests:.S=.elf)
asm_tests_bin = $(asm_tests:.S=.bin)

$(asm_tests_elf): %: $(asm_tests)
	$(RISCV_GCC) $(RISCV_GCC_OPTS) -I../../env/p -T../../env/p/link.ld $< -o $@

$(asm_tests_bin): $(asm_tests_elf)
	$(RISCV_OBJCOPY) -O binary $(ADJUST_VMA) $< $@
	$(RISCV_OBJDUMP) -d $(ADJUST_VMA) $< > test.txt


######### Program Runing #########

PORT ?= 10000

run: $(asm_tests_bin)
	#make -C $(NEMU_HOME) ISA=riscv64 run ARGS="-b $(abspath $(asm_tests_bin))"
	$(MAKE) -C $(NOOP_HOME) emu E=0 IMAGE="$(abspath $(asm_tests_bin))"


######### Utility #########

killall:
	-pkill -9 python
	-pkill -9 java
	-pkill -9 qemu


# count the total number of tests passed and total number of instructions executed
stat:
	watch -n 1 'find . -name "log.txt" | xargs cat | grep pass | awk "{t+=\$$2; i+=\$$4}END{print t, i}"'

# show CPU frequency
cpu:
	watch -n 1 'cat /proc/cpuinfo| grep MHz | grep -oE "[^ ]*$$" | column'


.PHONY: gen run killall stat cpu
