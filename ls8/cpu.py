"""CPU functionality."""

import sys
import os


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        # 256 bytes of memory
        self.ram = [0] * 256
        # register
        self.reg = [0] * 8
        # program counter
        self.pc = 0
        # stack pointer
        self.sp = 7
        # run state
        self.running = True

    def load(self, file_name):
        """Load a program into memory."""

        address = 0

        directory = os.path.join(os.path.dirname(__file__), "examples/")
        file_path = os.path.join(directory, file_name)

        program = list()
        try:
            with open(file_path) as f:
                for line in f:
                    comment = line.split("#")
                    num = comment[0].strip()
                    # ignore lines without instruction code
                    if len(num) == 0:
                        continue
                    # convert from binary to decimal
                    value = int(num, 2)
                    # add to program list
                    program.append(value)

        except FileNotFoundError:
            print(f"{file_name} not found")
            sys.exit(2)

        for instruction in program:
            self.ram[address] = instruction
            address += 1

        for instruction in program:
            self.ram[address] = instruction
            address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        # elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def ram_read(self, address):
        '''
        should accept the address to read and return the value stored
        '''
        return self.ram[address]

    def ram_write(self, address, value):
        '''
        should accept a value to write, and the address to write it to
        '''
        self.ram[address] = value

    def run(self):
        """Run the CPU."""
        pass
