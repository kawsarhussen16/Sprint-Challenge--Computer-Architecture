"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.reg[7] = 0xf4
        self.PC = 0
        self.MAR = 0
        self.MDR = 0
        self.IR = 0
        self.SP = 7
        self.FL = 0
        self.E = 0
        self.L = 0
        self.G = 0
    
    def ram_read(self, MAR):
        return self.ram[MAR]

    def ram_write(self, MAR, MDR):
        self.ram[MAR] = MDR

    def run_push(self, a):
        self.reg[self.SP] -= 1
        self.ram[self.reg[self.SP]] = self.reg[a]

    def run_pop(self, a):
        self.reg[a] = self.ram[self.reg[self.SP]]
        self.reg[self.SP] += 1

    def load(self):
        """Load a program into memory."""

        address = 0

        with open(sys.argv[1]) as f:
            for line in f:
                if line[0] != '#' and line != '\n':
                    self.ram[address] = int(line[0:8], 2)
                    address += 1
            f.closed


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""
        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]

            self.reg[reg_a] = self.reg[reg_a] % self.reg[reg_b]
        elif op == "CMP":
            if self.reg[reg_a] == self.reg[reg_b]:
                self.E = 1
                self.L = 0
                self.G = 0
            elif self.reg[reg_a] <= self.reg[reg_b]:
                self.E = 0
                self.L = 1
                self.G = 0
            else:
                self.E = 0
                self.L = 0
                self.G = 1
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()
  
    def run(self):
        """Run the CPU."""
        cpu_run = True

        HLT = 0b00000001
        LDI = 0b10000010
        PRN = 0b01000111
        PUSH = 0b01000101
        POP = 0b01000110
        RET = 0b00010001
        ADD = 0b10100000
        MUL = 0b10100010
        JMP = 0b01010100
        CMP = 0b10100111
        JEQ = 0b01010101
        JNE = 0b01010110
  

        while(cpu_run):
            operand_a = self.ram_read(self.PC + 1)
            operand_b = self.ram_read(self.PC + 2)
            # print(self.PC)
            if self.ram[self.PC] == HLT:
                cpu_run == False
                break

            elif self.ram[self.PC] == LDI:
                self.reg[operand_a] = operand_b
                self.PC += 3

            elif self.ram[self.PC] == PRN:
                print(self.reg[operand_a])
                self.PC += 2


            elif self.ram[self.PC] == JMP:
                self.PC = self.reg[operand_a]

            elif self.ram[self.PC] == CMP:
                self.alu("CMP", operand_a, operand_b)
                self.PC += 3

            elif self.ram[self.PC] == JEQ:
                if self.E == 1:
                    self.PC = self.reg[operand_a]
                else:
                    self.PC += 2

            elif self.ram[self.PC] == JNE:
                if self.E == 0:
                    self.PC = self.reg[operand_a]
                else:
                    self.PC += 2

            else:
                cpu_run == False
                break
                print(f"You have entered an invalid command: {self.ram[self.PC]}. Program exiting...")