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

        # decimal conversions of instructions
        LDI = 130
        MUL = 162
        PRN = 71
        HLT = 1
        PUSH = 69
        POP = 70
        ADD = 160
        CALL = 80
        RET = 17
        CMP = 167
        JEQ = 85
        JNE = 86
        JMP = 84

        # initialize branchtable to hold functions
        self.branchtable = {}
        self.branchtable[LDI] = self.ldi
        self.branchtable[ADD] = self.add
        self.branchtable[MUL] = self.mul
        self.branchtable[PRN] = self.prn
        self.branchtable[HLT] = self.hlt
        self.branchtable[PUSH] = self.push
        self.branchtable[POP] = self.pop
        self.branchtable[CALL] = self.call
        self.branchtable[RET] = self.ret
        self.branchtable[CMP] = self.cmp
        self.branchtable[JEQ] = self.jeq
        self.branchtable[JNE] = self.jne
        self.branchtable[JMP] = self.jmp

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
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        elif op == "CMP":
            operand_a = self.reg[reg_a]
            operand_b = self.reg[reg_b]
            if operand_a == operand_b:
                self.equal = 1
            else:
                self.equal = 0
        else:
            raise Exception("Unsupported ALU operation")

    '''
    instruction handlers set in branchtable
    '''

    def ldi(self):
        '''
        an LDI instruction takes two operands loaded into ram
        '''
        # get operands
        operand_a = self.ram_read(self.pc+1)
        operand_b = self.ram_read(self.pc+2)
        # load to register
        self.reg[operand_a] = operand_b
        # increment program counter by 3
        self.pc += 3

    def add(self):
        # get operands
        operand_a = self.ram_read(self.pc+1)
        operand_b = self.ram_read(self.pc+2)
        # call alu function to handle the arithmetic
        self.alu('ADD', operand_a, operand_b)
        # increment program counter by 3
        self.pc += 3

    def mul(self):
        # get operands
        operand_a = self.ram_read(self.pc+1)
        operand_b = self.ram_read(self.pc+2)
        # call alu function to handle the arithmetic
        self.alu('MUL', operand_a, operand_b)
        # increment program counter by 3
        self.pc += 3

    def prn(self):
        # get operand
        operand_a = self.ram_read(self.pc+1)
        # print the value
        print(self.reg[operand_a])
        # increment program counter by 2
        self.pc += 2

    def hlt(self):
        # set running to False
        self.running = False

    def push(self):
        # get the register address from ram
        reg = self.ram_read(self.pc+1)
        # get the value from register
        val = self.reg[reg]
        # decrement stack pointer
        self.reg[self.sp] -= 1
        # set new value to ram
        self.ram[self.reg[self.sp]] = val
        # increment program counter by 2
        self.pc += 2

    def pop(self):
        # get the register address from ram
        reg = self.ram_read(self.pc+1)
        # get the value from register
        val = self.ram_read(self.reg[self.sp])
        # increment stack pointer
        self.reg[self.sp] += 1
        # set new value to reg
        self.reg[reg] = val
        # increment program counter by 2
        self.pc += 2

    def call(self):
        # setup
        reg = self.ram_read(self.pc + 1)
        # CALL
        self.reg[self.sp] -= 1  # decrement sp
        # push pc + 2 on to the stack
        self.ram_write(self.reg[self.sp], self.pc+2)
        # set pc to subroutine
        self.pc = self.reg[reg]

    def ret(self):
        self.pc = self.ram_read(self.reg[self.sp])
        self.reg[self.sp] += 1

    def cmp(self):
        reg_a = self.ram_read(self.pc+1)
        reg_b = self.ram_read(self.pc+2)
        # call alu function to handle the arithmetic
        self.alu('CMP', reg_a, reg_b)
        self.pc += 3

    def jeq(self):
        reg_a = self.ram_read(self.pc+1)
        operand_a = self.reg[reg_a]
        if self.equal:
            self.pc = operand_a
        else:
            self.pc += 2

    def jne(self):
        reg_a = self.ram_read(self.pc+1)
        operand_a = self.reg[reg_a]
        if self.equal == False:
            self.pc = operand_a
        else:
            self.pc += 2

    def jmp(self):
        reg_a = self.ram_read(self.pc+1)
        operand_a = self.reg[reg_a]
        self.pc = operand_a

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
